"""Rebuild P1 process sources and exports. Own outputs only; no Part 1 imports.
Geometry adapts balanced-diagrams grid-wrap into lane grids; routes avoid nodes.
SVG and draw.io use the same explicit geometry (Part 1 proc_* convention).
"""
from pathlib import Path
import json, math, heapq, subprocess, hashlib, xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from PIL import ImageFont, Image

ROOT = Path(__file__).resolve().parent
W, H, FONT = 1100, 760, 16
BLUE, PALE, RED, GREY = '#004387', '#E7F0F6', '#B03A2E', '#DCDCDC'
AUTHOR = 'Author: 722I0004 · AI-assisted (Codex)'
EDGE = Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
F = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', FONT)
FB = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', FONT)
CHECKS = []

def grid_wrap_positions(order, ratio_target, pitch_x, pitch_y):
    """Adapted from balanced-diagrams/scripts/layout_drawio.py grid search."""
    cols = min(range(1, len(order)+1), key=lambda c: abs(math.log((c*pitch_x)/(math.ceil(len(order)/c)*pitch_y))-math.log(ratio_target)))
    return {nid: ((i%cols if i//cols%2==0 else cols-1-i%cols)*pitch_x, (i//cols)*pitch_y) for i,nid in enumerate(order)}

def txt(x, y, text, size=16, color=BLUE, bold=False, anchor='middle'):
    lines=text.split('\n'); lh=size+3
    y0=y-(len(lines)-1)*lh/2+size*.34
    return '<text x="%s" y="%s" text-anchor="%s" font-family="Arial, Helvetica, sans-serif" font-size="%s" fill="%s" font-weight="%s">%s</text>'%(x,y0,anchor,size,color,'bold' if bold else 'normal',''.join('<tspan x="%s" dy="%s">%s</tspan>'%(x,0 if i==0 else lh,escape(l)) for i,l in enumerate(lines)))

def rect(n, pad=0):
    return (n['x']-n['w']/2-pad,n['y']-n['h']/2-pad,n['x']+n['w']/2+pad,n['y']+n['h']/2+pad)

def overlaps(a,b):
    return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]

def port(n, side):
    return {'l':(n['x']-n['w']/2,n['y']),'r':(n['x']+n['w']/2,n['y']),'t':(n['x'],n['y']-n['h']/2),'b':(n['x'],n['y']+n['h']/2)}[side]

def route(a,b,ss,ds,nodes,occupied):
    dirs={'l':(-1,0),'r':(1,0),'t':(0,-1),'b':(0,1)}
    p,q=port(a,ss),port(b,ds); sd,td=dirs[ss],dirs[ds]
    start=(round((p[0]+sd[0]*20)/5),round((p[1]+sd[1]*20)/5))
    end=(round((q[0]+td[0]*20)/5),round((q[1]+td[1]*20)/5))
    blocks=[rect(n,8) for n in nodes.values() if n['kind']!='text']
    def blocked(c):
        x,y=c[0]*5,c[1]*5
        return any(r[0]<x<r[2] and r[1]<y<r[3] for r in blocks)
    queue=[(0,0,start,None)]; best={(start,None):0}; back={}; finish=None
    while queue:
        _,cost,c,d=heapq.heappop(queue)
        if c==end: finish=(c,d);break
        if cost>best.get((c,d),1e9):continue
        for nd,(dx,dy) in enumerate([(1,0),(0,1),(-1,0),(0,-1)]):
            nc=(c[0]+dx,c[1]+dy)
            if not(28<=nc[0]<=216 and 18<=nc[1]<=132) or blocked(nc):continue
            new=cost+1+(8 if d is not None and d!=nd else 0)+(3 if nc in occupied else 0)
            key=(nc,nd)
            if new<best.get(key,1e9):
                best[key]=new;back[key]=(c,d)
                h=abs(nc[0]-end[0])+abs(nc[1]-end[1])
                heapq.heappush(queue,(new+h,new,nc,nd))
    if finish is None: raise ValueError(('No route',a['id'],b['id']))
    path=[];cur=finish
    while cur in back:path.append((cur[0][0]*5,cur[0][1]*5));occupied.add(cur[0]);cur=back[cur]
    path.append((start[0]*5,start[1]*5));path.reverse();path=[p]+path+[q]
    out=[]
    for pt in path:
        if out and pt==out[-1]:continue
        while len(out)>1 and (out[-2][0]==out[-1][0]==pt[0] or out[-2][1]==out[-1][1]==pt[1]):out.pop()
        out.append(pt)
    return out

def label_rect(text,x,y):
    lines=text.split('\n');w=max(FB.getlength(l) for l in lines)+10;h=len(lines)*19+4
    return (x-w/2,y-h/2,x+w/2,y+h/2)

def label_hits_node(r,n):
    if n['kind'] not in ['decision','merge']:return overlaps(r,rect(n,3))
    # Separating-axis test against the actual diamond, not its bounding box.
    x,y,w,h=n['x'],n['y'],n['w']+6,n['h']+6
    a=[(r[0],r[1]),(r[2],r[1]),(r[2],r[3]),(r[0],r[3])]
    b=[(x,y-h/2),(x+w/2,y),(x,y+h/2),(x-w/2,y)]
    for poly in [a,b]:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            axis=(p[1]-q[1],q[0]-p[0]);aa=[v[0]*axis[0]+v[1]*axis[1] for v in a];bb=[v[0]*axis[0]+v[1]*axis[1] for v in b]
            if max(aa)<=min(bb) or max(bb)<=min(aa):return False
    return True

def place_label(e,nodes,labels,allroutes):
    segs=list(zip(e['pts'],e['pts'][1:]));segs.sort(key=lambda s: -(abs(s[1][0]-s[0][0])+abs(s[1][1]-s[0][1])))
    for a,b in segs:
        for t in [.5,.3,.7,.15,.85]:
            for off in [0,16,-16,28,-28,42,-42,60,-60,75,-75,100,-100,120,-120,140,-140]:
                x=a[0]+(b[0]-a[0])*t+(off if a[0]==b[0] else 0)
                y=a[1]+(b[1]-a[1])*t+(off if a[1]==b[1] else 0)
                rr=label_rect(e['label'],x,y)
                if rr[0]<140 or rr[2]>1090 or rr[1]<87 or rr[3]>630:continue
                if any(label_hits_node(rr,n) for n in nodes.values()):continue
                if any(overlaps(rr,r) for r in labels):continue
                # Text may not conceal any control-flow segment.
                if any(overlaps(rr,(min(p[0],q[0])-1,min(p[1],q[1])-1,max(p[0],q[0])+1,max(p[1],q[1])+1)) for pts in allroutes if pts is not e['pts'] for p,q in zip(pts,pts[1:])):continue
                labels.append(rr);return x,y,rr
    raise ValueError(('No label slot',e['src'],e['dst'],e['label']))

def shape_svg(n):
    x,y,w,h=n['x'],n['y'],n['w'],n['h'];k=n['kind'];c=RED if n.get('red') else BLUE
    fill=GREY if n.get('grey') else ('#FBEDEB' if n.get('red') else '#FFFFFF')
    common=f'fill="{fill}" stroke="{c}" stroke-width="2"'
    if k=='text':return txt(x,y,n['label'],FONT,c)
    if k in ['action','note']:s=f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="12" {common}/>'
    elif k in ['decision','merge']:s=f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" {common}/>'
    elif k=='start':return f'<circle cx="{x}" cy="{y}" r="{w/2}" fill="{BLUE}"/>'
    elif k=='final':return f'<circle cx="{x}" cy="{y}" r="{w/2}" fill="white" stroke="{BLUE}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{w/2-5}" fill="{BLUE}"/>'
    elif k=='flowfinal':return f'<circle cx="{x}" cy="{y}" r="{w/2}" fill="white" stroke="{BLUE}" stroke-width="2"/><path d="M{x-7},{y-7}L{x+7},{y+7}M{x-7},{y+7}L{x+7},{y-7}" stroke="{BLUE}" stroke-width="2"/>'
    elif k=='connector':s=f'<circle cx="{x}" cy="{y}" r="{w/2}" {common}/>'
    else:raise ValueError(k)
    return s+txt(x,y,n.get('label',''),FONT,'#1B1B1B',k=='connector')

def cell(root,id,value,style,x,y,w,h):
    c=ET.SubElement(root,'mxCell',id=id,value=value,style=style,vertex='1',parent='1')
    ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    return c

def build_page(p,base):
    nodes={n['id']:dict(n) for n in p['nodes']}
    if p.get('snake_order'):
        gp=grid_wrap_positions(p['snake_order'],1.3,230,145)
        for nid,(x,y) in gp.items():nodes[nid]['col'],nodes[nid]['row']=round(x/230),round(y/145)
    # Grid positions are deterministic: col/row for overview; lane/subrow for activities.
    for n in nodes.values():
        k=n['kind'];n.setdefault('w',180 if k=='action' else 170);n.setdefault('h',75 if k=='action' else 100)
        if k in ['start','final','flowfinal']:n['w']=n['h']=24
        if k=='merge':n['w']=n['h']=26
        if k=='connector':n['w']=n['h']=40
        n['x'],n['y']=p['xs'][n['col']],p['ys'][n['row']]
    for a,n in nodes.items():
        if n['kind']=='text':continue
        for b,m in nodes.items():
            if a<b and m['kind']!='text' and overlaps(rect(n),rect(m)):raise ValueError(('overlap',p['key'],a,b))
        label=n.get('label','');lines=label.split('\n')
        maxwidth=max(F.getlength(l) for l in lines)
        lim=n['w']*(.53 if n['kind']=='decision' else 1)-12
        if label and (maxwidth>lim or len(lines)*19>n['h']-8):raise ValueError(('text fit',p['key'],a,maxwidth,lim))
    edges=p['edges'];occupied=set()
    for e in edges:
        e['pts']=route(nodes[e['src']],nodes[e['dst']],e.get('ss','r'),e.get('ds','l'),nodes,occupied)
    edge_node_errors=[]
    for e in edges:
        for a,b in zip(e['pts'],e['pts'][1:]):
            rr=(min(a[0],b[0])-.1,min(a[1],b[1])-.1,max(a[0],b[0])+.1,max(a[1],b[1])+.1)
            for nid,n in nodes.items():
                if nid not in [e['src'],e['dst']] and n['kind']!='text' and overlaps(rr,rect(n,-.2)):
                    edge_node_errors.append((e['src'],e['dst'],nid))
    if edge_node_errors:raise ValueError(('edge through node',p['key'],edge_node_errors))
    labels=[]
    for e in edges:
        if e.get('label'):e['labelpos']=place_label(e,nodes,labels,[e2['pts'] for e2 in edges])
    if p.get('semantic'):
        inc={n:[] for n in nodes};out={n:[] for n in nodes}
        for e in edges:inc[e['dst']].append(e);out[e['src']].append(e)
        for nid,n in nodes.items():
            k=n['kind'];i,o=len(inc[nid]),len(out[nid])
            if k in ['action','decision'] and i!=1:raise ValueError(('incoming',p['key'],nid,i))
            if k=='decision' and (o<2 or any(not e.get('label','').startswith('[') for e in out[nid])):raise ValueError(('guards',nid))
            if k=='merge' and(i<2 or o!=1):raise ValueError(('merge',nid,i,o))
            if k in ['final','flowfinal'] and(i<1 or o):raise ValueError(('final',nid))
            if k=='start' and(i or o!=1):raise ValueError(('initial',nid))
    model=ET.Element('mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H),grid='1',gridSize='5',guides='1',math='0',shadow='0')
    root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#004387"/></marker><marker id="redarrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#B03A2E"/></marker></defs>',f'<rect width="{W}" height="{H}" fill="white"/>']
    def textitem(id,text,x,y,w,h,size=16,bold=False):
        cell(root,id,text,f'text;html=0;whiteSpace=wrap;align=left;verticalAlign=middle;strokeColor=none;fillColor=none;fontSize={size};fontColor={BLUE};fontStyle={1 if bold else 0};',x,y,w,h)
        svg.append(txt(x,y+h/2,text,size,BLUE,bold,'start'))
    textitem('title',p['title'],20,12,1060,28,22,True)
    textitem('sub',p['subtitle'],20,45,1060,30,16)
    for i,l in enumerate(p.get('lanes',[])):
        y0,y1,name=l
        svg.append(f'<rect x="15" y="{y0}" width="1070" height="{y1-y0}" fill="{PALE}" stroke="{BLUE}" stroke-width="1"/><rect x="15" y="{y0}" width="115" height="{y1-y0}" fill="{BLUE}"/>'+txt(72.5,(y0+y1)/2,name,16,'white',True))
        cell(root,f'lane{i}','',f'rounded=0;fillColor={PALE};strokeColor={BLUE};',15,y0,1070,y1-y0)
        cell(root,f'head{i}',name,f'rounded=0;html=0;whiteSpace=wrap;fillColor={BLUE};strokeColor={BLUE};fontColor=#FFFFFF;fontSize=16;fontStyle=1;',15,y0,115,y1-y0)
    for i,e in enumerate(edges):
        red=e.get('red');color=RED if red else BLUE;pts=e['pts'];ss=e.get('ss','r');ds=e.get('ds','l')
        ports={'l':(0,.5),'r':(1,.5),'t':(.5,0),'b':(.5,1)};sp,tp=ports[ss],ports[ds]
        style=f'edgeStyle=none;html=0;rounded=0;strokeColor={color};strokeWidth=2;endArrow=block;endFill=1;exitX={sp[0]};exitY={sp[1]};entryX={tp[0]};entryY={tp[1]};'
        c=ET.SubElement(root,'mxCell',id=f'e{i}',value='',style=style,edge='1',parent='1',source=e['src'],target=e['dst']);g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        arr=ET.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in pts[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        svg.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" marker-end="url(#%s)"/>'%(' '.join(f'{x},{y}' for x,y in pts),color,'redarrow' if red else 'arrow'))
    for nid,n in nodes.items():
        k=n['kind'];fill=GREY if n.get('grey') else ('#FBEDEB' if n.get('red') else '#FFFFFF');color=RED if n.get('red') else BLUE
        st={'action':'rounded=1;arcSize=20;','note':'rounded=1;','decision':'rhombus;','merge':'rhombus;','start':'ellipse;','final':'ellipse;shape=endState;','flowfinal':'shape=sumEllipse;','connector':'ellipse;','text':'text;strokeColor=none;fillColor=none;'}[k]
        if k in ['start','final']:fill=BLUE
        style=st+f'html=0;whiteSpace=wrap;fillColor={fill};strokeColor={color};strokeWidth=2;fontSize={FONT};fontColor=#1B1B1B;'
        cell(root,nid,n.get('label',''),style,*rect(n)[:2],n['w'],n['h']);svg.append(shape_svg(n))
    for i,e in enumerate(edges):
        if e.get('label'):
            x,y,rr=e['labelpos'];label=e['label'];color=RED if e.get('red') else BLUE
            cell(root,f'label{i}',label,f'text;html=0;whiteSpace=wrap;align=center;verticalAlign=middle;fillColor=#FFFFFF;strokeColor=none;fontSize=16;fontColor={color};fontStyle=1;',rr[0],rr[1],rr[2]-rr[0],rr[3]-rr[1])
            svg.append(f'<rect x="{rr[0]}" y="{rr[1]}" width="{rr[2]-rr[0]}" height="{rr[3]-rr[1]}" fill="white"/>'+txt(x,y,label,16,color,True))
    for j,line in enumerate(p.get('notes',[])):textitem(f'note{j}',line,145,642+j*20,925,20)
    textitem('author',AUTHOR,20,705,1060,20)
    textitem('legend','Blue/white: Part 2 scope · Red: exception · Grey: deferred, not built (L3 / A-09)',20,731,1060,20)
    svg.append('</svg>');svgpath=ROOT/f'{base}{p["suffix"]}.svg';svgpath.write_text(''.join(svg),encoding='utf-8')
    xmlpath=ROOT/f'{base}{p["suffix"]}.drawio';mx=ET.Element('mxfile',host='SaigonBite P1',version='24.7.17');d=ET.SubElement(mx,'diagram',id=p['key'],name=p['title']);d.append(model);ET.ElementTree(mx).write(xmlpath,encoding='utf-8',xml_declaration=True)
    CHECKS.append({'file':svgpath.name,'nodes':len(nodes),'edges':len(edges),'semantic_checked':bool(p.get('semantic')),'canvas':[W,H],'min_font_px':16,'placed_A4_landscape_230_mm_wide_min_pt':round(16*230/25.4*72/W,2),'node_overlap':0,'text_fit':0,'label_overlap':0,'edge_through_unrelated_node':0})
    return d,svgpath

def main():
    for base in ['business_process_v2','swimlane_v2']:
        spec=json.loads((ROOT/f'{base}.json').read_text(encoding='utf-8'));bundle=ET.Element('mxfile',host='SaigonBite P1',version='24.7.17')
        if base=='business_process_v2':bundle.set('sourcePart1SHA256',hashlib.sha256(Path('D:/RAD/FINAL/Part1_v2/models/SaigonBite_Business_Process.drawio').read_bytes()).hexdigest())
        for p in spec['pages']:
            d,svg=build_page(p,base);bundle.append(d)
            png=svg.with_suffix('.png');profile=Path('D:/RAD/FINAL/Part2/notes/P1_diagram_browser_profile')
            run=subprocess.run([str(EDGE),'--headless','--disable-gpu','--hide-scrollbars','--no-first-run','--force-device-scale-factor=2',f'--user-data-dir={profile}',f'--screenshot={png}','--window-size=1100,760',svg.as_uri()],capture_output=True,text=True,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
            if run.returncode or not png.exists():raise RuntimeError(run.stderr)
            im=Image.open(png);print(svg.name,im.size)
        ET.ElementTree(bundle).write(ROOT/f'{base}.drawio',encoding='utf-8',xml_declaration=True)
    (ROOT/'business_process_v2.qa.json').write_text(json.dumps(CHECKS,indent=2),encoding='utf-8')

if __name__=='__main__':main()
