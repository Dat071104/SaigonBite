from pathlib import Path
import json
import math
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

BLUE="#004387"; INK="#1B1B1B"; RED="#B03A2E"; PALE="#EAF1F8"; NOTE="#FFF8DB"; GREY="#6A6A6A"; WHITE="#FFFFFF"
FONT_REG="C:/Windows/Fonts/arial.ttf"; FONT_BOLD="C:/Windows/Fonts/arialbd.ttf"


def refresh_from_shared_model(spec,path):
    # Re-runnable static refresh. The sole reviewed model controls status; a matching
    # signature never clears a behavioral target on its own. No app is imported.
    import hashlib,re,textwrap
    modelpath=path.parent.parent/'shared'/'design_model.json'
    if not modelpath.exists():
        return spec  # Standalone adjacent-JSON reproduction remains supported.
    model=json.loads(modelpath.read_text(encoding='utf-8')); classes=model['classes']
    phase=spec['phase3']; nodes={n['id']:n for n in spec.get('nodes',[])}; FS=spec['canvas']['font_size']
    def mark(m):return ' †' if m.get('status') in ('P4-TARGET','GAP') else ''
    def wrap(t,w):
        limit=max(18,int((w-48)/(FS*.56)))
        pieces=[]
        for token in t.split():
            while len(token)>limit:
                cut=max(token.rfind(ch,1,limit+1) for ch in ('_', '.', '/', ':', '-'))
                cut=limit if cut<1 else cut+1
                pieces.append(token[:cut]);token=token[cut:]
            if token:pieces.append(token)
        lines=[];current=''
        for part in pieces:
            if current and len(current)+1+len(part)>limit:lines.append(current);current=part
            else:current=(current+' '+part).strip()
        if current:lines.append(current)
        return lines or ['']
    for e in phase['elements']:
        c=classes[e['class']]; aa={a['name']:a for a in c.get('attributes',[])};mm={m['name']:m for m in c.get('methods',[])}
        e.update(status=c['status'],attribute_types={n:aa[n]['type'] for n in e['attributes']},method_signatures={n:mm[n]['signature'] for n in e['methods']},attribute_statuses={n:aa[n]['status'] for n in e['attributes']},method_statuses={n:mm[n]['status'] for n in e['methods']},method_parameters={n:mm[n].get('parameters',[]) for n in e['methods']},method_returns={n:mm[n].get('return','Any') for n in e['methods']},P4_inputs={n:mm[n].get('P4_input','') for n in e['methods'] if mark(mm[n])},attribute_P4_inputs={n:aa[n].get('P4_input','') for n in e['attributes'] if mark(aa[n])})
        if phase['diagram_type']=='dcd':
            n=nodes[e['class'].replace('.','_').replace('-','_')]; n['attribute_lines']=[];n['method_lines']=[]
            for name in e['attributes']:
                a=aa[name]; n['attribute_lines']+=wrap(a['visibility']+name+': '+a['type']+(' *' if a.get('inferred') else '')+mark(a),n['w'])
            for name in e['methods']:
                m=mm[name]; result=m.get('return','')
                if phase['view']=='all':
                    t=m['visibility']+name+(': '+result if 'property' in m.get('decorators',[]) else '()'+(' -> '+result if result not in ('','Any') else ''))
                else:t=m['visibility']+m['signature']+(' {property}' if 'property' in m.get('decorators',[]) else '')
                n['method_lines']+=wrap(t+(' *' if m.get('inferred') else '')+mark(m),n['w'])
            needed=n['header_h']+len(n['attribute_lines'])*(FS+10)+(18 if n['attribute_lines'] and n['method_lines'] else 0)+len(n['method_lines'])*(FS+10)+30
            if needed>n['h']:raise ValueError('Reviewed model requires layout continuation: '+e['class'])
    if phase['diagram_type']=='sequence':
        ll={l['id']:l['class'] for l in phase['lifelines']}
        for i,m in enumerate(phase['messages']):
            c=classes.get(ll[m['to']],{}); mem=next((a for a in c.get('methods',[])+c.get('attributes',[]) if a['name']==m['method']),None)
            if not mem:continue
            m.update(status=mem['status'],P4_input=mem.get('P4_input',''))
            if 'signature' in mem:m.update({'signature':mem['signature'],'parameters':mem.get('parameters',[]),'return':mem.get('return','Any'),'return_type':mem.get('return','Any')})
            edge=next((x for x in spec['edges'] if x['id']==f'msg_{i:02d}'),None)
            if edge and m['kind']=='call':edge['label']=re.sub(re.escape(m['method'])+r'(?: †)?\(',m['method']+mark(mem)+'(',edge['label'],count=1)
            if m['kind']=='note' and mem['status']=='MATCH':m['arguments']=m['arguments'].replace('† ','')
        note=nodes.get('interaction_notes')
        if note:
            text='   •   '.join(f'{m["method"]}: {m["arguments"]}' for m in phase['messages'] if m['kind']=='note')
            note['lines']=textwrap.wrap(text,width=130,break_long_words=False,break_on_hyphens=False)
    spec['source_model_sha256']=hashlib.sha256(modelpath.read_bytes()).hexdigest()
    return spec

