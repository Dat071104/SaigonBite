"""Deterministic Part 2 state diagram renderer; JSON -> draw.io / SVG / PNG.

Reuses the P1 proc_* / business_process_v2 pipeline convention: one explicit
geometry, Arial measurement, editable mxGraph cells, SVG, hidden Edge export.
No P1 imports or writes. Invoke with no args for Order, or a JSON path.
"""
from pathlib import Path
import sys, json, subprocess, hashlib, xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from PIL import Image, ImageFont

sys.dont_write_bytecode = True
W, H, FONT = 1100, 760, 16
BLUE, RED, INK = '#004387', '#B03A2E', '#1B1B1B'
SCRATCH = Path('D:/RAD/FINAL/Part2/notes/P2-C')
EDGE = Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
F = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', FONT)
FB = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', FONT)
AUTHOR = 'Author: 722I0004 · AI-assisted (Codex)'

def text(x, y, value, size=FONT, color=INK, bold=False, anchor='middle'):
    lines = value.split('\n'); lh = size + 4
    y0 = y - (len(lines)-1)*lh/2 + size*.34
    return f'<text x="{x}" y="{y0}" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" font-weight="{"bold" if bold else "normal"}">' + ''.join(f'<tspan x="{x}" dy="{0 if i==0 else lh}">{escape(s)}</tspan>' for i,s in enumerate(lines)) + '</text>'

def bounds(n):
    return (n['x']-n['w']/2,n['y']-n['h']/2,n['x']+n['w']/2,n['y']+n['h']/2)

def overlap(a,b):
    return a[0]<b[2]-.5 and a[2]>b[0]+.5 and a[1]<b[3]-.5 and a[3]>b[1]+.5

def vertex(root, ident, label, style, box):
    x,y,w,h=box
    c=ET.SubElement(root,'mxCell',id=ident,value=label,style=style,vertex='1',parent='1')
    ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})

