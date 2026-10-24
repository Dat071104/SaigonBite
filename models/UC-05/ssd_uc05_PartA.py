"""Owned P2-E renderer/data builder. Geometry/font/export pattern adapted from
read-only models/shared/use_case_diagram.py and sm_order.py. No shared writes.
Run this file with bundled Python -Xutf8 -I to rebuild the complete E package.
Author: 722I0004 · AI-assisted (Codex)
"""
from pathlib import Path
import sys,json,math,shutil,subprocess,xml.etree.ElementTree as ET
from html import escape
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
R=Path('D:/RAD/FINAL/SaigonBite'); S=Path('D:/RAD/FINAL/Part2/notes/P2-E')
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'
W,H,FONT=1600,1200,26
INK,BLUE='#202B36','#004387'
def font(size=FONT,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
class Canvas:
    def __init__(self,uc,stem,title,figure,kind='activity'):
        self.uc,self.stem,self.title,self.figure,self.kind=uc,stem,title,figure,kind
        self.im=Image.new('RGB',(W,H),'white');self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>']
        self.mx=ET.Element('mxfile',host='SaigonBite analysis',type='device');dia=ET.SubElement(self.mx,'diagram',name=title,id=stem);model=ET.SubElement(dia,'mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H));self.root=ET.SubElement(model,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0')
        self.nodes={};self.edges=[];self.labels=[];self.decisions={};self.tcount=0
        self.txt(800,35,title,32,True,width=1530)
        self.txt(800,1125,f'Figure {figure}. {title} — {AUTHOR}',26,False,width=1540)
        self.txt(800,1165,'Analysis contract · 230 mm landscape · minimum 10.59 pt · no execution result',26,width=1540)
        if kind=='activity':
            self.line([(20,90),(1580,90),(1580,1115),(20,1115),(20,90)])
            self.line([(410,90),(410,1115)],arrow=False)
            self.txt(210,120,'Actor',28,True);self.txt(995,120,'System',28,True)
    def wrap(self,s,width,size=26):
        out=[]
        for line in s.split('\n'):
            words=line.split();cur=''
            for word in words:
                test=(cur+' '+word).strip()
                if font(size).getlength(test)>width and cur:out.append(cur);cur=word
                else:cur=test
            out.append(cur)
        return out
    def vertex(self,id,label,x,y,w,h,style):
        c=ET.SubElement(self.root,'mxCell',id=id,value=label,vertex='1',parent='1',style=style+'fontFamily=Arial;fontSize=26;html=0;whiteSpace=wrap;')
        ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    def txt(self,x,y,s,size=26,bold=False,width=1000,bg=False):
        lines=self.wrap(s,width,size);lh=size*1.18;top=y-(len(lines)-1)*lh/2
        if bg:
            maxw=max(font(size,bold).getlength(q) for q in lines)+12
            self.d.rectangle((x-maxw/2,top-2,x+maxw/2,top+len(lines)*lh),fill='white')
            self.svg.append(f'<rect x="{x-maxw/2}" y="{top-2}" width="{maxw}" height="{len(lines)*lh+2}" fill="white"/>')
        for j,q in enumerate(lines):
            yy=top+j*lh;ww=font(size,bold).getlength(q)
            self.d.text((x-ww/2,yy),q,font=font(size,bold),fill=INK)
            self.svg.append(f'<text x="{x}" y="{yy+size*.92}" text-anchor="middle" font-family="Arial" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{INK}">{escape(q)}</text>')
        self.vertex('txt'+str(self.tcount),'\n'.join(lines),x-width/2,top,width,len(lines)*lh,'text;strokeColor=none;fillColor=none;align=center;');self.tcount+=1
    def line(self,pts,arrow=False,dash=False,native=True):
        for a,b in zip(pts,pts[1:]):
            if native:
                ident='visual_line_'+str(self.tcount);self.tcount+=1
                c=ET.SubElement(self.root,'mxCell',id=ident,vertex='1',parent='1',value='',style='shape=line;strokeColor='+BLUE+';strokeWidth=2;'+('dashed=1;' if dash else ''))
                g=ET.SubElement(c,'mxGeometry',x=str(min(a[0],b[0])),y=str(min(a[1],b[1])),width=str(abs(b[0]-a[0])),height=str(abs(b[1]-a[1])),attrib={'as':'geometry'})
            if dash:
                length=math.dist(a,b);steps=max(1,int(length/10))
                for j in range(0,steps,2):
                    self.d.line((a[0]+(b[0]-a[0])*j/steps,a[1]+(b[1]-a[1])*j/steps,a[0]+(b[0]-a[0])*min(j+1,steps)/steps,a[1]+(b[1]-a[1])*min(j+1,steps)/steps),fill=BLUE,width=3)
            else:self.d.line([a,b],fill=BLUE,width=3)
        self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="'+BLUE+'" stroke-width="3"'+(' stroke-dasharray="10 8"' if dash else '')+'/>')
        if arrow:
            a,b=pts[-2:];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l;p=[(b[0]-ux*17-uy*8,b[1]-uy*17+ux*8),b,(b[0]-ux*17+uy*8,b[1]-uy*17-ux*8)]
            self.d.line(p,fill=BLUE,width=3);self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in p)+'" fill="none" stroke="'+BLUE+'" stroke-width="3"/>')
    def node(self,id,s,x,y,w=460,h=115,kind='action'):
        self.nodes[id]=dict(id=id,label=s,x=x,y=y,w=w,h=h,kind=kind)
        box=(x-w/2,y-h/2,x+w/2,y+h/2);fill='#E7F0F6'
        if kind in ['decision','merge']:
            pts=[(x,y-h/2),(x+w/2,y),(x,y+h/2),(x-w/2,y)];self.d.polygon(pts,fill='white',outline=BLUE,width=3);self.svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+'" fill="white" stroke="'+BLUE+'" stroke-width="3"/>');style='rhombus;'
            if kind=='decision':self.decisions[id]=[]
        elif kind in ['initial','final','connector']:
            self.d.ellipse(box,fill=BLUE if kind=='initial' else 'white',outline=BLUE,width=3);self.svg.append(f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="{BLUE if kind=="initial" else "white"}" stroke="{BLUE}" stroke-width="3"/>');style='shape=endState;' if kind=='final' else 'ellipse;'
            if kind=='final':self.d.ellipse((box[0]+6,box[1]+6,box[2]-6,box[3]-6),fill=BLUE);self.svg.append(f'<ellipse cx="{x}" cy="{y}" rx="{w/2-6}" ry="{h/2-6}" fill="{BLUE}"/>')
        else:
            self.d.rounded_rectangle(box,radius=16,fill=fill,outline=BLUE,width=3);self.svg.append(f'<rect x="{box[0]}" y="{box[1]}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{BLUE}" stroke-width="3"/>');style='rounded=1;'
        nativefill=BLUE if kind=='initial' else ('white' if kind in ['decision','merge','connector','final'] else fill)
        self.vertex(id,'',box[0],box[1],w,h,style+'fillColor='+nativefill+';strokeColor='+BLUE+';strokeWidth=2;')
        if s:self.txt(x,y-12,s,26,width=w-24)
        return id
    def edge(self,id,src,dst,label='',points=None,labelpos=None):
        sn,dn=self.nodes[src],self.nodes[dst]
        if points is None:
            if abs(sn['x']-dn['x'])<1:points=[(sn['x'],sn['y']+sn['h']/2),(dn['x'],dn['y']-dn['h']/2)]
            elif abs(sn['y']-dn['y'])<1:
                sign=1 if dn['x']>sn['x'] else -1;points=[(sn['x']+sign*sn['w']/2,sn['y']),(dn['x']-sign*dn['w']/2,dn['y'])]
            else:points=[(sn['x'],sn['y']+sn['h']/2),(sn['x'],(sn['y']+dn['y'])/2),(dn['x'],(sn['y']+dn['y'])/2),(dn['x'],dn['y']-dn['h']/2)]
        self.line(points,True,native=False)
        style='edgeStyle=none;endArrow=open;strokeColor='+BLUE+';strokeWidth=2;'
        for prefix,node,point in [('exit',sn,points[0]),('entry',dn,points[-1])]:style+=f'{prefix}X={(point[0]-(node["x"]-node["w"]/2))/node["w"]};{prefix}Y={(point[1]-(node["y"]-node["h"]/2))/node["h"]};{prefix}Perimeter=0;'
        c=ET.SubElement(self.root,'mxCell',id=id,source=src,target=dst,edge='1',parent='1',value='',style=style);g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});arr=ET.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in points[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        self.edges.append(dict(id=id,source=src,target=dst,label=label,points=points))
        if src in self.decisions:self.decisions[src].append(label)
        if label:
            if not labelpos:labelpos=((points[0][0]+points[-1][0])/2,(points[0][1]+points[-1][1])/2-25)
            self.txt(*labelpos,label,26,width=450,bg=True)
    def export(self):
        out=R/'models'/self.uc/self.stem;out.parent.mkdir(parents=True,exist_ok=True)
        self.svg.append('</svg>');out.with_suffix('.svg').write_text('\n'.join(self.svg),encoding='utf-8');self.im.save(out.with_suffix('.png'))
        ET.indent(self.mx);ET.ElementTree(self.mx).write(out.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
        for e in self.edges:assert e['source'] in self.nodes and e['target'] in self.nodes
        for id,guards in self.decisions.items():assert len(guards)>=2 and all(g.startswith('[') and g.endswith(']') for g in guards),(id,guards)
        ET.parse(out.with_suffix('.svg'));ET.parse(out.with_suffix('.drawio'))
        data=dict(author=AUTHOR,title=self.title,figure=self.figure,canvas=[W,H],minimum_font_px=26,placed_width_mm=230,minimum_placed_pt=round(26*230/W*72/25.4,2),nodes=list(self.nodes.values()),edges=self.edges,decisions=self.decisions)
        out.with_suffix('.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
        return data
def act(uc,suffix,title,fig):return Canvas(uc,f'activity_uc{uc[-2:]}_Part{suffix}',title,fig)
def build_activity01():
    p=act('UC-01','A','UC-01 — quote and selection','2.10A')
    p.node('01A-I','',210,190,28,28,'initial');p.node('01A-1','1 browseHubs()',210,300,340,90);p.node('01A-2','1 ACTIVE hubs, load/capacity\nNo persistent writes',1120,300,620,100)
    p.node('01A-3','2 Select hub\nselectHub(hubId)',210,470,340,100);p.node('01A-4','2 Available menu + own addresses\nNo persistent writes',1120,470,620,100)
    p.node('01A-5','3 Choose address, lines, voucher, payment\nrequestQuote(...)',210,660,340,160);p.node('01A-6','3 Validate actor/owner, active hub/menu, qty, raw radius, load, voucher, payment\nCompute full fingerprint + S/D/F/Q/T',1120,660,620,160)
    p.node('01A-D','Quote eligible?',1120,865,230,115,'decision');p.node('01A-E','E01/E02 refusal or busySuggestions\nNo Order/Payment/Line saved\nMG01 / MG03',650,865,400,160);p.node('01A-F','',650,1050,34,34,'final');p.node('01A-AB','AB',1120,1050,70,70,'connector')
    for i,s,t in [('a','01A-I','01A-1'),('b','01A-1','01A-2'),('c','01A-2','01A-3'),('d','01A-3','01A-4'),('e','01A-4','01A-5'),('f','01A-5','01A-6'),('g','01A-6','01A-D'),('j','01A-E','01A-F')]:p.edge(i,s,t)
    p.edge('h','01A-D','01A-E','[not eligible]',labelpos=(930,825));p.edge('i','01A-D','01A-AB','[eligible]',labelpos=(1280,980))
    p.txt(220,975,'Retry/suggestion choice starts\na fresh quote at 2/3; menu may differ.\nEmpty suggestions handled.',26,width=365)
    p.txt(1120,1084,'AB → Part B; 4 explicit full-price consent',26,width=750);a=p.export()
    p=act('UC-01','B','UC-01 — consent, choice and replay','2.10B')
    p.node('01B-AB','AB',210,190,70,70,'connector');p.node('01B-4','4 Review full fingerprint + T\nAccept full quote',210,330,340,125);p.node('01B-D1','Method?',1100,330,220,110,'decision')
    p.node('01B-ON','A02 ONLINE: choose valid option and simulator approve/decline BEFORE transaction',210,540,340,195);p.node('01B-M','',1100,690,44,44,'merge')
    p.node('01B-5','5 confirmCheckout(...)\nToken distinct from CSRF',210,840,340,125);p.node('01B-T','5 Begin short checkout transaction\nRecheck active role; token ownership\nDo not authorize a replay',1100,840,690,125);p.node('01B-D2','Token status?',1100,1010,240,110,'decision')
    p.node('01B-RE','A01 existingOrder\nMG02; no second save',650,1010,370,105);p.node('01B-END','',440,1010,34,34,'final');p.node('01B-BC','BC',1460,1010,70,70,'connector')
    p.edge('a','01B-AB','01B-4');p.edge('b','01B-4','01B-D1');p.edge('c','01B-D1','01B-ON','[ONLINE]',points=[(1100,275),(1100,240),(600,240),(600,540),(380,540)],labelpos=(700,465));p.edge('d','01B-D1','01B-M','[COD]',labelpos=(1200,540));p.edge('e','01B-ON','01B-M',points=[(210,637),(210,690),(1078,690)])
    p.edge('f','01B-M','01B-5');p.edge('g','01B-5','01B-T');p.edge('h','01B-T','01B-D2');p.edge('i','01B-D2','01B-RE','[own token found]',labelpos=(825,945));p.edge('j','01B-RE','01B-END');p.edge('k','01B-D2','01B-BC','[no own token]',labelpos=(1390,935))
    p.txt(1110,1084,'BC → Part C: foreign token is refused; unused token is revalidated.',26,width=900);b=p.export()
    p=act('UC-01','C','UC-01 — atomic checkout and outcomes','2.10C')
    p.node('01C-BC','BC',210,190,70,70,'connector');p.node('01C-V','6 Validate accepted checkout in transaction:\nunused token; own valid address; eligible lines;\nraw d ≤8.0; capacity; voucher; fingerprint + T',1100,245,800,145)
    p.node('01C-D1','All guards +\nconsent match?',1100,395,340,145,'decision');p.node('01C-E','E01/02/03 refusal,\nbusySuggestions / revisedQuote\nNo saved rows; MG01/MG03',650,395,360,145);p.node('01C-EF','',440,395,34,34,'final')
    p.node('01C-P','6 COD skips simulator; ONLINE runs short\ndeterministic decision INSIDE transaction',1100,550,800,95);p.node('01C-D2','Payment permits\ncreation?',1100,680,340,140,'decision');p.node('01C-DECL','E04 ONLINE declined\nNo rows; MG01',650,680,360,100);p.node('01C-DF','',440,680,34,34,'final')
    p.node('01C-W','7 Create Order PLACED + line/address snapshots\n+ S/D/F/Q/T + COD PENDING / ONLINE PAID C=T\nTry all writes + COMMIT as one unit',1100,825,800,120)
    p.node('01C-D3','Atomic save?',1100,970,300,120,'decision');p.node('01C-ROLL','E05 rollback all writes; release\nauthorization even on COMMIT failure\n0 saved rows; MG01',650,970,360,160);p.node('01C-RF','',440,970,34,34,'final');p.node('01C-S','8 placedOrderAndReceipt; PC01–06; load +1',1100,1080,800,55);p.node('01C-END','',1530,1080,34,34,'final')
    p.edge('a','01C-BC','01C-V',points=[(245,190),(680,190),(680,170),(1100,170),(1100,172)]);p.edge('b','01C-V','01C-D1');p.edge('c','01C-D1','01C-E','[no]',labelpos=(880,355));p.edge('d','01C-E','01C-EF');p.edge('e','01C-D1','01C-P','[yes]',labelpos=(1320,465));p.edge('f','01C-P','01C-D2');p.edge('g','01C-D2','01C-DECL','[ONLINE declined]',labelpos=(880,605));p.edge('h','01C-DECL','01C-DF');p.edge('i','01C-D2','01C-W','[COD or ONLINE approved]',labelpos=(1295,745));p.edge('j','01C-W','01C-D3');p.edge('k','01C-D3','01C-ROLL','[failed]',labelpos=(890,930));p.edge('l','01C-ROLL','01C-RF');p.edge('m','01C-D3','01C-S','[committed]',labelpos=(1320,1025));p.edge('n','01C-S','01C-END')
    p.txt(215,500,'Busy: ≤3 ACTIVE non-busy hubs\nwithin radius; load ratio, distance, ID.\nNew hub → new quote.\nChanged consent → new acceptance.',26,width=365)
    p.txt(210,900,'9 viewReceipt (SUC-03)\nF01 tracking/cancel follow-up\nuses SSD Part C and\nOrder Figure 2.3C.',26,width=355)
    return [a,b,p.export()]
def build_activity05():
    p=act('UC-05','A','UC-05 — incoming kitchen decision','2.18A')
    p.node('05A-I','',210,190,28,28,'initial');p.node('05A-Q','1–2 viewKitchenOrders()\nviewKitchenOrder(orderId)',210,340,350,125);p.node('05A-R','1–2 Read ownHubOrdersAndOffers /\nownHubOrderAndLines; passport excluded',1120,340,760,125)
    p.node('05A-D','3 Decision?',210,560,200,120,'decision');p.node('05A-M','',960,560,44,44,'merge');p.node('05A-B','B',210,840,70,70,'connector')
    p.node('05A-V','3/A02 Try guarded atomic command + COMMIT:\nactive own-hub PLACED; confirm: no open offer;\nreject: nonempty reason; any failure rolls back.',1120,730,760,135);p.node('05A-G','All guards +\ncommit pass?',1120,915,340,145,'decision');p.node('05A-E','E01/E04 refusal/rollback\nOrder unchanged; MG01',650,915,400,115);p.node('05A-EF','',650,1070,34,34,'final');p.node('05A-S','4 CONFIRMED + confirmed_at (PC01)\nOR A02 REJECTED + reason + BR-17\n+ open offer WITHDRAWN (PC02)',1120,1065,760,100);p.node('05A-F','',1530,1065,34,34,'final')
    p.edge('a','05A-I','05A-Q');p.edge('b','05A-Q','05A-R');p.edge('c','05A-R','05A-D');p.edge('d','05A-D','05A-M','[confirm]',points=[(310,560),(938,560)],labelpos=(620,515));p.edge('e','05A-D','05A-M','[reject]',points=[(110,560),(60,560),(60,430),(960,430),(960,538)],labelpos=(620,395));p.edge('f','05A-D','05A-B','[offer]',labelpos=(310,720));p.edge('g','05A-M','05A-V');p.edge('h','05A-V','05A-G');p.edge('i','05A-G','05A-E','[fail]',labelpos=(900,875));p.edge('j','05A-E','05A-EF');p.edge('k','05A-G','05A-S','[pass]',labelpos=(1360,978));p.edge('l','05A-S','05A-F');p.txt(215,1010,'B → Part B\nSUC-05 preparation is\na later supporting goal.',26,width=355);a=p.export()
    p=act('UC-05','B','UC-05 — replacement offer guards','2.18B')
    p.node('05B-B','B',210,190,70,70,'connector');p.node('05B-A','A03 choose line + target\nofferReplacement(...)',210,380,350,135);p.node('05B-V','A03 Validate and try atomic OFFERED + COMMIT:\nactive own-hub PLACED; no OFFERED; line belongs to Order;\nsource NOW unavailable (sold out / unlisted / archived);\ntarget active + brand active, same-hub listed AVAILABLE,\ndifferent, not another line, price ≤ source snapshot',1100,380,820,230)
    p.node('05B-D','Guards + save pass?',1100,660,340,145,'decision');p.node('05B-E','E01/E02/E04 refusal or rollback\nOrder unchanged; MG01',640,660,400,145);p.node('05B-F','',640,870,34,34,'final');p.node('05B-O','A03 One OFFERED committed; original/new\nname + price snapshots; whole line, same qty\nOrder stays PLACED; still counts in load (PC03)',1100,870,820,145);p.node('05B-C','C',1100,1050,70,70,'connector')
    p.edge('a','05B-B','05B-A');p.edge('b','05B-A','05B-V');p.edge('c','05B-V','05B-D');p.edge('d','05B-D','05B-E','[fail]',labelpos=(885,620));p.edge('e','05B-E','05B-F');p.edge('f','05B-D','05B-O','[pass]',labelpos=(1290,765));p.edge('g','05B-O','05B-C');p.txt(215,820,'Cross-brand allowed.\nResolved offers remain history.\nAt most one OFFERED/order.\nConfirm/startPreparing blocked\nwhile open.',26,width=350);p.txt(1100,1084,'C → Part C: request has committed; no transaction waits for Customer.',26,width=1000);b=p.export()
    p=act('UC-05','C','UC-05 — separate Customer response','2.18C')
    p.node('05C-C','C',210,190,70,70,'connector');p.node('05C-Q','C1 Read own orders + offer\nC2 Review amounts; submit\nACCEPT or DECLINE',210,300,350,135)
    p.node('05C-V','C3/C6 Recheck active owner, own PLACED, exact open OFFERED\nbelongs to Order. ACCEPT also requires target still ACTIVE,\nbrand active, same-hub listed + AVAILABLE.\nDECLINE needs no target availability check.',1100,300,800,175)
    p.node('05C-D','Selected response\neligible?',1100,505,340,145,'decision');p.node('05C-E','E03 stale: 0 rows.\nE02 invalid target:\noffer WITHDRAWN;\nreturn reason only.\nOrder/lines/payment\nunchanged (MG01).',650,505,360,220);p.node('05C-EF','',440,505,34,34,'final')
    p.node('05C-M','C4/C6 Try one atomic response + COMMIT:\nACCEPT: offer ACCEPTED; offered price, same qty;\nD=min(Dold,Snew); F/Q same; COD payable=Tnew;\nONLINE PAID; C unchanged; owed=C−Tnew (PC04).\nDECLINE: DECLINED + REJECTED; reason/closed_at;\nCOD VOIDED / ONLINE REFUND_PENDING, owed=C (BR-17).',1100,755,800,220)
    p.node('05C-COMMIT','Atomic save?',1100,970,300,120,'decision');p.node('05C-ROLL','E04 rollback every intended change\nOrder unchanged (MG01); controlled retry',650,970,360,145);p.node('05C-RF','',440,970,34,34,'final');p.node('05C-S','C5/C6 Return committed response',1100,1080,800,55);p.node('05C-F','',1530,1080,34,34,'final')
    p.edge('a','05C-C','05C-Q');p.edge('b','05C-Q','05C-V');p.edge('c','05C-V','05C-D');p.edge('d','05C-D','05C-E','[no]',labelpos=(880,465));p.edge('e','05C-E','05C-EF');p.edge('f','05C-D','05C-M','[yes]',labelpos=(1320,610));p.edge('g','05C-M','05C-COMMIT');p.edge('h','05C-COMMIT','05C-ROLL','[failed]',labelpos=(890,930));p.edge('i','05C-ROLL','05C-RF');p.edge('j','05C-COMMIT','05C-S','[committed]',labelpos=(1320,1025));p.edge('k','05C-S','05C-F')
    p.txt(215,700,'SUC-03 response session.\nChoice precedes transaction.\nInvalid-target withdrawal also\nrolls back on save failure (E04).\nNo transaction waits for user.\nAcceptance is not confirmation.',26,width=345)
    return [a,b,p.export()]
class SSD(Canvas):
    def __init__(self,uc,suffix,title,fig,actor):
        super().__init__(uc,f'ssd_uc{uc[-2:]}_Part{suffix}',title,fig,'ssd');self.actor=actor
        self.node('actor',actor,200,120,300,65);self.node('system',':System',1400,120,300,65)
        self.line([(200,155),(200,1110)],dash=True);self.line([(1400,155),(1400,1110)],dash=True)
    def frame(self,id,label,y,h,dividers=()):
        self.d.rectangle((80,y,1530,y+h),outline=BLUE,width=3);self.svg.append(f'<rect x="80" y="{y}" width="1450" height="{h}" fill="none" stroke="{BLUE}" stroke-width="3"/>');self.vertex(id,'',80,y,1450,h,'shape=umlFrame;fillColor=none;strokeColor='+BLUE+';')
        self.txt(800,y+15,label,26,True,width=1300,bg=True)
        for yy in dividers:self.line([(80,yy),(1530,yy)],dash=True)
    def msg(self,id,s,y,ret=False):
        pts=[(1400,y),(200,y)] if ret else [(200,y),(1400,y)];self.line(pts,True,ret,native=False)
        label=f'{id}  {s}';count=len(self.wrap(label,1120,26))
        self.txt(800,y-10-(count+1)*26*1.18/2,label,26,width=1120,bg=True)
        self.edges.append(dict(id=id,source='system' if ret else 'actor',target='actor' if ret else 'system',label=s,points=pts,return_message=ret))
        self.vertex(id+'_a','',199.5,y-.5,1,1,'opacity=0;strokeColor=none;fillColor=none;');self.vertex(id+'_s','',1399.5,y-.5,1,1,'opacity=0;strokeColor=none;fillColor=none;')
        c=ET.SubElement(self.root,'mxCell',id=id,value='',edge='1',parent='1',source=id+('_s' if ret else '_a'),target=id+('_a' if ret else '_s'),style='edgeStyle=none;exitX=0.5;exitY=0.5;entryX=0.5;entryY=0.5;endArrow=open;strokeColor='+BLUE+';'+('dashed=1;' if ret else ''));g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});ET.SubElement(g,'mxPoint',x=str(pts[0][0]),y=str(y),attrib={'as':'sourcePoint'});ET.SubElement(g,'mxPoint',x=str(pts[1][0]),y=str(y),attrib={'as':'targetPoint'})
def build_ssd01():
    p=SSD('UC-01','A','UC-01 — read-only quote dialogue','2.11A','Customer')
    p.msg('01S-M01','browseHubs()',245);p.msg('01S-R01','activeHubsWithLoadAndCapacity',330,True)
    p.msg('01S-M02','selectHub(hubId)',445);p.msg('01S-R02','availableMenuAndOwnAddresses | refusal',530,True)
    p.frame('01S-loop','loop [Customer requests a fresh quote / corrects input / selects a suggested hub]',600,460)
    p.msg('01S-M03','requestQuote(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?)',760)
    p.msg('01S-R03','quoteWithFingerprintAndSDFQT | refusal | busySuggestions',875,True)
    p.txt(800,995,'Eligible quote → review full fingerprint + T; ONLINE approve/decline choice precedes Part B.\nBusy suggestions state menu may differ; empty list allowed; another hub needs a new quote.',26,width=1320);a=p.export()
    p=SSD('UC-01','B','UC-01 — checkout and guarded results','2.11B','Customer')
    p.msg('01S-M04','confirmCheckout(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod,\nonlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken)',295)
    p.frame('01S-alt','alt [mutually exclusive checkout result]',360,720,dividers=[515,635,755,875])
    p.txt(800,405,'[own token already exists] — no authorization or second insertion',26,width=1250);p.msg('01S-R04a','existingOrder (MG02)',485,True)
    p.txt(800,535,'[unused token, eligible, unchanged consent, COD or approved ONLINE, commit succeeds]',26,width=1250);p.msg('01S-R04b','placedOrderAndReceipt (PC01–PC06)',605,True)
    p.txt(800,655,'[unused token, active/valid request but load ≥ capacity]',26,width=1250);p.msg('01S-R04c','busySuggestions; nothing saved (MG03 / MG01)',725,True)
    p.txt(800,775,'[unused token, otherwise eligible, fingerprint OR T differs]',26,width=1250);p.msg('01S-R04d','revisedQuote; nothing saved (MG01)',845,True)
    p.txt(800,905,'[all other outcomes: foreign/invalid token or guard, ONLINE decline, lock/write/commit failure]',26,width=1280);p.msg('01S-R04e','refusal; no new order/payment/line; release authorization on rollback (MG01)',1025,True)
    b=p.export()
    p=SSD('UC-01','C','UC-01 — receipt and supporting order actions','2.11C','Customer')
    p.frame('01S-opt1','opt [Customer opens own receipt through SUC-03]',185,240);p.msg('01S-M05','viewReceipt(orderId)',285);p.msg('01S-R05','ownOrderReceipt | refusal',385,True)
    p.frame('01S-opt2','opt [Customer tracks own orders through SUC-03]',460,240);p.msg('01S-M06','viewMyOrders()',560);p.msg('01S-R06','ownOrdersAndOpenOffers',660,True)
    p.frame('01S-opt3','opt [SUC-04 extension: cancel requested at order action selected]',735,350);p.msg('01S-M07','cancelOrder(orderId)',845);p.msg('01S-R07','cancelledOrderAndAmounts | refusal',950,True)
    p.txt(800,1020,'[own PLACED / CONFIRMED] → CANCELLED + offer WITHDRAWN + BR-17 full C\n[otherwise] → refusal, zero lifecycle rows changed; no revival; no payout claim.',26,width=1260)
    return [a,b,p.export()]
def build_ssd05():
    p=SSD('UC-05','A','UC-05 — kitchen black-box operations','2.19A','Kitchen staff')
    p.msg('05S-M01','viewKitchenOrders()',230);p.msg('05S-R01','ownHubOrdersAndOffers',305,True);p.msg('05S-M02','viewKitchenOrder(orderId)',405);p.msg('05S-R02','ownHubOrderAndLines | refusal',480,True)
    p.frame('05S-alt','alt [staff selects one command; active own-hub PLACED is rechecked]',530,590,dividers=[755,945])
    p.txt(800,585,'[confirm selected; no open offer required]',26,width=1250);p.msg('05S-M03','confirmOrder(orderId)',660);p.msg('05S-R03','confirmedOrder | refusal',730,True)
    p.txt(800,775,'[reject selected; reason required; any open offer withdrawn]',26,width=1250);p.msg('05S-M04','rejectOrder(orderId, reason)',850);p.msg('05S-R04','rejectedOrder | refusal',920,True)
    p.txt(800,965,'[offer selected; §3.3 source/target/no-open-offer guards required]',26,width=1250);p.msg('05S-M05','offerReplacement(orderId, orderLineId, targetItemId)',1040);p.msg('05S-R05','offeredReplacement | refusal',1110,True);a=p.export()
    p=SSD('UC-05','B','UC-05 — separate SUC-03 acceptance response','2.19B','Customer')
    p.msg('05S-M06','viewMyOrders()',230);p.msg('05S-R06','ownOrdersAndOpenOffers',305,True);p.msg('05S-M07','viewReplacement(orderId)',400);p.msg('05S-R07','originalAndOfferedLineQuantityTotalRefundOwed | refusal',480,True)
    p.frame('05S-answer','opt [Customer selects ACCEPT after seeing proposed amounts]',535,555)
    p.msg('05S-M08','acceptReplacement(orderId, offerId)',635)
    p.frame('05S-result','alt [accept result; eligible = own PLACED + exact open OFFERED]',690,400,dividers=[810,905,1000])
    p.msg('05S-R08a','[eligible + valid target + committed] acceptedOrderAndAmounts (PC04)',790,True);p.msg('05S-R08b','[eligible + invalid target + committed] withdrawnOfferAndReason (MG01)',885,True);p.msg('05S-R08c','[ineligible owner / state / offer] staleRefusal; zero changes (MG01)',980,True);p.msg('05S-R08d','[eligible; save fails] controlledFailure; rollback, no changes (MG01)',1075,True)
    b=p.export()
    p=SSD('UC-05','C','UC-05 — separate SUC-03 decline response','2.19C','Customer')
    p.txt(800,225,'C1–C2: same offer/amounts as Part B. Eligible = own PLACED + exact open OFFERED.\nCommitted: DECLINED + REJECTED; COD VOIDED / ONLINE full C owed (BR-17).',26,width=1320)
    p.frame('05S-decline','opt [Customer selects DECLINE]',330,735)
    p.msg('05S-M09','declineReplacement(orderId, offerId)',465)
    p.frame('05S-decline-results','alt [exclusive decline result]',530,500,dividers=[710,865])
    p.msg('05S-R09','[eligible + committed] rejectedOrderAndAmounts (BR-17)',675,True)
    p.msg('05S-R09b','[ineligible owner / state / offer] staleRefusal; zero changes (MG01)',825,True)
    p.msg('05S-R09c','[eligible; save fails] controlledFailure; rollback, no changes (MG01)',980,True)
    return [a,b,p.export()]
def aliases(uc,kind,pages):
    out=R/'models'/uc;stem=f'{kind}_uc{uc[-2:]}'
    combined=ET.Element('mxfile',host='SaigonBite analysis',type='device')
    for page in pages:combined.append(ET.parse(out/(page['figure'] and (stem+'_Part'+chr(65+pages.index(page)))+'.drawio')).getroot().find('diagram'))
    ET.ElementTree(combined).write(out/(stem+'.drawio'),encoding='utf-8',xml_declaration=True)
    for suffix in ['png','svg']:shutil.copyfile(out/(stem+'_PartA.'+suffix),out/(stem+'.'+suffix))
    (out/(stem+'.json')).write_text(json.dumps({'author':AUTHOR,'main_image':'Part A alias; editable base contains every page','parts':pages},indent=2),encoding='utf-8')
def main():
    S.mkdir(parents=True,exist_ok=True)
    groups=[('UC-01','activity',build_activity01()),('UC-05','activity',build_activity05()),('UC-01','ssd',build_ssd01()),('UC-05','ssd',build_ssd05())]
    for uc,kind,pages in groups:aliases(uc,kind,pages)
    owned=Path(__file__)
    for uc,kind,_ in groups:
        dest=R/'models'/uc/f'{kind}_uc{uc[-2:]}.py'
        if dest!=owned:shutil.copyfile(owned,dest)
        for p in (R/'models'/uc).glob(f'{kind}_uc{uc[-2:]}_Part*.json'):shutil.copyfile(owned,p.with_suffix('.py'))
    log={'groups':[{ 'UC':uc,'kind':kind,'pages':len(pages),'figures':[p['figure'] for p in pages]} for uc,kind,pages in groups],'checks':'XML parse; connected source/target IDs; every decision exit guarded; minimum 10.59 pt at 230 mm; generated PNG via PIL; independent SVG render pending','pages':[p for _,_,pages in groups for p in pages]}
    (S/'generation_qa.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    print('Built',sum(len(pages) for _,_,pages in groups),'readable pages')
if __name__=='__main__':main()
