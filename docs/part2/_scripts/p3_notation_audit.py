"""Inspect native drawing geometry for independent-review findings R1–R4.
Author: 722I0004 · AI-assisted (Codex). Static, read-only; no app imports.
"""
from pathlib import Path
import html,math,re,xml.etree.ElementTree as ET

def text(cell):
    return html.unescape(re.sub(r'<[^>]+>','',cell.get('value',''))).strip()

def style(cell):
    return dict(part.split('=',1) for part in cell.get('style','').split(';') if '=' in part)

def audit(path,data,meta,model,check):
    native=path.with_suffix('.drawio')
    if not native.is_file():return
    cells={c.get('id'):c for c in ET.parse(native).findall('.//mxCell')}
    key=path.name;kind=meta.get('diagram_type')
    def rect(cell_id,seen=None):
        seen=set() if seen is None else seen
        if cell_id not in cells or cell_id in seen:return None
        cell=cells[cell_id];g=cell.find('mxGeometry')
        if g is None:return None
        x,y,w,h=(float(g.get(n,'0')) for n in ('x','y','width','height'))
        parent=cell.get('parent')
        if parent not in ('0','1',None):
            outer=rect(parent,seen|{cell_id})
            if outer:x+=outer[0];y+=outer[1]
        return x,y,w,h
    def point_to_rect(point,box):
        x,y,w,h=box;px,py=point
        return math.hypot(max(x-px,0,px-x-w),max(y-py,0,py-y-h))
    if kind=='package':
        for cell in cells.values():
            if cell.get('edge')=='1' and cell.get('id','').startswith('dep_'):
                s=style(cell)
                check('package_dependency_notation',key+':'+cell.get('id'),s.get('dashed')=='1' and s.get('endArrow')=='open','Actual native package dependency is dashed with open arrowhead')
    if kind=='dcd' and path.parent.name.startswith('UC-'):
        relations=[r for r in meta.get('dependencies',[]) if r.get('kind') not in ('dependency','generalization') and r.get('source_multiplicity') is not None]
        proofs=meta.get('association_end_labels',[])
        for relation in relations:
            matches=[p for p in proofs if all(p.get(n)==relation.get(n) for n in ('source','target','kind','role'))]
            name=key+':'+relation['source']+'->'+relation['target']+':'+relation.get('role','')
            canonical=[r for r in model.get('associations',[]) if all(r.get(n)==relation.get(n) for n in ('source','target','kind','role'))]
            if model:
                check('DCD_model_end_values',name,any(all(r.get(side+'_multiplicity')==relation.get(side+'_multiplicity') for side in ('source','target')) for r in canonical),'Both drawn end values agree with the sole canonical relationship')
            check('DCD_end_label_evidence',name,len(matches)==1,'Each association has one native edge and two separate end-label identities')
            if len(matches)!=1:continue
            proof=matches[0];edge=cells.get(proof.get('native_edge_id'));check('DCD_end_label_edge',name,edge is not None and edge.get('edge')=='1','Evidence resolves an actual editable edge')
            for side in ('source','target'):
                label=cells.get(proof.get(side+'_label_id'));point=proof.get(side+'_endpoint');box=rect(proof.get(side+'_label_id'))
                expected=relation[side+'_multiplicity']
                good=label is not None and text(label)==expected
                check('DCD_separate_end_label',name+':'+side,good,'Actual text cell contains only the multiplicity for this end: '+expected)
                valid=bool(point and len(point)==2 and box)
                if valid:
                    font=float(style(label).get('fontSize','18'));valid=point_to_rect(point,box)<=max(40,3*font)
                check('DCD_adjacent_end_label',name+':'+side,valid,'Actual end label is within three text heights of its attached endpoint')
                attached=False
                if edge is not None and point:
                    node_box=rect(edge.get(side))
                    if node_box:
                        x,y,w,h=node_box;px,py=point
                        attached=x-.75<=px<=x+w+.75 and y-.75<=py<=y+h+.75 and min(abs(px-x),abs(px-x-w),abs(py-y),abs(py-y-h))<=.75
                check('DCD_end_boundary',name+':'+side,attached,'Declared polyline endpoint touches the actual native source/target rectangle')
    if kind not in ('sequence','dao_sequence'):return
    messages=meta.get('messages',[])
    for i,message in enumerate(messages):
        edge_id=message.get('native_edge_id')
        if not edge_id:continue
        edge=cells.get(edge_id);mkind=message.get('kind','call');s=style(edge) if edge is not None else {}
        check('message_native_edge',key+':'+str(i),edge is not None and edge.get('edge')=='1','Message resolves an actual native edge')
        if mkind=='call':check('synchronous_call_arrow',key+':'+str(i),s.get('dashed','0')=='0' and s.get('endArrow') in ('block','classic') and s.get('endFill','1')=='1','Synchronous call has solid line and closed filled head')
        if mkind=='return':check('reply_arrow',key+':'+str(i),s.get('dashed')=='1' and s.get('endArrow')=='open','Reply is dashed with open head')
    for fragment in meta.get('interaction_fragments',[]):
        fid=fragment.get('id');box=rect(fid);operator=fragment.get('operator');indices=fragment.get('message_indices',[])
        check('interaction_fragment_native',key+':'+str(fid),box is not None and operator in ('alt','opt','break','loop','critical'),'Guarded region is an actual native fragment rectangle')
        check('interaction_fragment_nonempty',key+':'+str(fid),bool(indices) and bool(fragment.get('guard')),'A labelled branch contains actual guarded interaction messages')
        if box:
            expected=tuple(float(fragment.get(n,-1)) for n in ('x','y','w','h'))
            check('interaction_fragment_geometry',key+':'+str(fid),all(abs(a-b)<=.75 for a,b in zip(box,expected)),'Evidence matches actual native bounds')
            visible=[]
            for cid,cell in cells.items():
                bounds=rect(cid)
                if bounds and text(cell) and box[0]-.75<=bounds[0]<=box[0]+box[2]+.75 and box[1]-.75<=bounds[1]<=box[1]+box[3]+.75:visible.append(text(cell))
            normalize=lambda value:' '.join(re.findall(r'\w+',str(value).lower()))
            words=normalize(' '.join(visible));guard=normalize(fragment.get('guard',''))
            check('interaction_fragment_visible_guard',key+':'+str(fid),bool(guard) and guard in words and str(operator) in words,'Actual native text inside the fragment declares its operator and guard')
            for index in indices:
                message=messages[index] if isinstance(index,int) and 0<=index<len(messages) else None
                inside=False
                if message:
                    edge=cells.get(message.get('native_edge_id'));points=[]
                    if edge is not None:
                        g=edge.find('mxGeometry')
                        if g is not None:
                            points=[(float(p.get('x','0')),float(p.get('y','0'))) for p in g.findall('.//mxPoint')]
                    if not points and message.get('y') is not None:points=[(box[0]+box[2]/2,float(message['y']))]
                    inside=bool(points) and all(box[0]-.75<=x<=box[0]+box[2]+.75 and box[1]-.75<=y<=box[1]+box[3]+.75 for x,y in points)
                check('guarded_message_containment',key+':'+str(fid)+':'+str(index),inside,'Actual native waypoint/message path lies inside its guarded operand region')
    if kind=='sequence' and meta.get('op_id') in ('OP-07','OP-03','OP-06') and meta.get('UC') in ('UC-01','UC-05'):
        result={'OP-07':'cancelledOrderAndAmounts','OP-03':'rejectedOrder','OP-06':'rejectedOrderAndAmounts'}[meta['op_id']]
        check('SSD_success_result',key,any(m.get('kind')=='return' and result in ' '.join(str(m.get(n,'')) for n in ('method','arguments','label')) for m in messages),'Explicit dashed success return for frozen SSD outcome: '+result)
    # These renderer families were repaired for R1/R4. A missing proof must not
    # silently reduce the strengthened check to its former token-only scope.
    repaired=kind=='dao_sequence' or (kind=='sequence' and meta.get('UC') in ('UC-01','UC-05'))
    if repaired:
        check('repaired_message_edge_coverage',key,all(m.get('native_edge_id') for m in messages if m.get('kind','call')!='note'),'Every actual message in repaired sequence families identifies its native edge')
        if meta.get('operation') in ('confirmCheckout','acceptReplacement'):
            check('repaired_guard_geometry',key,bool(meta.get('interaction_fragments')),'Risk-focused checkout/replacement continuations retain explicit guarded-region evidence')