def render(p, target):
    nodes={n['id']:n for n in p['nodes']}; errors=[]
    for ident,n in nodes.items():
        for other,m in nodes.items():
            if ident<other and overlap(bounds(n),bounds(m)):errors.append(f'node overlap {ident}/{other}')
        incoming=sum(e['dst']==ident for e in p['edges']);outgoing=sum(e['src']==ident for e in p['edges'])
        if n.get('kind')=='initial' and (incoming or outgoing!=1):errors.append(f'initial degree {ident}')
        if n.get('kind')=='final' and outgoing:errors.append(f'final outgoing {ident}')
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#004387"/></marker></defs>',f'<rect width="{W}" height="{H}" fill="white"/>']
    model=ET.Element('mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H),grid='1',gridSize='10')
    root=ET.SubElement(model,'root'); ET.SubElement(root,'mxCell',id='0'); ET.SubElement(root,'mxCell',id='1',parent='0')
    def item(ident,label,box,size=FONT,bold=False,color=INK,fill='none'):
        x,y,w,h=box
        font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',size)
        if max(font.getlength(s) for s in label.split('\n'))>w-4 or len(label.split('\n'))*(size+4)>h+1: errors.append(f'text overflow {ident}')
        vertex(root,ident,label,f'text;html=0;whiteSpace=wrap;align=center;verticalAlign=middle;fillColor={fill};strokeColor=none;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};',box)
        if fill!='none':svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
        svg.append(text(x+w/2,y+h/2,label,size,color,bold))
    item('title',p['title'],[20,10,1060,36],22,True,BLUE)
    item('subtitle',p['subtitle'],[20,48,1060,28],16,False,BLUE)
    # Arcs precede states; source/target IDs remain native editable references.
    for i,e in enumerate(p['edges']):
        if e['src'] not in nodes or e['dst'] not in nodes:errors.append(f'unconnected edge {i}'); continue
        pts=e['points']; style='edgeStyle=none;rounded=0;html=0;strokeColor=#004387;strokeWidth=2;endArrow=block;endFill=1;'
        sn,tn=nodes[e['src']],nodes[e['dst']]
        for prefix,node,pt in [('exit',sn,pts[0]),('entry',tn,pts[-1])]:
            xx=(pt[0]-(node['x']-node['w']/2))/node['w']; yy=(pt[1]-(node['y']-node['h']/2))/node['h']
            style+=f'{prefix}X={xx};{prefix}Y={yy};{prefix}Perimeter=0;'
        if e.get('dashed'):style+='dashed=1;'
        c=ET.SubElement(root,'mxCell',id=f'e{i}',value='',style=style,edge='1',parent='1',source=e['src'],target=e['dst'])
        g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});arr=ET.SubElement(g,'Array',attrib={'as':'points'})
        ET.SubElement(g,'mxPoint',x=str(pts[0][0]),y=str(pts[0][1]),attrib={'as':'sourcePoint'})
        ET.SubElement(g,'mxPoint',x=str(pts[-1][0]),y=str(pts[-1][1]),attrib={'as':'targetPoint'})
        for x,y in pts[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        svg.append('<polyline points="%s" fill="none" stroke="#004387" stroke-width="2" marker-end="url(#a)" %s/>'%(' '.join(f'{x},{y}' for x,y in pts),'stroke-dasharray="6 4"' if e.get('dashed') else ''))
        for a,b in zip(pts,pts[1:]):
            if a[0]!=b[0] and a[1]!=b[1]:errors.append(f'nonorthogonal edge {i}')
            for nid,n in nodes.items():
                if nid in [e['src'],e['dst']]:continue
                if overlap((min(a[0],b[0])-.1,min(a[1],b[1])-.1,max(a[0],b[0])+.1,max(a[1],b[1])+.1),bounds(n)):errors.append(f'edge {i} intersects {nid}')
    for nid,n in nodes.items():
        k=n.get('kind','state');x,y,w,h=n['x'],n['y'],n['w'],n['h'];x0,y0,_,_=bounds(n)
        grey=n.get('grey',False);fill='#DCDCDC' if grey else ('#FFFBE6' if k=='note' else '#FFFFFF')
        if k in ['initial','final']:
            style='ellipse;' if k=='initial' else 'shape=endState;'
            vertex(root,nid,'',style+f'fillColor={BLUE};strokeColor={BLUE};', [x0,y0,w,h])
            svg.append(f'<circle cx="{x}" cy="{y}" r="{w/2}" fill="{"white" if k=="final" else BLUE}" stroke="{BLUE}" stroke-width="2"/>')
            if k=='final':svg.append(f'<circle cx="{x}" cy="{y}" r="{w/2-5}" fill="{BLUE}"/>')
        elif k=='choice':
            vertex(root,nid,'','rhombus;fillColor=#FFFFFF;strokeColor=#004387;strokeWidth=2;',[x0,y0,w,h])
            svg.append(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" fill="white" stroke="{BLUE}" stroke-width="2"/>')
        else:
            style=('shape=note;size=15;' if k=='note' else 'rounded=1;arcSize=20;')+f'html=0;whiteSpace=wrap;fillColor={fill};strokeColor={BLUE};strokeWidth=2;fontSize={FONT};fontColor={INK};'
            vertex(root,nid,n['label'],style,[x0,y0,w,h])
            svg.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="{0 if k=="note" else 14}" fill="{fill}" stroke="{BLUE}" stroke-width="2"/>'+text(x,y,n['label']))
            if max(F.getlength(s) for s in n['label'].split('\n'))>w-12 or len(n['label'].split('\n'))*20>h-8:errors.append(f'node text overflow {nid}')
    boxes=[]
    for i,e in enumerate(p['edges']):
        if not e.get('label'):continue
        b=e['label_box'];r=(b[0],b[1],b[0]+b[2],b[1]+b[3])
        for nid,n in nodes.items():
            if overlap(r,bounds(n)):errors.append(f'label {i} intersects node {nid}')
        for j,rr in boxes:
            if overlap(r,rr):errors.append(f'label {i} intersects label {j}')
        for j,other in enumerate(p['edges']):
            for a,q in zip(other['points'],other['points'][1:]):
                if overlap(r,(min(a[0],q[0])-.2,min(a[1],q[1])-.2,max(a[0],q[0])+.2,max(a[1],q[1])+.2)):
                    errors.append(f'label {i} masks edge {j}')
        boxes.append((i,r));item(f'label{i}',e['label'],b,16,True,BLUE,'white')
    item('notes','\n'.join(p.get('notes',[])),[20,638,1060,60],16,False,INK)
    item('author',AUTHOR,[20,704,1060,24],16,True,BLUE)
    item('legend','Filled dot: initial · Bullseye: final · Grey: future/unreachable · Labels: event [guard] / effect',[20,730,1060,24],16,False,BLUE)
    if errors:raise ValueError((target.name,errors))
    svg.append('</svg>');target.with_suffix('.svg').write_text(''.join(svg),encoding='utf-8')
    mx=ET.Element('mxfile',host='SaigonBite P2',version='24.7.17'); d=ET.SubElement(mx,'diagram',id=p['key'],name=p['title']);d.append(model)
    ET.ElementTree(mx).write(target.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
    run=subprocess.run([str(EDGE),'--headless','--disable-gpu','--hide-scrollbars','--no-first-run','--force-device-scale-factor=2',f'--user-data-dir={SCRATCH/("edge_"+target.stem)}',f'--screenshot={target.with_suffix(".png")}','--window-size=1100,760',target.with_suffix('.svg').as_uri()],capture_output=True,text=True,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    if run.returncode or not target.with_suffix('.png').exists():raise RuntimeError(run.stderr)
    return {'file':str(target),'states':[n.get('label','') for n in nodes.values() if n.get('kind','state')=='state'],'edges':len(p['edges']),'canvas':[W,H],'minimum_font_px':16,'placed_width_mm':230,'minimum_pt':round(16*230/25.4*72/W,2),'png_size':Image.open(target.with_suffix('.png')).size,'checks':'XML; connected edge IDs; text fits; node/label overlaps; orthogonal routes'}

def build(spec_path):
    SCRATCH.mkdir(parents=True,exist_ok=True)
    spec_path=Path(spec_path);data=json.loads(spec_path.read_text(encoding='utf-8'))
    log=[]
    for p in data['pages']:
        target=spec_path.parent/p['stem']; log.append(render(p,target))
    (SCRATCH/(spec_path.stem+'_qa.json')).write_text(json.dumps(log,indent=2),encoding='utf-8')
    print(json.dumps(log,ensure_ascii=False))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.json'))
