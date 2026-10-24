"""Owned P2-G renderer. Reuses read-only sm_order.py XML/SVG primitive conventions.
JSON -> editable draw.io / independent Pillow PNG / SVG; hidden Edge SVG QA.
"""
from pathlib import Path
import sys,json,math,subprocess,xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
W,H,FONT=1100,760,16
BLUE='#004387'; INK='#1B1B1B'; RED='#B03A2E'
SCR=Path('D:/RAD/FINAL/Part2/notes/P2-G'); EDGE=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'
class Canvas:
 def __init__(self,title):
  self.im=Image.new('RGB',(W*2,H*2),'white');self.d=ImageDraw.Draw(self.im);self.errors=[];self.nodes={};self.edges=[]
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1100" height="760" fill="white"/>']
  self.model=ET.Element('mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H));self.root=ET.SubElement(self.model,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0')
  self.text('title',title,550,25,20,True);self.text('author',AUTHOR,550,742,16,True)
 def font(self,size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/arial'+('bd' if bold else '')+'.ttf',size*2)
 def cell(self,id,label,box,style):
  if id in self.nodes:raise ValueError(id)
  self.nodes[id]=box
  c=ET.SubElement(self.root,'mxCell',id=id,value=label,style='html=0;whiteSpace=wrap;fontFamily=Arial;fontSize=16;fontColor='+INK+';'+style,vertex='1',parent='1');ET.SubElement(c,'mxGeometry',x=str(box[0]),y=str(box[1]),width=str(box[2]),height=str(box[3]),attrib={'as':'geometry'})
 def text(self,id,s,x,y,size=16,bold=False,color=INK,box=None,cell=True):
  lines=s.split('\n');lh=size+4;y0=y-(len(lines)-1)*lh/2
  if box:
   f=self.font(size,bold)
   if max(f.getlength(q)/2 for q in lines)>box[2]-8:self.errors.append('text width '+id)
   if len(lines)*lh>box[3]:self.errors.append('text height '+id)
  for j,line in enumerate(lines):
   yy=y0+j*lh
   self.d.text((x*2,yy*2),line,font=self.font(size,bold),fill=color,anchor='mm')
   self.svg.append(f'<text x="{x}" y="{yy+size*.34}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="middle" fill="{color}">{escape(line)}</text>')
  if cell:
   tw=max(self.font(size,bold).getlength(q)/2 for q in lines)+12;th=len(lines)*lh+8
   self.cell(id,s,box or [x-tw/2,y-th/2,tw,th],f'text;strokeColor=none;fillColor=none;fontSize={size};fontStyle={1 if bold else 0};')
 def rect(self,id,s,x,y,w,h,fill='white',color=BLUE,rounded=False,cell=True):
  b=[x,y,x+w,y+h];self.d.rounded_rectangle([v*2 for v in b],radius=16 if rounded else 0,fill=fill,outline=color,width=3)
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{8 if rounded else 0}" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
  if cell:self.cell(id,s,[x,y,w,h],f'rounded={1 if rounded else 0};fillColor={fill};strokeColor={color};strokeWidth=1.5;')
  if s:self.text(id+'_label',s,x+w/2,y+h/2,box=[x,y,w,h],cell=False)
 def diamond(self,id,s,x,y,w=100,h=60):
  pts=[(x,y-h/2),(x+w/2,y),(x,y+h/2),(x-w/2,y)]
  self.d.polygon([(a*2,b*2) for a,b in pts],fill='white',outline=BLUE,width=3)
  self.svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+f'" fill="white" stroke="{BLUE}" stroke-width="1.5"/>')
  self.cell(id,s,[x-w/2,y-h/2,w,h],'rhombus;fillColor=white;strokeColor='+BLUE+';')
  if s:self.text(id+'_label',s,x,y,cell=False)
 def circle(self,id,x,y,final=False):
  r=12;self.d.ellipse(((x-r)*2,(y-r)*2,(x+r)*2,(y+r)*2),fill='white' if final else BLUE,outline=BLUE,width=3)
  self.svg.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{"white" if final else BLUE}" stroke="{BLUE}" stroke-width="1.5"/>')
  if final:
   self.d.ellipse(((x-7)*2,(y-7)*2,(x+7)*2,(y+7)*2),fill=BLUE);self.svg.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{BLUE}"/>')
  self.cell(id,'',[x-r,y-r,24,24],('shape=endState;' if final else 'ellipse;')+'fillColor='+BLUE+';strokeColor='+BLUE+';')
 def line(self,id,pts,source=None,target=None,dashed=False,arrow=True,label='',labelxy=None):
  for a,b in zip(pts,pts[1:]):
   if dashed:
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    for i in range(0,int(length),12):
     j=min(i+6,length);self.d.line(((a[0]+dx*i/length)*2,(a[1]+dy*i/length)*2,(a[0]+dx*j/length)*2,(a[1]+dy*j/length)*2),fill=BLUE,width=3)
   else:self.d.line([a[0]*2,a[1]*2,b[0]*2,b[1]*2],fill=BLUE,width=3)
  self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{BLUE}" stroke-width="1.5"'+(' stroke-dasharray="6 6"' if dashed else '')+'/>')
  if arrow:
   a,b=pts[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);pp=[b,(b[0]-10*math.cos(ang-.4),b[1]-10*math.sin(ang-.4)),(b[0]-10*math.cos(ang+.4),b[1]-10*math.sin(ang+.4))]
   self.d.polygon([(x*2,y*2) for x,y in pp],fill=BLUE);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pp)+f'" fill="{BLUE}"/>')
  if source:
   assert source in self.nodes and target in self.nodes,(source,target)
   style='edgeStyle=none;rounded=0;strokeColor='+BLUE+';strokeWidth=1.5;endArrow='+('block' if arrow else 'none')+';'+('dashed=1;' if dashed else '')
   for pref,nid,pt in [('exit',source,pts[0]),('entry',target,pts[-1])]:
    x,y,w,h=self.nodes[nid];style+=f'{pref}X={(pt[0]-x)/w};{pref}Y={(pt[1]-y)/h};{pref}Perimeter=0;'
   c=ET.SubElement(self.root,'mxCell',id=id,value='',style=style,edge='1',parent='1',source=source,target=target)
   g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});arr=ET.SubElement(g,'Array',attrib={'as':'points'})
   for x,y in pts[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
   self.edges.append({'id':id,'source':source,'target':target,'guard':label})
  else:
   a,b=pts[0],pts[-1];vertical=a[0]==b[0]
   self.cell(id+'_decoration','',[min(a[0],b[0]),min(a[1],b[1]),max(1,abs(b[0]-a[0])),max(1,abs(b[1]-a[1]))],'shape=line;'+('direction=south;' if vertical else '')+'strokeColor='+BLUE+';strokeWidth=1.5;fillColor=none;'+('dashed=1;' if dashed else ''))
  if label:self.text(id+'_guard',label,*labelxy,size=16)
 def frame(self,id,label,y,h):
  self.rect(id,'',65,y,975,h,fill='white');self.text(id+'_label',label,550,y+14,16,True)
 def finish(self,target,p):
  if self.errors:raise ValueError((target,self.errors))
  self.svg.append('</svg>');target.with_suffix('.svg').write_text(''.join(self.svg),encoding='utf-8');self.im.save(target.with_suffix('.png'))
  mx=ET.Element('mxfile',host='SaigonBite P2-G',version='24.7.17');d=ET.SubElement(mx,'diagram',name=p['title'],id=target.stem);d.append(self.model);ET.ElementTree(mx).write(target.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
  proof=SCR/(target.stem+'_svg.png')
  run=subprocess.run([str(EDGE),'--headless','--disable-gpu','--hide-scrollbars','--no-first-run','--force-device-scale-factor=2',f'--user-data-dir={SCR/("edge_"+target.stem)}',f'--screenshot={proof}','--window-size=1100,760',target.with_suffix('.svg').as_uri()],capture_output=True,text=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
  (SCR/(target.stem+'_edge.log')).write_text(run.stderr,encoding='utf-8')
  assert run.returncode==0 and proof.exists(),run.stderr
  return {'stem':target.stem,'canvas':[W,H],'placed_width_mm':230,'minimum_font_px':16,'minimum_pt':16*230/25.4*72/W,'connected_edges':self.edges,'nodes':list(self.nodes),'svg_proof':str(proof),'png':str(target.with_suffix('.png'))}

def activity(p,target):
 c=Canvas(p['title']);pre=p['prefix']
 c.rect('admin_lane','',20,60,310,665,fill='#F3F7FA');c.rect('system_lane','',330,60,750,665,fill='#FFFFFF')
 c.text('admin_header','Admin',175,80,18,True);c.text('system_header',':System',705,80,18,True)
 c.circle(pre+'-start',175,113)
 c.rect(pre+'-browse',p['browse'],40,145,270,66,rounded=True)
 c.rect(pre+'-read',p['read'],385,145,640,66,rounded=True)
 c.diamond(pre+'-choice','Next?',175,320,120,70)
 c.rect(pre+'-inspect','Read-only inspection\nNo persistent rows changed',385,285,640,70,rounded=True)
 c.rect(pre+'-request',p['request'],40,408,270,90,rounded=True)
 c.rect(pre+'-validate',p['validate'],385,403,640,90,rounded=True)
 c.diamond(pre+'-valid','Saved?',705,535,120,60)
 c.rect(pre+'-save',p['save'],365,584,345,64,rounded=True)
 c.rect(pre+'-refuse',p['refuse'],755,584,305,64,fill='#FBEDEB',color=RED,rounded=True)
 c.diamond(pre+'-merge','',705,690,26,26)
 c.rect(pre+'-observe','Observe result; finish',40,644,270,42,rounded=True);c.circle(pre+'-final',175,704,True)
 es=[('start','browse',[(175,125),(175,145)],'',None),('browse','read',[(310,178),(385,178)],'',None),('read','choice',[(705,211),(705,250),(175,250),(175,285)],'',None),('choice','inspect',[(235,320),(385,320)],'[inspect only]',(310,291)),('choice','request',[(175,355),(175,408)],'[maintain]',(235,380)),('request','validate',[(310,450),(385,450)],'',None),('validate','valid',[(705,493),(705,505)],'',None),('valid','save',[(645,535),(535,535),(535,584)],'[guards pass;\nsave completes]',(440,555)),('valid','refuse',[(765,535),(908,535),(908,584)],'[else]',(950,557)),('save','merge',[(535,648),(535,690),(692,690)],'',None),('refuse','merge',[(908,648),(908,670),(705,670),(705,677)],'',None),('inspect','merge',[(1025,320),(1070,320),(1070,690),(718,690)],'',None),('merge','observe',[(705,703),(705,715),(335,715),(335,665),(310,665)],'',None),('observe','final',[(175,686),(175,692)],'',None)]
 for i,(s,t,pts,l,xy) in enumerate(es):c.line(pre+'-e'+str(i),pts,pre+'-'+s,pre+'-'+t,label=l,labelxy=xy)
 c.text('legend',p['legend'],550,52,16)
 return c.finish(target,p)

def ssd(p,target):
 c=Canvas(p['title'])
 c.frame('loop','loop [inspect; getHub only if a hub is selected; zero writes]' if len(p['queries'])>1 else 'loop [each inspection request; zero writes]',105,145)
 c.frame('opt','opt [Admin chooses one maintenance request]',260,425)
 c.frame('commands','alt '+p['commands'][0]['guard'],295,225)
 for y,cmd in zip([309,384,459],p['commands']):
  if y>309:
   c.line('divider'+str(y),[(65,y-14),(1040,y-14)],arrow=False);c.text('guard'+str(y),cmd['guard'],550,y,16,True)
 c.frame('outcome','alt [all selected-command guards pass; save completes]',530,150)
 c.line('outcome_divider',[(65,610),(1040,610)],arrow=False);c.text('else_guard','[else: invalid, stale, denied or save failed]',550,624,16,True)
 # Lifelines are editable vertices; every message connects them by source/target.
 c.rect('actor','Admin',75,62,110,32);c.rect('system',':System',905,62,130,32)
 c.cell('actor_lifeline','',[129,94,2,591],'strokeColor=none;fillColor=none;');c.cell('system_lifeline','',[969,94,2,591],'strokeColor=none;fillColor=none;')
 c.line('actor_dash',[(130,94),(130,685)],dashed=True,arrow=False);c.line('system_dash',[(970,94),(970,685)],dashed=True,arrow=False)
 def msg(id,call,y,ret=None):
  c.text(id+'_text',id+'  '+call,550,y-(24 if '\n' in call else 14),16)
  c.line(id,[(130,y),(970,y)],'actor_lifeline','system_lifeline')
  if ret:
   c.text(id+'_return_text',ret,550,y+14,16);c.line(id+'_return',[(970,y+28),(130,y+28)],'system_lifeline','actor_lifeline',dashed=True)
 if len(p['queries'])==1:
  q=p['queries'][0];msg(q['id'],q['call'],165,q['return'])
 else:
  for q,y in zip(p['queries'],[155,212]):msg(q['id'],q['call'],y,q['return'])
 for cmd,y in zip(p['commands'],[360,435,510]):msg(cmd['id'],cmd['call'],y)
 c.text('success','savedRecord',550,572,16);c.line('saved',[(970,588),(130,588)],'system_lifeline','actor_lifeline',dashed=True)
 c.text('failure','controlledRefusal; no change',550,652,16);c.line('refused',[(970,668),(130,668)],'system_lifeline','actor_lifeline',dashed=True)
 c.text('note',p['note'],550,710,16)
 return c.finish(target,p)

def build(spec_path):
 spec_path=Path(spec_path);data=json.loads(spec_path.read_text(encoding='utf-8'));logs=[]
 for p in data['pages']:logs.append((activity if p['type']=='activity' else ssd)(p,spec_path.parent/p['stem']))
 # Base editable source holds all pages; base visual alias is first-page only.
 if len(data['pages'])>1 and spec_path.stem==data['base']:
  mx=ET.Element('mxfile',host='SaigonBite P2-G')
  for p in data['pages']:
   child=ET.parse(spec_path.parent/(p['stem']+'.drawio')).getroot().find('diagram');mx.append(child)
  ET.ElementTree(mx).write(spec_path.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
  for ext in ['.png','.svg']:spec_path.with_suffix(ext).write_bytes((spec_path.parent/(data['pages'][0]['stem']+ext)).read_bytes())
 (SCR/(spec_path.stem+'_qa.json')).write_text(json.dumps(logs,indent=2),encoding='utf-8')
 print(json.dumps([{'stem':x['stem'],'minimum_pt':round(x['minimum_pt'],2),'edges':len(x['connected_edges'])} for x in logs]))
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');build(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.json'))
