"""Reproducible UML analysis exports. Author: 722I0004, AI-assisted (Codex).

Balanced-diagrams skill: decide bounded page geometry before placing nodes;
reuse the immutable Phase 1 stakeholder renderer's font/wrap and SVG helpers.
This file owns the small shared renderer used by domain_model.py as well.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import importlib.util, json, math, shutil
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
SCRATCH = Path(r'D:\RAD\FINAL\Part2\notes\P2-B')
spec = importlib.util.spec_from_file_location('p1_stakeholder_renderer', OUT/'stakeholder_chart.py')
P1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(P1)
BLUE, INK, LINE = '#004387', '#202B36', '#52616F'
FONT = 26

class Page:
    def __init__(self, stem, title, number, width=1600, height=1220):
        self.stem,self.w,self.h=stem,width,height
        self.nodes=[]; self.edges=[]; self.texts=[]; self.shapes=[]
        self.text(30,18,title,34,True)
        self.text(30,height-66,f'Figure {number} · Author: 722I0004 · AI-assisted (Codex)',26)
        self.text(30,height-35,'Analysis model · team defaults; no lecturer approval or runtime result inferred',26)
    def text(self,x,y,s,size=FONT,bold=False,color=INK):
        self.texts.append(dict(x=x,y=y,text=s,size=size,bold=bold,color=color))
    def node(self,id,label,x,y,w,h,kind='rect',fill='#E7F0F6',attrs=None):
        n=dict(id=id,label=label,x=x,y=y,w=w,h=h,kind=kind,fill=fill,attrs=attrs)
        self.nodes.append(n); return n
    def edge(self,id,source,target,points,label='',lx=None,ly=None,kind='assoc',ends=None):
        self.edges.append(dict(id=id,source=source,target=target,points=points,label=label,lx=lx,ly=ly,kind=kind,ends=ends))
    def export(self):
        img=Image.new('RGB',(self.w,self.h),'white'); d=ImageDraw.Draw(img)
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">',
             '<rect width="100%" height="100%" fill="white"/>']
        mx=ET.Element('mxfile',{'host':'app.diagrams.net','type':'device'})
        dia=ET.SubElement(mx,'diagram',{'name':self.stem,'id':self.stem})
        mod=ET.SubElement(dia,'mxGraphModel',{'page':'1','pageWidth':str(self.w),'pageHeight':str(self.h),'grid':'1','gridSize':'10'})
        root=ET.SubElement(mod,'root'); ET.SubElement(root,'mxCell',{'id':'0'});ET.SubElement(root,'mxCell',{'id':'1','parent':'0'})
        # Edges first keeps UML association lines underneath class/use-case bodies.
        for e in self.edges:
            pts=list(e['points']); col=LINE
            ns={n['id']:n for n in self.nodes}
            # Actor symbols are narrow; connect to their arms rather than label bounds.
            for key,idx in [('source',0),('target',-1)]:
                n=ns[e[key]]
                if n['kind']=='actor' and e['kind']=='assoc':
                    point=(n['x']+85+(30 if n['x']<300 else -30),n['y']+57)
                    if idx==0:pts.insert(0,point)
                    else:pts.append(point)
            dashed=e['kind'] in ('include','extend','anchor')
            def line(a,b):
                if dashed:
                    distance=math.dist(a,b); count=max(1,int(distance/12))
                    for i in range(0,count,2):
                        t=i/count; u=min(1,(i+1)/count)
                        d.line((a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u),fill=col,width=3)
                else:d.line([a,b],fill=col,width=3)
            for a,b in zip(pts,pts[1:]): line(a,b)
            svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{col}" stroke-width="3"'+(' stroke-dasharray="10 7"' if dashed else '')+'/>')
            arrow=e['kind'] in ('general','include','extend','nav')
            if arrow:
                a,b=pts[-2:]; dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy); ux,uy=dx/length,dy/length
                p=[b,(b[0]-ux*20-uy*10,b[1]-uy*20+ux*10),(b[0]-ux*20+uy*10,b[1]-uy*20-ux*10)]
                if e['kind']=='general':d.polygon(p,fill='white',outline=col,width=3);svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="white" stroke="{col}" stroke-width="3"/>')
                else:
                    d.line([p[1],p[0],p[2]],fill=col,width=3);svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in [p[1],p[0],p[2]])+f'" fill="none" stroke="{col}" stroke-width="3"/>')
            if e['kind']=='composition':
                a,b=pts[:2]; dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
                p=[a,(a[0]+ux*14-uy*9,a[1]+uy*14+ux*9),(a[0]+ux*28,a[1]+uy*28),(a[0]+ux*14+uy*9,a[1]+uy*14-ux*9)]
                d.polygon(p,fill=col);svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{col}"/>')
            style='endArrow=none;strokeColor='+col+';strokeWidth=2;rounded=0;'
            if dashed:style+='dashed=1;'
            if arrow:style+='endArrow='+('block;endFill=0;' if e['kind']=='general' else 'open;')
            if e['kind']=='composition':style+='startArrow=diamond;startFill=1;'
            edge=ET.SubElement(root,'mxCell',{'id':e['id'],'edge':'1','parent':'1','source':e['source'],'target':e['target'],'style':style,'value':''})
            geom=ET.SubElement(edge,'mxGeometry',{'relative':'1','as':'geometry'});array=ET.SubElement(geom,'Array',{'as':'points'})
            for x,y in pts[1:-1]:ET.SubElement(array,'mxPoint',{'x':str(x),'y':str(y)})
            # Explicit endpoint attachment reproduces the same geometry on reopen.
            ns={n['id']:n for n in self.nodes}
            for key,p in [('source',pts[0]),('target',pts[-1])]:
                n=ns[e[key]];rx=(p[0]-n['x'])/n['w'];ry=(p[1]-n['y'])/n['h']
                edge.set('style',edge.get('style')+f'{"exit" if key=="source" else "entry"}X={rx};{"exit" if key=="source" else "entry"}Y={ry};')
            if e['label']:self.text(e['lx'],e['ly'],e['label'],26,color=BLUE)
            if e['ends']:
                for s,x,y in e['ends']:self.text(x,y,s,26,color=BLUE)
        for n in self.nodes:
            x,y,w,h=n['x'],n['y'],n['w'],n['h'];kind=n['kind'];fill=n['fill']
            if kind=='actor':
                cx=x+w/2;cy=y+22
                d.ellipse((cx-16,cy-16,cx+16,cy+16),outline=INK,width=3)
                d.line([(cx,cy+16),(cx,cy+65)],fill=INK,width=3);d.line([(cx-30,cy+35),(cx+30,cy+35)],fill=INK,width=3)
                d.line([(cx-28,cy+100),(cx,cy+65),(cx+28,cy+100)],fill=INK,width=3)
                svg.extend([f'<circle cx="{cx}" cy="{cy}" r="16" fill="white" stroke="{INK}" stroke-width="3"/>',f'<path d="M{cx},{cy+16} V{cy+65} M{cx-30},{cy+35} H{cx+30} M{cx-28},{cy+100} L{cx},{cy+65} L{cx+28},{cy+100}" fill="none" stroke="{INK}" stroke-width="3"/>'])
                lines=n['label'].split('\n');tx=x;ty=y+128
                for i,s in enumerate(lines):
                    tw=d.textlength(s,font=P1.font(26));d.text((cx-tw/2,ty+i*31),s,font=P1.font(26),fill=INK);P1.add_text_svg(svg,cx-tw/2,ty+i*31,[s],26)
                style='shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;fillColor=white;'
                value=n['label']
            else:
                if kind=='ellipse':d.ellipse((x,y,x+w,y+h),fill=fill,outline=BLUE,width=3);svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{BLUE}" stroke-width="3"/>')
                elif kind=='frame':d.rectangle((x,y,x+w,y+h),outline=BLUE,width=3);svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
                else:d.rectangle((x,y,x+w,y+h),fill=fill,outline=BLUE,width=3);svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{BLUE}" stroke-width="3"/>')
                label_lines=n['label'].split('\n')
                if kind=='class':
                    self.text(x+14,y+12,n['label'],28,True)
                    d.line((x,y+52,x+w,y+52),fill=BLUE,width=2);svg.append(f'<path d="M{x},{y+52} H{x+w}" stroke="{BLUE}" stroke-width="2"/>')
                    for i,a in enumerate(n['attrs'] or []):self.text(x+14,y+65+i*31,a,26)
                elif kind in ('frame','note','ref'):
                    self.text(x+12,y+12,n['label'],26,kind=='frame')
                else:
                    lines=[]
                    for s in label_lines:lines.extend(P1.wrap_lines(d,s,P1.font(26),w-70))
                    top=y+(h-len(lines)*31)/2
                    for i,s in enumerate(lines):
                        tw=d.textlength(s,font=P1.font(26));self.text(x+(w-tw)/2,top+i*31,s,26)
                style=('ellipse;' if kind=='ellipse' else '')+f'fillColor={"none" if kind=="frame" else fill};strokeColor={BLUE};whiteSpace=wrap;'
                value='' # Editable text cells reproduce every line independently.
            cell=ET.SubElement(root,'mxCell',{'id':n['id'],'vertex':'1','parent':'1','value':value,'style':style+'fontFamily=Arial;fontSize=26;html=0;'})
            ET.SubElement(cell,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'})
            if kind=='class':
                separator=ET.SubElement(root,'mxCell',{'id':n['id']+'_compartment_line','vertex':'1','parent':'1','value':'','style':f'shape=line;strokeColor={BLUE};strokeWidth=2;'})
                ET.SubElement(separator,'mxGeometry',{'x':str(x),'y':str(y+52),'width':str(w),'height':'1','as':'geometry'})
        for i,t in enumerate(self.texts):
            lines=t['text'].split('\n');f=P1.font(t['size'],t['bold'])
            for j,s in enumerate(lines):d.text((t['x'],t['y']+j*t['size']*1.19),s,font=f,fill=t['color'])
            P1.add_text_svg(svg,t['x'],t['y'],lines,t['size'],t['color'],t['bold'],t['size']*1.19)
            P1.add_drawio_text(root,'text_'+str(i),t['x'],t['y'],max(d.textlength(s,font=f) for s in lines)+8,len(lines)*t['size']*1.25,lines,t['size'],t['bold'],t['color'])
        svg.append('</svg>')
        (OUT/(self.stem+'.svg')).write_text('\n'.join(svg),encoding='utf-8')
        img.save(OUT/(self.stem+'.png'))
        ET.indent(mx);ET.ElementTree(mx).write(OUT/(self.stem+'.drawio'),encoding='utf-8',xml_declaration=True)
        data=dict(stem=self.stem,width=self.w,height=self.h,font_min=26,placed_width_mm=230,min_placed_pt=26*230/self.w*72/25.4,nodes=self.nodes,edges=self.edges)
        (OUT/(self.stem+'.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
        ids={n['id'] for n in self.nodes}
        assert len(ids)==len(self.nodes)
        assert all(e['source'] in ids and e['target'] in ids for e in self.edges)
        ET.parse(OUT/(self.stem+'.drawio'));ET.parse(OUT/(self.stem+'.svg'))
        assert data['min_placed_pt']>=9
        return data

def actor(p,id,label,x,y):return p.node(id,label,x,y,170,120,'actor')
def uc(p,id,label,x,y,w,h,main=False):return p.node(id,label,x,y,w,h,'ellipse','#DCEAF5' if main else '#F5F8FA')
def system(p,w=1120,h=970):
    # Place boundary first so it does not obscure inner shapes in every export.
    p.node('system','SaigonBite system',300,100,w,h,'frame','white')
def build():
    pages=[]
    p=Page('use_case_diagram_PartA','Use cases · (a) ordering and customer support','2.1A')
    system(p,h=950)
    actor(p,'customer','Customer',60,260);actor(p,'local','Local\ncustomer',5,730);actor(p,'tourist','Tourist\ncustomer',145,730)
    actor(p,'simulator','Payment\nsimulator',1430,510)
    uc(p,'UC01','UC-01\nPlace an order with an accepted full price, voucher and payment choice\nextension point:\npayment authorization',370,155,640,260,True)
    uc(p,'quote','Validate accepted checkout\n«included subgoal»',1080,180,300,170)
    uc(p,'online','Simulate online payment\n«extension subgoal»',1080,500,300,170)
    uc(p,'SUC02','SUC-02\nRegister (local or tourist), edit profile, manage addresses',370,520,310,210)
    uc(p,'SUC03','SUC-03\nTrack my orders, view receipt, answer a replacement offer\nextension point:\norder action selected',720,500,320,270)
    uc(p,'SUC04','SUC-04\nCancel an order\n(PLACED or CONFIRMED)',690,850,390,175)
    for id,target,pts in [('a1','UC01',[(230,310),(370,285)]),('a2','SUC02',[(230,330),(320,330),(320,625),(370,625)]),('a3','SUC03',[(230,350),(290,350),(290,805),(690,805),(690,635),(720,635)])]:p.edge(id,'customer',target,pts)
    p.edge('genlocal','local','customer',[(90,730),(15,730),(15,215),(145,215),(145,260)],kind='general')
    p.edge('gentourist','tourist','customer',[(230,730),(270,730),(270,195),(175,195),(175,260)],kind='general')
    p.edge('includequote','UC01','quote',[(1010,260),(1080,260)],'«include»',1015,360,'include')
    p.edge('extendonline','online','UC01',[(1230,500),(1230,450),(690,450),(690,415)],'«extend» [ONLINE]',1060,465,'extend')
    p.edge('extendcancel','SUC04','SUC03',[(880,850),(880,770)],'«extend»\n[request cancel; state\nPLACED or CONFIRMED]',1070,790,'extend')
    p.edge('sim','simulator','online',[(1430,570),(1380,585)])
    p.text(355,1100,'Solid line = actor participation; hollow triangle points to general actor.',26)
    pages.append(p)
    p=Page('use_case_diagram_PartB','Use cases · (b) kitchen and shipper fulfilment','2.1B',height=1100)
    system(p,h=850)
    actor(p,'kitchen','Kitchen staff',70,265);actor(p,'shipper','Shipper',70,735);actor(p,'customer','Customer',1430,220)
    uc(p,'UC05','UC-05\nDecide an incoming order: confirm, reject, or offer a replacement the customer agrees to',390,180,900,225,True)
    uc(p,'SUC05','SUC-05\nStart preparing and mark ready',390,510,430,155)
    uc(p,'SUC06','SUC-06\nSet menu availability at my hub',900,510,430,155)
    uc(p,'UC02','UC-02\nDeliver an order: pick up, deliver with cash collection, or report failure',390,745,900,190,True)
    p.edge('k5','kitchen','UC05',[(240,315),(390,290)])
    p.edge('kprep','kitchen','SUC05',[(240,335),(320,335),(320,587),(390,587)])
    p.edge('kavail','kitchen','SUC06',[(240,355),(280,355),(280,705),(1115,705),(1115,665)])
    p.edge('ship','shipper','UC02',[(240,785),(390,840)])
    p.edge('reply','customer','UC05',[(1430,280),(1290,290)])
    p.text(490,430,'Customer answer occurs through SUC-03 (Figure 2.1A);',26)
    p.text(490,465,'it does not create a second synchronous kitchen actor session.',26)
    p.text(350,975,'Sequence dependencies are described in flows, not drawn as «include».',26)
    pages.append(p)
    p=Page('use_case_diagram_PartC','Use cases · (c) administration, (d) reports and shared access','2.1C',height=1370)
    system(p,h=1060)
    actor(p,'admin','Admin',70,370);actor(p,'manager','Manager',1430,520)
    actor(p,'customer','Customer',1430,805);actor(p,'kitchen','Kitchen staff',1430,970);actor(p,'shipper','Shipper',70,1010)
    uc(p,'UC03','UC-03\nMaintain hubs and kitchen capacity',380,175,440,195,True)
    uc(p,'UC06','UC-06\nMaintain brands, menu items and hub listings',875,175,470,195,True)
    uc(p,'SUC07','SUC-07\nMaintain vouchers',380,440,380,135)
    uc(p,'SUC08','SUC-08\nMaintain user accounts;\ndeactivate/reactivate',380,635,380,155)
    uc(p,'SUC09','SUC-09\nArchive closed orders;\nread archived history',380,850,380,155)
    uc(p,'UC04','UC-04\nProduce management reports: sales, workload, delivery performance',875,495,470,230,True)
    uc(p,'SUC01','SUC-01\nLog in / log out',910,970,400,140)
    for id,t,y,pts in [('ad3','UC03',270,[(240,410),(330,410),(330,270),(380,270)]),('ad6','UC06',270,[(240,430),(280,430),(280,155),(1110,155),(1110,175)]),('ad7','SUC07',507,[(240,450),(380,507)]),('ad8','SUC08',710,[(240,470),(320,470),(320,710),(380,710)]),('ad9','SUC09',928,[(240,490),(290,490),(290,928),(380,928)])]:p.edge(id,'admin',t,pts)
    p.edge('manage','manager','UC04',[(1430,570),(1345,610)])
    p.edge('loginad','admin','SUC01',[(240,510),(265,510),(265,1130),(1110,1130),(1110,1110)])
    p.edge('loginma','manager','SUC01',[(1430,590),(1410,590),(1410,1018),(1300,1018)])
    p.edge('logincu','customer','SUC01',[(1430,855),(1380,855),(1380,1040),(1310,1040)])
    p.edge('loginki','kitchen','SUC01',[(1430,1020),(1350,1020),(1350,1062),(1300,1062)])
    p.edge('loginsh','shipper','SUC01',[(240,1060),(910,1060)])
    p.text(900,405,'(c) CRUD management',26,True)
    p.text(900,755,'(d) read-only reports',26,True)
    p.text(900,825,'Authentication is a session precondition,\nnot an include on every business request.',26)
    p.text(325,1190,'Deferred (L3): complaint/refund decision, refund payout, rating. No deferred UCs drawn.',26)
    pages.append(p)
    result=[p.export() for p in pages]
    for suffix in ['drawio','png','svg','json']:shutil.copyfile(OUT/f'use_case_diagram_PartA.{suffix}',OUT/f'use_case_diagram.{suffix}')
    # Main editable source contains every readable page; main image is first-page alias.
    combined=ET.Element('mxfile',{'host':'app.diagrams.net','type':'device'})
    for p in pages:combined.append(ET.parse(OUT/(p.stem+'.drawio')).getroot().find('diagram'))
    ET.indent(combined);ET.ElementTree(combined).write(OUT/'use_case_diagram.drawio',encoding='utf-8',xml_declaration=True)
    (OUT/'use_case_diagram.json').write_text(json.dumps({'parts':result,'main_image':'first-page alias; use every PartA–PartC in the report','author':'722I0004 · AI-assisted (Codex)','user_goal_count':15,'factored_subgoals':['Validate accepted checkout','Simulate online payment'],'relation_decisions':['UC01 includes mandatory validation','Online simulation extends UC01 at payment authorization when ONLINE','SUC04 extends SUC03 at order action selected when cancellation requested and cancellable']},indent=2),encoding='utf-8')
    return result
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(build(),default=str)[:0]+'Use-case exports generated and XML/endpoint/font checks passed.')