def main():
    path=Path(__file__).with_suffix(".json")
    spec=json.loads(path.read_text(encoding="utf-8"))
    spec=refresh_from_shared_model(spec,path)
    render(spec,path)

def render(spec,path):
    W,H=spec["canvas"]["width"],spec["canvas"]["height"]
    FS=spec["canvas"]["font_size"]; placed=spec["canvas"]["placed_width_mm"]
    IM=Image.new("RGB",(W*2,H*2),WHITE); D=ImageDraw.Draw(IM)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>']
    mx=ET.Element("mxfile",host="SaigonBite P3"); dia=ET.SubElement(mx,"diagram",name=spec["title"],id="page1")
    model=ET.SubElement(dia,"mxGraphModel",page="1",pageWidth=str(W),pageHeight=str(H),grid="1",gridSize="10")
    root=ET.SubElement(model,"root"); ET.SubElement(root,"mxCell",id="0"); ET.SubElement(root,"mxCell",id="1",parent="0")
    ids=set(); boxes={}; pending_edge_labels=[]
    def cell(cid,value,x,y,w,h,style,vertex=True,source=None,target=None,edge=False):
        if cid in ids: raise ValueError("duplicate mxCell id "+cid)
        ids.add(cid)
        value=value.replace(chr(92)+"n",chr(10))
        attrs={"id":cid,"value":value,"style":style,"parent":"1"}
        if edge:
            attrs.update({"edge":"1","source":source,"target":target})
        else: attrs.update({"vertex":"1"})
        obj=ET.SubElement(root,"mxCell",attrs)
        geo=ET.SubElement(obj,"mxGeometry",x=str(x),y=str(y),width=str(w),height=str(h),attrib={"as":"geometry"})
        return obj
    def draw_text(lines,x,y,w,h,size=FS,bold=False,color=INK,align="center"):
        f=ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size*2)
        lh=size+10; total=len(lines)*lh
        yy=y+(h-total)/2
        for i,line in enumerate(lines):
            cy=yy+i*lh+size
            if align=="left":
                D.text((int((x+12)*2),int(cy*2)),line,font=f,fill=color,anchor="ls")
                tx=x+12; anchor="start"
            else:
                D.text((int((x+w/2)*2),int(cy*2)),line,font=f,fill=color,anchor="ms")
                tx=x+w/2; anchor="middle"
            svg.append(f'<text x="{tx}" y="{cy}" text-anchor="{anchor}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{color}">{escape(line)}</text>')
    def draw_node(n):
        x,y,w,h=n["x"],n["y"],n["w"],n["h"]; kind=n.get("kind","class"); nid=n["id"]
        boxes[nid]=(x,y,w,h)
        if kind=="class":
            stroke=n.get("stroke",BLUE); fill=n.get("fill",WHITE)
            D.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=fill,outline=stroke,width=4)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            head_h=n.get("header_h",110)
            D.rectangle((x*2,y*2,(x+w)*2,(y+head_h)*2),fill=PALE,outline=stroke,width=4)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{head_h}" fill="{PALE}" stroke="{stroke}" stroke-width="2"/>')
            draw_text(n.get("header_lines",[]),x+8,y+4,w-16,head_h*.62,FS,True,BLUE)
            draw_text(n.get("subtitle_lines",[]),x+8,y+head_h*.57,w-16,head_h*.4,FS,False,GREY)
            cur=y+head_h
            attrs=n.get("attribute_lines",[]); meths=n.get("method_lines",[])
            if attrs:
                ah=max(FS+10,len(attrs)*(FS+10))
                draw_text(attrs,x+12,cur+4,w-24,ah,FS,False,INK,"left")
                cur+=ah+10
            if attrs and meths:
                D.line((x*2,cur*2,(x+w)*2,cur*2),fill=BLUE,width=3)
                svg.append(f'<line x1="{x}" y1="{cur}" x2="{x+w}" y2="{cur}" stroke="{BLUE}" stroke-width="1.5"/>')
                cur+=8
            if meths:
                draw_text(meths,x+12,cur+4,w-24,max(FS+10,h-(cur-y)-12),FS,False,INK,"left")
            value="\\n".join(n.get("header_lines",[])+n.get("subtitle_lines",[])+["---"]+attrs+["---"]+meths)
            cell(nid,value,x,y,w,h,f"swimlane;startSize={head_h};html=0;whiteSpace=wrap;fillColor=#FFFFFF;swimlaneFillColor={PALE};strokeColor={stroke};fontSize={FS};fontColor={INK};")
            return
        if kind in {"layer","frame"}:
            stroke=n.get("stroke",BLUE); fill=n.get("fill","none")
            D.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),outline=stroke,width=3)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="{"8 5" if n.get("dashed") else "none"}"/>')
            draw_text(n.get("lines",[]),x+8,y+3,w-16,min(h,100),FS,True,BLUE,"left")
            cell(nid,"\\n".join(n.get("lines",[])),x,y,w,h,f"rounded=0;html=0;whiteSpace=wrap;fillColor=none;strokeColor={stroke};fontSize={FS};fontColor={BLUE};align=left;verticalAlign=top;")
            return
        if kind=="note":
            D.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=NOTE,outline=BLUE,width=3)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{NOTE}" stroke="{BLUE}" stroke-width="1.5"/>')
            draw_text(n.get("lines",[]),x+10,y+6,w-20,h-12,FS,False,INK,"left")
            cell(nid,"\\n".join(n.get("lines",[])),x,y,w,h,f"shape=note;whiteSpace=wrap;html=0;fillColor={NOTE};strokeColor={BLUE};fontSize={FS};fontColor={INK};align=left;verticalAlign=middle;")
            return
        if kind=="lifeline":
            D.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=PALE,outline=BLUE,width=4)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PALE}" stroke="{BLUE}" stroke-width="2"/>')
            draw_text(n.get("lines",[]),x+4,y+2,w-8,h-4,FS,n.get("bold",True),BLUE)
            cell(nid,"\\n".join(n.get("lines",[])),x,y,w,h,f"rounded=0;whiteSpace=wrap;html=0;fillColor={PALE};strokeColor={BLUE};fontSize={FS};fontStyle={1 if n.get('bold',True) else 0};fontColor={BLUE};")
            return
        if kind=="activation":
            D.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill="#D7E5F3",outline=BLUE,width=2)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#D7E5F3" stroke="{BLUE}" stroke-width="1"/>')
            cell(nid,"",x,y,w,h,f"rounded=0;html=0;fillColor=#D7E5F3;strokeColor={BLUE};")
            return
        if kind=="anchor":
            boxes[nid]=(x,y,w,h)
            cell(nid,"",x,y,w,h,"opacity=0;strokeOpacity=0;fillOpacity=0;")
            return
        if kind=="text":
            if n.get("background"):
                D.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=n["background"])
                svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{n["background"]}" stroke="none"/>')
            lines=n.get("lines",[])
            draw_text(lines,x,y,w,h,FS,n.get("bold",False),n.get("color",BLUE),n.get("align","left"))
            cell(nid,"\\n".join(lines),x,y,w,h,f"text;html=0;whiteSpace=wrap;align={n.get('align','left')};verticalAlign=middle;strokeColor=none;fillColor={n.get('background','none')};fontSize={FS};fontColor={n.get('color',BLUE)};")
            return
    for n in spec.get("nodes",[]):
        boxes[n["id"]]=(n["x"],n["y"],n["w"],n["h"])
        if n.get("kind")=="anchor":
            cell(n["id"],"",n["x"],n["y"],n["w"],n["h"],"opacity=0;strokeOpacity=0;fillOpacity=0;")
    for e in spec.get("edges",[]):
        src=e["source"]; dst=e["target"]
        if src not in boxes or dst not in boxes: raise ValueError(f"unresolved edge endpoint {e['id']}: {src}->{dst}")
        pts=e["points"]; color=e.get("color",BLUE); dash=e.get("dashed",False); width=e.get("width",3)
        if dash:
            for a,b in zip(pts,pts[1:]):
                dist=math.dist(a,b); n=max(1,int(dist/16))
                for k in range(n):
                    t=k/n; u=min(1,t+.58/n)
                    D.line([(int(2*(a[0]+(b[0]-a[0])*q)),int(2*(a[1]+(b[1]-a[1])*q))) for q in (t,u)],fill=color,width=width*2)
        else: D.line([(int(x*2),int(y*2)) for x,y in pts],fill=color,width=width*2)
        svg.append('<polyline points="'+" ".join(f"{x},{y}" for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="8 5"' if dash else '')+'/>')
        if e.get("arrow","block")!="none":
            a,b=pts[-2:]; ang=math.atan2(b[1]-a[1],b[0]-a[0])
            points=[b,(b[0]-18*math.cos(ang-.42),b[1]-18*math.sin(ang-.42)),(b[0]-18*math.cos(ang+.42),b[1]-18*math.sin(ang+.42))]
            if e.get("arrow")=="open":
                D.line([(int(x*2),int(y*2)) for x,y in [points[1],b,points[2]]],fill=color,width=width*2)
            else:
                D.polygon([(int(x*2),int(y*2)) for x,y in points],fill=color)
            if e.get("arrow")=="open":
                svg.append('<polyline points="'+" ".join(f"{x},{y}" for x,y in [points[1],b,points[2]])+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
            else:
                svg.append('<polygon points="'+" ".join(f"{x},{y}" for x,y in points)+f'" fill="{color}"/>')
        if e.get("label"):
            pending_edge_labels.append((e,color,pts))
        c=ET.SubElement(root,"mxCell",id=e["id"],value=e.get("label","").replace(chr(92)+"n",chr(10)),edge="1",parent="1",source=src,target=dst,style=f"edgeStyle=none;html=0;endArrow={e.get('arrow','block')};strokeColor={color};strokeWidth={width};fontSize={FS};"+("dashed=1;" if dash else ""))
        if e.get("arrow")=="open":c.set("style",c.get("style","")+"endFill=0;")
        elif e.get("arrow")!="none":c.set("style",c.get("style","")+"endFill=1;")
        if e.get("association"):
            sx,sy,sw,sh=boxes[src];tx,ty,tw,th=boxes[dst]
            c.set("style",c.get("style","")+f"exitX={(pts[0][0]-sx)/sw};exitY={(pts[0][1]-sy)/sh};exitPerimeter=0;entryX={(pts[-1][0]-tx)/tw};entryY={(pts[-1][1]-ty)/th};entryPerimeter=0;")
        g=ET.SubElement(c,"mxGeometry",relative="1",attrib={"as":"geometry"}); arr=ET.SubElement(g,"Array",attrib={"as":"points"})
        for x,y in pts[1:-1]: ET.SubElement(arr,"mxPoint",x=str(x),y=str(y))
        if e.get("association") or e["id"].startswith("msg_"):
            ET.SubElement(g,"mxPoint",x=str(pts[0][0]),y=str(pts[0][1]),attrib={"as":"sourcePoint"})
            ET.SubElement(g,"mxPoint",x=str(pts[-1][0]),y=str(pts[-1][1]),attrib={"as":"targetPoint"})
    # Draw class/lifeline boxes after connectors so the boxes mask connector segments cleanly.
    for n in spec.get("nodes",[]):
        if n.get("kind")!="anchor": draw_node(n)
    # Sequence call labels sit above activations and message lines, with only a
    # compact white backing behind the text so lifelines remain visible.
    for e,color,pts in pending_edge_labels:
        lx,ly,lw,lh=e.get("label_box",(pts[len(pts)//2][0]-180,pts[len(pts)//2][1]-30,360,60))
        D.rectangle((int(lx*2),int((ly+10)*2),int((lx+lw)*2),int((ly+lh)*2)),fill=WHITE)
        draw_text(e["label"].split("\\n"),lx,ly,lw,lh,FS,True,color)
        svg.append(f'<rect x="{lx}" y="{ly+10}" width="{lw}" height="{lh-10}" fill="white" fill-opacity="0.88" stroke="none"/>')
        for i,line in enumerate(e["label"].split("\\n")):
            cy=ly+FS+i*(FS+6)
            svg.append(f'<text x="{lx+lw/2}" y="{cy}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{FS}" font-weight="bold" fill="{color}">{escape(line)}</text>')
    # Keep title and author visible in every native source/export.
    draw_text([spec["title"]],40,16,W-80,80,FS+4,True,BLUE)
    footer=spec.get("footer", "Author: 722I0004 · AI-assisted (Codex)")
    draw_text([footer],40,H-88,W-80,68,FS,False,BLUE,"left")
    cell("diagram_title",spec["title"],40,16,W-80,80,f"text;html=0;whiteSpace=wrap;fontSize={FS+4};fontStyle=1;fontColor={BLUE};strokeColor=none;fillColor=none;")
    cell("diagram_author",footer,40,H-88,W-80,68,f"text;html=0;whiteSpace=wrap;fontSize={FS};fontColor={BLUE};strokeColor=none;fillColor=none;align=left;")
    svg.append("</svg>")
    IM.save(path.with_suffix(".png"))
    path.with_suffix(".svg").write_text("".join(svg),encoding="utf-8")
    ET.ElementTree(mx).write(path.with_suffix(".drawio"),encoding="utf-8",xml_declaration=True)
    ET.parse(path.with_suffix(".drawio"))
    min_pt=round(FS*placed/25.4*72/W,2)
    spec["render_receipt"]={"canvas":[W,H],"minimum_font_px":FS,"placed_width_mm":placed,"minimum_pt":min_pt,"xml":"parsed","connected_edges":True,"author_native_cell":True,"all_text_minimum_px":FS}
    path.with_suffix(".json").write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding="utf-8")

if __name__=="__main__": main()
