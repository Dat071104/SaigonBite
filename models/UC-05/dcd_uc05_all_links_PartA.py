"""Standalone P3-A renderer. Author: 722I0004 · AI-assisted (Codex).
Input JSON is beside this generator. Pure document generation; no app imports.
Geometry follows the immutable P2 PIL/SVG/mxGraph pipeline and balanced-diagrams.
"""
from pathlib import Path
import sys,json,math,re,hashlib,xml.etree.ElementTree as ET
from html import escape
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
W,H=1600,1200
INK,BLUE='#202B36','#004387'
def font(n=24,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
def wrap(s,width,n=24):
    out=[]
    for ln in str(s).split('\n'):
        cur=''
        words=[]
        for token in ln.split():
            while font(n).getlength(token)>width:
                k=len(token)-1
                while k>1 and font(n).getlength(token[:k])>width:k-=1
                words.append(token[:k]);token=token[k:]
            words.append(token)
        for word in words:
            if font(n).getlength((cur+' '+word).strip())>width and cur:out.append(cur);cur=word
            else:cur=(cur+' '+word).strip()
        out.append(cur)
    return out
def refresh_from_shared(spec,input_path):
    """Status/signature authority is the reviewed shared model, never name matching.
    Refresh only this plate. Geometry/branches and exact SSD arguments are retained.
    New members/associations require the owned lane-refresh step, not invention here.
    """
    modelpath=Path(input_path).parents[1]/'shared/design_model.json'
    model=json.loads(modelpath.read_text(encoding='utf-8'));classes=model['classes'];phase=spec['phase3']
    def meth(cl,name):return next(x for x in classes[cl]['methods'] if x['name']==name)
    def marker(x):return '†' if x.get('status') in ['P4-TARGET','GAP'] else ''
    def signature(cl,name):
        x=meth(cl,name);s=x['signature']
        if '->' not in s:s+=' -> '+x.get('return','Any')+' [inferred return]'
        return x.get('visibility','+')+' '+s+marker(x)+(' {property; read as .'+name+'}' if 'property' in (x.get('decorators') or []) else '')
    p4=set()
    severity={'MATCH':0,'P4-TARGET':1,'GAP':2}
    for index,edge in enumerate(phase.get('dependencies',[])):
        candidates=[x for x in model['associations']+model['dependencies'] if (x['source'],x['target'],x['kind'])==(edge['source'],edge['target'],edge['kind']) and x.get('allowed_on_layered_diagram',True)]
        assert candidates,(spec['stem'],'selected relation is absent/disallowed; run the owned lane refresh')
        current=max(candidates,key=lambda x:severity.get(x.get('status','MATCH'),0));edge.update(current)
        if marker(current):p4.update(x.strip() for x in current.get('P4_input','').split(';') if x.strip())
        if index<len(spec.get('edges',[])):
            spec['edges'][index]['label']=spec['edges'][index]['label'].rstrip('†')+marker(current)
    for e in phase.get('elements',[]):
        for name in e.get('methods',[]):
            x=meth(e['class'],name)
            if marker(x):p4.update(v.strip() for v in x.get('P4_input','').split(';') if v.strip())
    if phase['diagram_type']=='dcd':
        for card in spec.get('cards',[]):
            if len(card['compartments'])<3:continue
            e=card['element'];cl=e['class'];attributes={a['name']:a for a in classes[cl]['attributes']}
            values=[]
            for name in e['attributes']:
                a=attributes[name];values.append(a.get('visibility','+')+' '+name+': '+a['type']+(' [inferred]' if a.get('inferred') else ''))
            if classes[cl].get('enum_members'):values=['+ '+str(v['name'] if isinstance(v,dict) else v) for v in classes[cl]['enum_members']]
            card['compartments'][1]=values or [('{attributes in preceding card}' if '{attributes in preceding card}' in card['compartments'][1] else '{no selected attribute}')]
            card['compartments'][2]=[signature(cl,n) for n in e['methods']] or ['{no selected operation}']
            card['box'][3]=20+sum(sum(len(wrap(t,686))*27.6 for t in comp)+10 for comp in card['compartments'])
        for x in sorted({card['box'][0] for card in spec.get('cards',[]) if len(card['compartments'])>=3}):
            y=100
            for card in sorted([card for card in spec['cards'] if card['box'][0]==x and len(card['compartments'])>=3],key=lambda card:card['box'][1]):
                card['box'][1]=y;y+=card['box'][3]+18
            assert y-18<=1058,(spec['stem'],'refreshed members need a new split')
    else:
        lf={l['id']:l for l in phase['lifelines']}
        for message in phase['messages']:
            if message['kind'] not in ['call','ssd']:continue
            cl=lf[message['to']]['class'];name=message['method'];x=meth(cl,name)
            if name=='fingerprint':
                message['argument_bindings']={'payment_method':'payment.method','online_option':'payment.option'}
                parameters=[p['name'] for p in x['parameters'] if p['name'] not in ['self','cls']]
                if set(parameters)<=set(message['argument_bindings']):
                    message['arguments']=', '.join(message['argument_bindings'][p] for p in parameters)
                    message['label']=re.sub(r'fingerprint†?\([^)]*\)','fingerprint'+marker(x)+'('+message['arguments']+')',message['label'])
            elif message['kind']=='call':
                message['label']=re.sub(r'(?<![A-Za-z0-9_])'+re.escape(name)+r'†?(?=\()',name+marker(x),message['label'])
            elif message['kind']=='ssd':
                adapter=cl+'.'+name
                message['label']=re.sub(re.escape(adapter)+r'†?(?=\s*\[HTTP)',adapter+marker(x),message['label'])
            message['receiver_signature']=x['signature'];message['status']=x['status'];message['P4_input']=x.get('P4_input','')
        # A longer reviewed signature/binding must not put the next label on a
        # self-call return loop. Preserve the existing branch frames and padding.
        xs={l['id']:90+i*(1420/max(1,len(phase['lifelines'])-1)) for i,l in enumerate(phase['lifelines'])}
        messages=phase['messages']
        for i,message in enumerate(messages[1:],1):
            previous=messages[i-1]
            if previous['from']!=previous['to'] or message['kind']=='return':continue
            width=max(420,abs(xs[message['from']]-xs[message['to']])-30)
            top=message['y']-8-len(wrap(message['label'],width))*27.6
            needed=math.ceil(previous['y']+32-top)
            if needed>0:
                for later in messages[i:]:
                    if later['kind']!='return' or not later.get('guard'):later['y']+=needed
        for frame in spec.get('frames',[]):
            if frame.get('operands'):
                last=max(x['y']+25 for x in messages if x['kind'] not in ['return','ssd'])
                assert last<=frame['operands'][0][0],(spec['stem'],'longer reviewed label needs a new split')
        row=next(x for x in model['operation_rows'] if x['UC']==spec['UC'] and x['operation']==phase['operation'])
        p4.update(v.strip() for v in row['P4 input'].split(';') if v.strip())
        for message in phase['messages']:
            if message['from']=='view' and message['to']=='ctrl':message['PC_MG']=row['PC/MG ensured']
        # A behavior target clears only after explicit reviewed model/row statuses.
        if row['status']=='MATCH' and all(message.get('status','MATCH')=='MATCH' for message in phase['messages']):
            for note in spec.get('notes',[]):note['text']=note['text'].replace('†','')
            spec['realisation_note']=spec.get('realisation_note','').replace('†','')
    spec['P4_input']='; '.join(sorted(p4)) or 'none on this view'
    spec['shared_model_source']='models/shared/design_model.json';spec['shared_model_sha256']=hashlib.sha256(modelpath.read_bytes()).hexdigest()
    spec['refresh_policy']='Explicit shared-model statuses only; matching signatures never clear behavioral targets.'
    return spec
class Canvas:
    def __init__(self,spec):
        self.s=spec;self.im=Image.new('RGB',(W,H),'white');self.d=ImageDraw.Draw(self.im);self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>'];self.mx=ET.Element('mxfile',host='SaigonBite P3-A',type='device');dia=ET.SubElement(self.mx,'diagram',name=spec['title'],id=spec['stem']);mod=ET.SubElement(dia,'mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H));self.root=ET.SubElement(mod,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0');self.i=0;self.bounds=[]
        self.text(35,16,spec['title'],1530,28,True)
    def vertex(self,id,x,y,w,h,label='',style=''):
        c=ET.SubElement(self.root,'mxCell',id=id,value=label,vertex='1',parent='1',style=style+'fontFamily=Arial;fontSize=24;whiteSpace=wrap;html=0;');ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    def text(self,x,y,s,w,n=24,b=False):
        lines=wrap(s,w,n);lh=n*1.15
        for j,ln in enumerate(lines):
            yy=y+j*lh;self.d.text((x,yy),ln,font=font(n,b),fill=INK);self.svg.append(f'<text x="{x}" y="{yy+n*.93}" font-family="Arial" font-size="{n}" font-weight="{"bold" if b else "normal"}" fill="{INK}">{escape(ln)}</text>')
            assert font(n,b).getlength(ln)<=w+2,(self.s['stem'],ln,w)
        self.vertex('text'+str(self.i),x,y,w,max(lh,len(lines)*lh),'\n'.join(lines),'text;align=left;verticalAlign=top;strokeColor=none;fillColor=none;');self.i+=1
        assert y+len(lines)*lh<=1202,(self.s['stem'],s,y)
        return len(lines)*lh
    def rect(self,x,y,w,h,fill='white',id=None,style=''):
        self.d.rectangle((x,y,x+w,y+h),fill=fill,outline=BLUE,width=2);self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{BLUE}" stroke-width="2"/>');self.vertex(id or 'rect'+str(self.i),x,y,w,h,'','fillColor='+fill+';strokeColor='+BLUE+';'+style);self.i+=1
    def line(self,pts,dash=False,arrow=False,source=None,target=None,kind='dependency'):
        for a,b in zip(pts,pts[1:]):
            if dash:
                l=math.dist(a,b);n=max(1,int(l/9))
                for k in range(0,n,2):self.d.line((a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n,a[0]+(b[0]-a[0])*min(k+1,n)/n,a[1]+(b[1]-a[1])*min(k+1,n)/n),fill=BLUE,width=2)
            else:self.d.line([a,b],fill=BLUE,width=2)
        self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="'+BLUE+'" stroke-width="2"'+(' stroke-dasharray="8 7"' if dash else '')+'/>')
        if arrow:
            a,b=pts[-2:];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l;p=[(b[0]-ux*14-uy*7,b[1]-uy*14+ux*7),b,(b[0]-ux*14+uy*7,b[1]-uy*14-ux*7)];self.d.line(p,fill=BLUE,width=2);self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in p)+'" fill="none" stroke="'+BLUE+'" stroke-width="2"/>')
            if kind=='generalization':
                self.d.polygon(p,fill='white',outline=BLUE,width=2);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+'" fill="white" stroke="'+BLUE+'"/>')
            if kind=='composition':
                a,b=pts[:2];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l;p=[a,(a[0]+ux*12-uy*7,a[1]+uy*12+ux*7),(a[0]+ux*24,a[1]+uy*24),(a[0]+ux*12+uy*7,a[1]+uy*12-ux*7)];self.d.polygon(p,fill=BLUE);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+'" fill="'+BLUE+'"/>')
        if source and target:
            c=ET.SubElement(self.root,'mxCell',id='edge'+str(self.i),source=source,target=target,edge='1',parent='1',style='edgeStyle=none;endArrow='+('block' if kind=='generalization' else 'open')+';'+('dashed=1;' if dash else '')+('startArrow=diamond;startFill=1;' if kind=='composition' else '')+'strokeColor='+BLUE+';');g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});arr=ET.SubElement(g,'Array',attrib={'as':'points'})
            for x,y in pts[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
            self.i+=1
    def finish(self,out):
        self.text(35,1080,self.s.get('continuation','Single complete operation view.'),1530)
        self.text(35,1112,'† design target, not yet in code at C0 (see P4 input '+self.s.get('P4_input','none on this view')+').',1530)
        self.text(35,1145,'Figure '+self.s['figure']+'. '+self.s.get('caption',self.s['title'])+' — Author: 722I0004 · AI-assisted (Codex)',1530)
        self.text(35,1171,'Static / target design · 230 mm landscape · smallest text 9.78 pt · native draw.io / final placement UNTESTED',1530)
        self.svg.append('</svg>');out.with_suffix('.svg').write_text('\n'.join(self.svg),encoding='utf-8');self.im.save(out.with_suffix('.png'));ET.indent(self.mx);ET.ElementTree(self.mx).write(out.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
        for q in [out.with_suffix('.svg'),out.with_suffix('.drawio')]:ET.parse(q)
        ids={c.get('id') for c in self.root.findall('mxCell')}
        for c in self.root.findall('mxCell'):
            if c.get('edge')=='1':assert c.get('source') in ids and c.get('target') in ids
def render(spec,out):
    c=Canvas(spec)
    if spec['phase3']['diagram_type']=='dcd':
        for card in spec.get('cards',[]):
            x,y,w,h=card['box'];c.rect(x,y,w,h,'#F1F6FA',card['id']);yy=y+8
            for i,comp in enumerate(card['compartments']):
                if i:c.line([(x,yy-4),(x+w,yy-4)])
                yy+=c.text(x+12,yy,'\n'.join(comp),w-24,24,i==0)+10
            assert yy<y+h+3,(spec['stem'],card['id'],yy,y+h)
        for e in spec.get('edges',[]):
            c.line(e['points'],e['kind']=='dependency',True,e['source'],e['target'],e['kind']);c.text(*e['labelpos'],e['label'],e.get('labelwidth',1000))
        for n in spec.get('notes',[]):c.text(n['x'],n['y'],n['text'],n['w'])
    else:
        lines=spec['phase3']['lifelines'];xs={n['id']:90+i*(1420/max(1,len(lines)-1)) for i,n in enumerate(lines)}
        for n in lines:
            x=xs[n['id']];c.rect(x-85,76,170,94,'#F1F6FA',n['id']);c.text(x-80,82,n.get('label',n['class']),160);c.line([(x,170),(x,1060)],True)
        for f in spec.get('frames',[]):
            c.rect(30,f['y'],1540,f['h'],'white',f['id'],'shape=umlFrame;fillColor=none;')
            # Redraw lifelines over the transparent combined fragment.
            for x in xs.values():c.line([(x,f['y']),(x,f['y']+f['h'])],True)
            c.text(40,f['y']+3,f['label'],1520,24,True)
            for yy,label in f.get('operands',[]):
                c.line([(30,yy),(1570,yy)],True);c.text(40,yy+3,label,1520,24,True)
        for n in spec.get('notes',[]):
            c.rect(35,n['y'],1530,n.get('h',80),'#FFF8E9');c.text(45,n['y']+5,n['text'],1510)
        for msg in spec['phase3']['messages']:
            if msg['kind']=='note':continue
            a,b=xs[msg['from']],xs[msg['to']];y=msg['y'];label=msg['label'];ls=wrap(label,max(420,abs(b-a)-30),24);labelw=max(420,abs(b-a)-30);lx=max(40,min(a,b)+15)
            if a==b:
                pts=[(a,y),(a+45,y),(a+45,y+25),(a,y+25)];lx=max(40,min(a-370,1100));labelw=450
            else:pts=[(a,y),(b,y)]
            c.line(pts,msg['kind']=='return',True,msg['from'],msg['to']);c.text(lx,y-8-len(wrap(label,labelw))*27.6,label,labelw)
            if msg['kind'] not in ['return','ssd']:
                c.rect(b-5,y,10,25,'#DAE9F5')
    c.finish(out)
if __name__=='__main__':
    inp=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.json')
    spec=refresh_from_shared(json.loads(inp.read_text(encoding='utf-8')),inp)
    inp.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    render(spec,inp.with_suffix(''))
