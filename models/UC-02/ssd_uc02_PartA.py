"""Owned renderer, adapted from read-only sm_order.py primitives and proc_* style.
One explicit geometry produces editable mxGraph XML, SVG and Pillow PNG.
Edge headless independently renders each SVG to scratch for comparison.
"""
from pathlib import Path
import json, math, sys, subprocess, xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont
sys.dont_write_bytecode=True
ROOT=Path('D:/RAD/FINAL/SaigonBite'); SCRATCH=Path('D:/RAD/FINAL/Part2/notes/P2-F')
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'
BLUE='#004387'; INK='#1B1B1B'; RED='#B03A2E'; W=1100; H=900; FS=18
EDGE=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')

class Canvas:
 def __init__(self,title):
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1100" height="900" fill="white"/>']
  self.im=Image.new('RGB',(W*2,H*2),'white'); self.d=ImageDraw.Draw(self.im)
  self.mx=ET.Element('mxfile',host='SaigonBite P2'); dia=ET.SubElement(self.mx,'diagram',name=title,id='page1'); model=ET.SubElement(dia,'mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H));self.r=ET.SubElement(model,'root');ET.SubElement(self.r,'mxCell',id='0');ET.SubElement(self.r,'mxCell',id='1',parent='0')
  self.boxes={};self.edges=[];self.errors=[];self.serial=0
  self.text('title',title,20,12,1060,42,22,True,BLUE)
  self.text('author',AUTHOR,20,850,1060,28,18,True,BLUE)
 def cell(self,id,label,box,style):
  c=ET.SubElement(self.r,'mxCell',id=id,value=label,style=style,vertex='1',parent='1');x,y,w,h=box;ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
 def text(self,id,label,x,y,w,h,size=FS,bold=False,color=INK,mx=True):
  f=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',size*2)
  lines=label.split('\n');lh=size+4
  if any(f.getlength(s)/2>w-4 for s in lines) or len(lines)*lh>h+2:self.errors.append('text overflow '+id)
  yy=y+h/2-(len(lines)-1)*lh/2
  for i,s in enumerate(lines):
   cy=yy+i*lh;self.d.text(((x+w/2)*2,cy*2),s,font=f,fill=color,anchor='mm')
   self.svg.append(f'<text x="{x+w/2}" y="{cy+size*.34}" text-anchor="middle" font-family="Arial" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{color}">{escape(s)}</text>')
  if mx:self.cell(id,label,(x,y,w,h),f'text;html=0;whiteSpace=wrap;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};align=center;verticalAlign=middle;strokeColor=none;fillColor=none;')
 def line(self,pts,color=BLUE,dash=False,width=2):
  self.svg.append('<polyline points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
  for a,b in zip(pts,pts[1:]):
   if dash:
    dist=math.dist(a,b);n=max(1,int(dist/12))
    for k in range(n):
     t=k/n;u=min(1,t+0.55/n);self.d.line([(2*(a[0]+(b[0]-a[0])*q),2*(a[1]+(b[1]-a[1])*q)) for q in [t,u]],fill=color,width=width*2)
   else:self.d.line([(x*2,y*2) for x,y in [a,b]],fill=color,width=width*2)
 def rect(self,id,label,x,y,w,h,kind='action',color=BLUE):
  self.boxes[id]=(x,y,w,h)
  if kind in ['initial','final']:
   self.svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{color if kind=="initial" else "white"}" stroke="{color}" stroke-width="2"/>')
   self.d.ellipse((x*2,y*2,(x+w)*2,(y+h)*2),fill=color if kind=='initial' else 'white',outline=color,width=4)
   if kind=='final':
    self.svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2-6}" ry="{h/2-6}" fill="{color}"/>');self.d.ellipse(((x+6)*2,(y+6)*2,(x+w-6)*2,(y+h-6)*2),fill=color)
   style='ellipse;' if kind=='initial' else 'shape=endState;'
  elif kind in ['decision','merge']:
   pts=[(x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)]
   self.svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+f'" fill="white" stroke="{color}" stroke-width="2"/>');self.d.polygon([(a*2,b*2) for a,b in pts],fill='white',outline=color,width=4);style='rhombus;'
  else:
   fill='#FFFBE6' if kind=='note' else 'white';rx=0 if kind in ['note','frame','head'] else 12
   self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="2"/>');self.d.rounded_rectangle((x*2,y*2,(x+w)*2,(y+h)*2),radius=rx*2,fill=fill,outline=color,width=4);style='rounded=1;' if rx else 'rounded=0;'
  self.cell(id,label,(x,y,w,h),style+f'html=0;whiteSpace=wrap;strokeColor={color};fillColor=white;fontSize={FS};align=center;verticalAlign=middle;')
  if label:self.text(id+'_txt',label,x+5,y+3,w-10,h-6,mx=False)
 def edge(self,id,src,dst,pts,dash=False,label='',labelbox=None,color=BLUE,openarrow=False):
  assert src in self.boxes and dst in self.boxes,(src,dst)
  self.edges.append({'id':id,'source':src,'target':dst,'points':pts,'dashed':dash,'label':label})
  self.line(pts,color,dash)
  a,b=pts[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);arrow=[b,(b[0]-11*math.cos(ang-.4),b[1]-11*math.sin(ang-.4)),(b[0]-11*math.cos(ang+.4),b[1]-11*math.sin(ang+.4))]
  self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in arrow)+f'" fill="{color}"/>');self.d.polygon([(x*2,y*2) for x,y in arrow],fill=color)
  c=ET.SubElement(self.r,'mxCell',id=id,value='',edge='1',parent='1',source=src,target=dst,style=f'edgeStyle=none;html=0;endArrow=block;strokeColor={color};'+('dashed=1;' if dash else ''))
  g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});ar=ET.SubElement(g,'Array',attrib={'as':'points'})
  for x,y in pts[1:-1]:ET.SubElement(ar,'mxPoint',x=str(x),y=str(y))
  if label:
   x,y,w,h=labelbox;self.text(id+'_guard',label,x,y,w,h,18,True,color)
 def save(self,path,spec):
  if path.stem != Path(__file__).stem: return {'skipped': path.stem}
  if self.errors:raise ValueError(self.errors)
  path.with_suffix('.png').parent.mkdir(parents=True,exist_ok=True);self.im.save(path.with_suffix('.png'));path.with_suffix('.svg').write_text(''.join(self.svg)+'</svg>',encoding='utf-8');ET.ElementTree(self.mx).write(path.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
  spec.update({'nodes':self.boxes,'edges':self.edges,'canvas':[W,H],'minimum_font_px':FS,'placed_width_mm':230,'minimum_pt':round(FS*230/25.4*72/W,2),'author':AUTHOR});path.with_suffix('.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
  ET.parse(path.with_suffix('.drawio'))
  return {'stem':path.stem,'nodes':len(self.boxes),'edges':len(self.edges),'minimum_pt':spec['minimum_pt'],'text_overflow':self.errors,'xml':'parsed','connected_edges':True}

def activity(uc,part,title,actor,request,guard,effect,result,note):
 c=Canvas(f'UC-{uc} activity — Part {part}: {title}')
 c.rect('ActorLane','',20,85,340,755,'frame');c.rect('SystemLane','',360,85,720,755,'frame');c.text('actorname',actor,25,90,330,30,20,True,BLUE);c.text('systemname','System',365,90,710,30,20,True,BLUE)
 c.rect('I','',165,135,30,30,'initial');c.rect('A_request',request,40,190,280,110);c.rect('D_valid',guard,465,155,370,180,'decision');c.rect('S_effect',effect,465,365,370,150)
 c.rect('D_commit','Operation\nsucceeds?',565,545,170,90,'decision');c.rect('S_refuse','Refuse; no changes\n'+('MG01 / E01–E05' if uc=='02' else 'MG01/02 / E01–02'),865,355,200,110,color=RED)
 c.rect('S_rollback',('Rollback command\nNo partial changes\nMG01 / E06' if uc=='02' else 'Read unavailable\nNo fabricated result\nMG01 / E03'),850,590,215,100,color=RED)
 c.rect('A_result',result,40,650,280,90);c.rect('M_end','',632,755,36,36,'merge');c.rect('F','',634,805,32,32,'final');c.rect('N',note,35,365,290,215,'note')
 c.edge('e1','I','A_request',[(180,165),(180,190)]);c.edge('e2','A_request','D_valid',[(320,245),(465,245)])
 c.edge('e3','D_valid','S_effect',[(650,335),(650,365)],label='[valid]',labelbox=(655,337,100,26))
 c.edge('e4','D_valid','S_refuse',[(835,245),(965,245),(965,355)],label='[invalid]',labelbox=(835,258,120,26),color=RED)
 c.edge('e5','S_effect','D_commit',[(650,515),(650,545)])
 c.edge('e6','D_commit','A_result',[(565,590),(380,590),(380,695),(320,695)],label='[yes]',labelbox=(408,595,90,26))
 c.edge('e7','D_commit','S_rollback',[(735,590),(795,590),(795,640),(850,640)],label='[no]',labelbox=(747,599,65,26),color=RED)
 c.edge('e8','S_refuse','M_end',[(965,465),(1080,465),(1080,773),(668,773)],color=RED)
 c.edge('e9','S_rollback','M_end',[(957,690),(957,730),(650,730),(650,755)],color=RED)
 c.edge('e10','A_result','M_end',[(180,740),(180,773),(632,773)])
 c.edge('e11','M_end','F',[(650,791),(650,805)])
 c.text('scope','Scoped activity episodes: pickup / finish or one report; final ends this episode, not other requests.',15,58,1070,26,18,False,BLUE)
 p=ROOT/f'models/UC-{uc}/activity_uc{uc}_Part{part}';return c.save(p,{'type':'activity','part':part,'guard_definition':'valid = every condition written in D_valid holds; invalid = its logical complement','flow_notes':note})

def ssd(uc,part,title,actor,rows,frames,notes):
 c=Canvas(f'UC-{uc} SSD'+(f' — Part {part}: ' if part else ' — ')+title)
 c.rect('Actor',actor,100,95,250,55,'head');c.rect('System',':System',750,95,250,55,'head')
 c.line([(225,150),(225,790)],dash=True);c.line([(875,150),(875,790)],dash=True)
 for i,(x,y,w,h,label) in enumerate(frames):
  c.rect(f'frame{i}','',50,y,1000,h,'frame');c.text(f'frametext{i}',label,55,y+2,990,26,18,True,BLUE)
 if uc=='02' and part=='B':
  c.line([(50,415),(1050,415)],dash=True);c.text('operand2','[unable to deliver; reason required]',65,425,970,28,18,True,BLUE)
 elif uc=='04':
  c.rect('altframe','',70,220,960,530,'frame');c.text('altlabel','alt [sales]',80,224,940,26,18,True,BLUE)
  for yy,label in [(365,'[workload now]'),(555,'[delivery performance]')]:
   c.line([(70,yy),(1030,yy)],dash=True);c.text('operand'+str(yy),label,80,yy+4,940,26,18,True,BLUE)
 for id,y,call,ret in rows:
  # Invisible native anchor cells give every message a concrete lifeline endpoint.
  for who,x in [('a',225),('s',875)]:
   for suf,yy in [('',y),('r',y+34)]:c.boxes[id+who+suf]=(x-1,yy-1,2,2);c.cell(id+who+suf,'',(x-1,yy-1,2,2),'opacity=0;strokeOpacity=0;fillOpacity=0;')
  c.edge(id,id+'a',id+'s',[(225,y),(875,y)]);c.text(id+'_label',id+' '+call,240,y-27,620,25)
  c.edge(id+'r',id+'sr',id+'ar',[(875,y+34),(225,y+34)],dash=True);c.text(id+'_return',ret,245,y+36,610,26,18,False,BLUE)
 c.text('notes',notes,20,795,1060,48,18)
 p=ROOT/f'models/UC-{uc}/ssd_uc{uc}'+Path('') if False else ROOT/f'models/UC-{uc}/ssd_uc{uc}{"_Part"+part if part else ""}'
 return c.save(p,{'type':'ssd','rows':[{'message_id':id,'call':call,'return':ret} for id,y,call,ret in rows],'fragments':frames,'notes':notes})

def main():
 qa=[]
 qa.append(activity('02','A','inspect and claim','Shipper','1–3: Browse, inspect,\nthen takeDelivery(orderId)','Active SHIPPER;\nREADY + unassigned\nAWAITING_PICKUP?','3: Atomic winner assigned\nDelivery PICKED_UP\nOrder OUT_FOR_DELIVERY\nSave picked_up_at — PC01','Read assignedDelivery\nContinue B or C later','1: viewReadyDeliveries()\n2: viewDelivery(orderId)\nRead-only contact snapshot;\nno passport.\nEmpty/no claim → end MG01.\nAny active shipper can claim;\nno concurrent-delivery cap.'))
 qa.append(activity('02','B','successful delivery','Shipper','4–5 / A01: Hand over;\nconfirmDelivered(orderId,\ncashCollected?)','Active assigned shipper;\nPICKED_UP +\nOUT_FOR_DELIVERY;\nCOD cash=T / ONLINE 0?','5: Atomic terminal save\nDelivery + Order DELIVERED\nCOD PAID, cash=T; ONLINE\nremains PAID; finish/close\nPC02; partial owed retained','6: Read delivered result\nRequest ends','Resume own assignment via\nsteps 1–2; bypass pickup.\nCOD takes exactly T.\nONLINE takes no cash.\nWrong shipper/cash/repeat\n→ MG01, 0 changed rows.'))
 qa.append(activity('02','C','failed delivery','Shipper','A02: Unable to deliver;\nreportFailure(orderId, reason)','Active assigned shipper;\nPICKED_UP +\nOUT_FOR_DELIVERY;\nnonempty reason?','A02: Atomic FAILED + reason\nOrder DELIVERY_FAILED\nfinish/close times\nCOD VOIDED; ONLINE\nREFUND_PENDING, owed=C\nPC03 — BR-17','6: Read failed result\nRequest ends','C = captured ONLINE amount.\nFull C replaces partial owed;\nnever C + partial.\nNo payout is claimed.\nWrong shipper / repeat\n→ MG01, 0 changed rows.'))
 qa.append(activity('04','A','operational sales','Manager','1–2: salesReport(startDateVN,\nendDateVN, hubId?)','Active MANAGER;\nvalid ordered dates;\nexisting optional hub?','2–3: VN [start,end+1) → UTC\nDELIVERED by finish time\nOrder-grain S,D,F−Q,T,owed\nNo line join; item ID groups\nInclude archive — PC01','4–5: Read sales / counts\nEnd or new request','Refunds owed separate from T;\nnever subtract twice.\nOperational, not accounting.\nEmpty counts/sums = 0.\nReport writes 0 rows MG01;\nnon-manager denied MG02.'))
 qa.append(activity('04','B','workload now','Manager','A01: workloadReport()','Active MANAGER?','A01: Hubs incl. archived\nCooking load = PLACED +\nCONFIRMED + PREPARING\nLoad / capacity; READY;\nOUT_FOR_DELIVERY — PC01\nLabel now + as-of time','5: Read current snapshot\nEnd or new request','No date / hub parameter.\nWorkload is not historical.\nEmpty hub set allowed.\n0 persistent writes MG01.\nNon-manager denied MG02.\nNo Report lifecycle exists.'))
 qa.append(activity('04','C','delivery performance','Manager','A02: deliveryReport(\nstartDateVN, endDateVN,\nhubId?)','Active MANAGER;\nvalid ordered dates;\nexisting optional hub?','A02: VN interval → UTC\nFinished DELIVERED + FAILED\nMean READY→pickup; Nwait\nMean pickup→success; Nride\nfailed / finished; Nfinished\nArchive included — PC01','5 / A03: Read metrics + N\nEmpty denominator → n/a\nPC02; end / new request','Wait: finished valid pairs.\nRide: successes only.\nShow each sample size N.\nMissing pair: no sample.\n0 writes MG01; deny MG02.\nNo scientific result claimed.'))
 qa.append(ssd('02','A','queries and atomic pickup','Shipper',[
 ('M01',230,'viewReadyDeliveries()','readyAndOwnAssignedDeliveries | refusal'),
 ('M02',365,'viewDelivery(orderId)','deliveryContactSnapshotAndCashDue | refusal'),
 ('M03',555,'takeDelivery(orderId)','assignedDelivery [valid winner] | refusal [otherwise]')],[(50,185,1000,265,'loop [browse / inspect again while needed; active SHIPPER]'),(50,485,1000,150,'opt [select unassigned READY order; bypass for own PICKED_UP]')], 'M03 result alt [winner] PC01 / [invalid, lost race, repeat, failure] MG01.\nQueries expose contact/address snapshot only; no passport; session identity is implicit.'))
 qa.append(ssd('02','B','exclusive finish outcomes','Shipper',[
 ('M04',235,'confirmDelivered(orderId, cashCollected?)','deliveredOrderAndPayment [valid] | refusal [otherwise]'),
 ('M05',530,'reportFailure(orderId, reason)','failedOrderAndPayment [valid] | refusal [otherwise]')],[(50,180,1000,510,'alt [successful handover: COD cash=T / ONLINE cash absent or 0]')], 'alt second operand [unable to deliver; nonempty reason] uses M05.\nEach result: alt [valid + atomic commit] PC02/PC03 / [otherwise] MG01; no payout.'))
 qa.append(ssd('04','','independent report requests','Manager',[
 ('M01',285,'salesReport(startDateVN, endDateVN, hubId?)','operationalSalesAndRefundsOwed | invalidFilter | denied'),
 ('M02',455,'workloadReport()','currentHubLoadCapacityReadyOutForDelivery | denied'),
 ('M03',650,'deliveryReport(startDateVN, endDateVN, hubId?)','waitRideFailureRatesWithNAndNA | invalidFilter | denied')],[(50,180,1000,590,'loop [another independently authorized report request]')], 'alt operands: [sales] M01 / [workload] M02 / [delivery performance] M03.\nAll branches read only MG01; non-manager denied MG02; empty metrics n/a with N=0.'))
 (SCRATCH/'activity_uc02_qa.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
 print(json.dumps(qa))
if __name__=='__main__': main()
