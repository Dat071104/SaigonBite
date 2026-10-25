from pathlib import Path
import json,csv,re,copy,math,subprocess,textwrap,xml.etree.ElementTree as ET,hashlib,sys,ast
from xml.sax.saxutils import escape
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
R=Path('D:/RAD/FINAL/SaigonBite'); SCR=Path('D:/RAD/FINAL/Part2/notes/P3-C'); AUTHOR='Author: 722I0004 · AI-assisted (Codex)'; W=1200; BLUE='#004387'; INK='#202A35'
MODEL=R/'models/shared/design_model.json'
def load():return json.loads(MODEL.read_text(encoding='utf-8'))
def wrap(s,n=78):return '\n'.join(textwrap.wrap(s,n,break_long_words=False,break_on_hyphens=False))
class Canvas:
 def __init__(self,title,h=850):
  self.h=h;self.im=Image.new('RGB',(W*2,h*2),'white');self.d=ImageDraw.Draw(self.im);self.nodes={};self.edges=[]
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}"><rect width="{W}" height="{h}" fill="white"/>']
  self.mx=ET.Element('mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(h)); self.root=ET.SubElement(self.mx,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0');self.text('title',title,600,26,22,True);self.text('author',AUTHOR,600,h-20,18,True)
 def font(self,s,b=False):return ImageFont.truetype('C:/Windows/Fonts/arial'+('bd' if b else '')+'.ttf',s*2)
 def cell(self,id,label,x,y,w,h,style=''):
  assert id not in self.nodes,id; self.nodes[id]=(x,y,w,h);c=ET.SubElement(self.root,'mxCell',id=id,value=label,vertex='1',parent='1',style='html=0;whiteSpace=wrap;fontFamily=Arial;'+style);ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
 def text(self,id,t,x,y,s=18,b=False,left=False):
  s=max(s,23) if self.h==1250 else s;lines=t.split('\n');lh=s+4
  for j,line in enumerate(lines):
   assert self.font(s,b).getlength(line)/2<1170,(id,line)
   yy=y+j*lh; self.d.text((x*2,yy*2),line,font=self.font(s,b),fill=INK,anchor='lm' if left else 'mm');self.svg.append(f'<text x="{x}" y="{yy+s*.34}" text-anchor="{"start" if left else "middle"}" font-family="Arial" font-size="{s}" font-weight="{"bold" if b else "normal"}">{escape(line)}</text>')
  width=max(self.font(s,b).getlength(l)/2 for l in lines)+10;self.cell(id,t,x if left else x-width/2,y-s/2,width,len(lines)*lh+4,f'text;strokeColor=none;fillColor=none;fontSize={s};fontStyle={1 if b else 0};align={"left" if left else "center"};verticalAlign=top;spacing=0;')
 def rect(self,id,x,y,w,h,fill='white',label=''):
  self.d.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=fill,outline=BLUE,width=3);self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{BLUE}" stroke-width="1.5"/>');self.cell(id,'',x,y,w,h,'fillColor='+fill+';strokeColor='+BLUE+';')
 def line(self,id,pts,s=None,t=None,dashed=False,arrow=True,label='',open_head=False):
  for a,b in zip(pts,pts[1:]):
   if dashed:
    dx=b[0]-a[0];dy=b[1]-a[1];ln=math.hypot(dx,dy)
    for k in range(0,int(ln),12):
     q=min(k+6,ln);self.d.line(((a[0]+dx*k/ln)*2,(a[1]+dy*k/ln)*2,(a[0]+dx*q/ln)*2,(a[1]+dy*q/ln)*2),fill=BLUE,width=3)
   else:self.d.line([(x*2,y*2) for x,y in [a,b]],fill=BLUE,width=3)
  self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{BLUE}" stroke-width="1.5"'+(' stroke-dasharray="6 6"' if dashed else '')+'/>')
  if arrow:
   a,b=pts[-2:];an=math.atan2(b[1]-a[1],b[0]-a[0]);p=[b,(b[0]-10*math.cos(an-.4),b[1]-10*math.sin(an-.4)),(b[0]-10*math.cos(an+.4),b[1]-10*math.sin(an+.4))];
   if open_head:
    v=[p[1],p[0],p[2]];self.d.line([(x*2,y*2) for x,y in v],fill=BLUE,width=3);self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in v)+f'" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
   else:self.d.polygon([(x*2,y*2) for x,y in p],fill=BLUE);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{BLUE}"/>')
  if s:
   assert s in self.nodes and t in self.nodes;(x,y,w,h)=self.nodes[s];a=pts[0];(xx,yy,ww,hh)=self.nodes[t];b=pts[-1]
   st=f'edgeStyle=none;endArrow={"open" if open_head else "block" if arrow else "none"};dashed={int(dashed)};strokeColor={BLUE};exitX={(a[0]-x)/w};exitY={(a[1]-y)/h};entryX={(b[0]-xx)/ww};entryY={(b[1]-yy)/hh};exitPerimeter=0;entryPerimeter=0;'
   e=ET.SubElement(self.root,'mxCell',id=id,value=label,edge='1',parent='1',source=s,target=t,style=st);g=ET.SubElement(e,'mxGeometry',relative='1',attrib={'as':'geometry'});ar=ET.SubElement(g,'Array',attrib={'as':'points'})
   for x,y in pts[1:-1]:ET.SubElement(ar,'mxPoint',x=str(x),y=str(y))
   self.edges.append({'source':s,'target':t})
  else:
   # Editable native decoration: preserve the same straight lifeline/divider
   # already visible in SVG/PNG, rather than silently omitting it in draw.io.
   assert len(pts)==2 and (pts[0][0]==pts[1][0] or pts[0][1]==pts[1][1]),(id,pts)
   (x1,y1),(x2,y2)=pts;vertical=x1==x2
   self.cell(id,'',x1-1 if vertical else min(x1,x2),min(y1,y2) if vertical else y1-1,2 if vertical else abs(x2-x1),abs(y2-y1) if vertical else 2,f'shape=line;direction={"south" if vertical else "east"};strokeColor={BLUE};strokeWidth=1.5;dashed={int(dashed)};endArrow=none;startArrow=none;fillColor=none;')
 def finish(self,target,p):
  self.svg.append('</svg>');target.with_suffix('.svg').write_text(''.join(self.svg),encoding='utf-8');self.im.save(target.with_suffix('.png'));root=ET.Element('mxfile',host='SaigonBite P3-C');d=ET.SubElement(root,'diagram',name=p['title'],id=target.stem);d.append(self.mx);ET.ElementTree(root).write(target.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
  ids={x.get('id') for x in root.iter('mxCell')};assert all(e.get('source') in ids and e.get('target') in ids for e in root.iter('mxCell') if e.get('edge')=='1')
  p['qa']={'canvas':[W,self.h],'placed_width_mm':170 if self.h==1250 else 230,'minimum_font_px':23 if self.h==1250 else 18,'minimum_pt':(23*170 if self.h==1250 else 18*230)*72/25.4/W,'connected_edges':len(self.edges),'xml_valid':True};native=[x for x in root.iter('mxCell') if x.get('value')];fonts=[]
  for node in native:
   style=dict(q.split('=',1) for q in node.get('style','').split(';') if '=' in q);assert 'fontSize' in style and 'fontStyle' in style,(target,node.get('id'));fonts.append(float(style['fontSize']))
  p['qa'].update(native_text_cells=len(native),native_minimum_font_px=min(fonts),native_minimum_pt=min(fonts)*p['qa']['placed_width_mm']*72/25.4/W,native_explicit_font_styles=True);assert p['qa']['native_minimum_pt']>=9
  target.with_suffix('.json').write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf-8')
def element(c,attrs,methods):return {'class':c,'attributes':attrs,'methods':methods}
def signature(m):
 node=ast.parse('def '+m['signature']+':\n pass').body[0];a=node.args;out=[];inferred=False
 args=a.posonlyargs+a.args;defs=[None]*(len(args)-len(a.defaults))+a.defaults
 for x,d in zip(args,defs):
  if x.arg in ['self','cls']:continue
  inferred=inferred or x.annotation is None
  out.append(x.arg+': '+(ast.unparse(x.annotation) if x.annotation else 'Any')+(' = '+ast.unparse(d) if d else ''))
 if a.vararg:out.append('*'+a.vararg.arg+': '+(ast.unparse(a.vararg.annotation) if a.vararg.annotation else 'Any'))
 for x,d in zip(a.kwonlyargs,a.kw_defaults):out.append(x.arg+': '+(ast.unparse(x.annotation) if x.annotation else 'Any')+(' = '+ast.unparse(d) if d else ''))
 if a.kwarg:out.append('**'+a.kwarg.arg+': '+(ast.unparse(a.kwarg.annotation) if a.kwarg.annotation else 'Any'))
 ret=ast.unparse(node.returns) if node.returns else 'Any';inferred=inferred or node.returns is None
 return m['visibility']+' '+node.name+'('+', '.join(out)+') -> '+ret+(' [inferred]' if inferred else '')+(' †' if m['status']!='MATCH' else '')
def card(c,n,attrs,methods,x,y,w):
 cc=load()['classes'][n];assert set(attrs)<={a['name'] for a in cc['attributes']},(n,'stale attribute selection');assert set(methods)<={m['name'] for m in cc['methods']},(n,'stale method selection');lines=['«'+('association class' if cc.get('association_class') else cc['stereotype'])+'» '+n]
 for a in cc['attributes']:
  if a['name'] in attrs:lines+=textwrap.wrap(a['visibility']+' '+a['name']+': '+a['type'],max(38,int(w/9)),break_long_words=False)
 if not attrs and cc['layer']!='view':lines+=['(attributes omitted in this projection)']
 lines+=['— operations —']
 for m in cc['methods']:
  if m['name'] in methods:lines+=textwrap.wrap(signature(m),max(38,int(w/9)),break_long_words=False)
 if not methods:lines+=['(no operation selected)']
 if cc.get('routes'):
  for route in cc['routes']:
   if route['view_function'] in methods:
    lines+=textwrap.wrap('{'+'/'.join(route['methods'])+' '+route['rule']+'}',max(38,int(w/9)),break_long_words=False)
 h=len(lines)*22+18;c.rect(n,x,y,w,h,'#F5F9FD');c.text(n+'_label','\n'.join(lines),x+10,y+20,18,False,True);return h

def projected_dependencies(model,boxes):
 names={b['class'] for b in boxes};deps=[];classes=model['classes']
 for d in model['associations']:
  if d['source'] in names and d['target'] in names:deps.append(dict(d))
 for d in model['dependencies']:
  if d['source'] not in names or d['target'] not in names or not d.get('allowed_on_layered_diagram',True):continue
  sc,tc=classes[d['source']],classes[d['target']]
  if ((sc['layer'] in ['view','controller'] and tc['layer']!=sc['layer']) or (sc['layer']=='domain' and tc['layer']=='domain' and tc['stereotype']=='enumeration')):
   if not any(x['source']==d['source'] and x['target']==d['target'] for x in deps):deps.append(dict(d))
 return deps

def association_geometry(a,b,nodes,source,target):
 # Ports and labels are planned in the open row gutter; never put both cardinalities in one summary.
 if abs(a[1]-b[1])<30:
  lower=min([box[1] for name,box in nodes.items() if name not in (source,target) and box[1]>max(a[1],b[1])+30]+[740])
  floor=max(a[1]+a[3],b[1]+b[3]);room=lower-floor;assert room>=28,(source,target,'split the projection instead of shrinking text')
  inset=35 if room<50 else 60;left_to_right=a[0]<b[0];sign=1 if left_to_right else -1
  sx=a[0]+a[2]-inset if left_to_right else a[0]+inset;tx=b[0]+inset if left_to_right else b[0]+b[2]-inset
  se=(sx,a[1]+a[3]);te=(tx,b[1]+b[3]);bar=min(floor+40,lower-15)
  points=[se,(sx,bar),(tx,bar),te]
  source_label=(sx-sign*25,se[1]+17);target_label=(tx+sign*25,min(te[1]+19,lower-19));role_label=((sx+tx)/2,bar-18)
  return points,source_label,target_label,role_label
 if abs(a[0]-b[0])<30:
  down=b[1]>a[1];sx=a[0]+a[2]/2;tx=b[0]+b[2]/2;se=(sx,a[1]+a[3] if down else a[1]);te=(tx,b[1] if down else b[1]+b[3]);mid=(se[1]+te[1])/2
  points=[se,(sx,mid),(tx,mid),te];points=[x for i,x in enumerate(points) if i==0 or x!=points[i-1]]
  return points,(sx+28,se[1]+(19 if down else -19)),(tx+25,te[1]+(-19 if down else 19)),(max(sx,tx)+37,mid)
 raise ValueError((source,target,'association needs a separately planned route'))

def dcd(p,target):
 c=Canvas(p['title']); model=load();els=[];p['dependencies']=projected_dependencies(model,p['boxes'])
 for b in p['boxes']:
  h=card(c,b['class'],b['attributes'],b['methods'],*b['xyw']);assert b['xyw'][1]+h<740,(target,b['class'],h);els.append(element(b['class'],b['attributes'],b['methods']))
 deps=[];end_labels=[]
 for i,d in enumerate(p.get('dependencies',[])):
  a=c.nodes[d['source']];b=c.nodes[d['target']];edge_id='dep'+str(i);inheritance=d['kind'] in ('generalization','inheritance');association=d['kind']!='dependency' and not inheritance
  if association:
   pts,source_xy,target_xy,role_xy=association_geometry(a,b,c.nodes,d['source'],d['target'])
  elif abs(a[1]-b[1])<30:
   pts=[(a[0]+a[2],a[1]+a[3]/2),(b[0],b[1]+b[3]/2)] if a[0]<b[0] else [(a[0],a[1]+a[3]/2),(b[0]+b[2],b[1]+b[3]/2)]
  elif d['kind']!='dependency' and abs(a[0]-b[0])<30:
   pts=[(a[0]+a[2]/2,a[1]+a[3]),(b[0]+b[2]/2,b[1])]
  elif b[0]>600:
   pts=[(a[0]+a[2],a[1]+a[3]/2),(1180,a[1]+a[3]/2),(1180,b[1]+b[3]/2),(b[0]+b[2],b[1]+b[3]/2)]
  else:
   gutter=35+i*9;pts=[(a[0],a[1]+a[3]/2),(gutter,a[1]+a[3]/2),(gutter,b[1]+b[3]/2),(b[0],b[1]+b[3]/2)]
  c.line(edge_id,pts,d['source'],d['target'],d['kind']=='dependency',d.get('navigable',True) if association else True);deps.append(d)
  if association:
   sid=edge_id+'_source_mult';tid=edge_id+'_target_mult';c.text(sid,d['source_multiplicity'],*source_xy,18);c.text(tid,d['target_multiplicity'],*target_xy,18)
   if d.get('role'):c.text(edge_id+'_role',d['role'],*role_xy,18)
   end_labels.append({'source':d['source'],'target':d['target'],'kind':d['kind'],'role':d.get('role',''),'native_edge_id':edge_id,'source_label_id':sid,'target_label_id':tid,'source_endpoint':list(pts[0]),'target_endpoint':list(pts[-1])})
 c.text('continuation',wrap(p['continuation'],112),600,765,18)
 c.text('legend','† design target, not yet in code at C0 (see P4 input '+p['P4_input']+')',600,807,18)
 p['phase3']={'diagram_type':'dcd','elements':els,'dependencies':deps,'states':[],'association_classes':[{'class':e['class'],'classification':'association class'} for e in els if model['classes'][e['class']].get('association_class')],'association_end_labels':end_labels};c.finish(target,p)

def sequence(p,target):
 method=next(m for m in load()['classes'][p['controller']]['methods'] if m['name']==p['method'])
 if p.get('controller_signature')!=method['signature']:raise ValueError('Reviewed controller signature changed. Review SSD argument aliases, then run Part2/notes/P3-C/repair_refresh.py to refresh and rerender owned views.')
 p['status']=method['status']
 c=Canvas(p['title'],1250);xs={'actor':90,'view':385,'controller':760,'domain':1100};cls=p['domain'];ctrl=p['controller'];msg=[];message_y=[]
 for id,label in [('actor','Admin'),('view','«view» admin'),('controller',':'+ctrl),('domain',':'+cls)]:
  x=xs[id];ww=250 if id=='controller' else 190 if id=='view' else 160;c.rect(id,x-ww/2,65,ww,55,'#F5F9FD',label);c.text(id+'_label',label,x,92,18,True);c.line(id+'_life',[(x,120),(x,1135)],dashed=True,arrow=False)
 c.rect('activation',754,245,12,880,'#E0EBF7')
 def m(fr,to,method,args,kind,y,label=None,guard='',pc=''):
  data={'from':fr,'to':to,'method':method,'kind':kind,'arguments':args,'guard':guard,'PC_MG':pc,'native_edge_id':'msg'+str(len(msg)+1),'y':y};msg.append(data);message_y.append(y);x1=xs[fr];x2=xs[to];txt=label or method+'('+args+')';txt=wrap(txt,108 if kind=='ssd' else 42 if fr!=to else 30)
  if fr==to:
   pts=[(x1,y),(x1+100,y),(x1+100,y+35),(x1,y+35)];c.text('ml'+str(len(msg)),txt,x1+20,y-28,18,False,True)
  else:
   pts=[(x1,y),(x2,y)];c.text('ml'+str(len(msg)),txt,600 if kind=='ssd' else (x1+x2)/2,y-((len(txt.split('\n'))-1)*(27 if c.h==1250 else 22)+22),18)
  c.line('msg'+str(len(msg)),pts,fr,to,kind=='return',True,open_head=kind=='return')
 m('actor','view',p['operation'],p['parameters'],'ssd',190)
 adapter_target=any(m['status']!='MATCH' for m in load()['classes']['admin']['methods'] if m['name'] in ([p['view_method'],'hub_menu'] if p['operation']=='listCatalogue' else [p['view_method']]))
 c.text('adapter', 'Route adapter: admin.'+p['view_method']+(' / admin.hub_menu (hub filter)' if p['operation']=='listCatalogue' else '')+(' †' if adapter_target else ''),600,395,23)
 m('view','controller',p['method'],p['arguments'],'call',275,label=p['method']+'('+p['arguments']+')'+(' †' if p['status']!='MATCH' else ''))
 m('controller','controller','_require_admin','uid()','call',345)
 c.rect('alt',30,410,1140,715);c.text('alt_label',wrap('alt ['+p['reject_guard']+'] '+p['MG'],92),50,427,18,True,True)
 m('controller','view','refusal','','return',540,label='refusal / no data; zero writes' if p['read'] else 'controlledRefusal / no data; nothing changed',guard='denied / invalid / stale',pc=p['MG'])
 m('view','actor','response','','return',570,label='refusal response',guard='denied / invalid / stale',pc=p['MG'])
 c.line('divide1',[(30,580),(1170,580)],arrow=False);c.text('guardok',wrap('[authorized; valid; selected change completes] '+p['PC'],92),50,610,18,True,True)
 if p.get('create'):
  m('controller','domain',cls,p['create'],'create',700,label='«create» '+cls+'('+p['create']+')',guard='valid')
 else:
  m('controller','domain','attributes',p['domain_note'],'note',700,label='«note» '+p['domain_note'],guard='valid')
 c.rect('persist',360,755,790,110,'#FFFBEA');c.text('persist_label','loaded/saved through data access — see 4.3.2',755,780,18);c.text('effect_label',wrap(p['effect'],62),755,815,18)
 m('controller','view','result','','return',920,label=p['result'],guard='success',pc=p['PC'])
 m('view','actor','response','','return',970,label='render / redirect acknowledgement')
 c.line('divide2',[(30,1000),(1170,1000)],arrow=False);c.text('fail_guard','[technical read/save failure] '+p['MG'],50,1025,18,True,True)
 m('controller','view','controlledFailure','','return',1110,label='controlled failure; '+('zero writes' if p['read'] else 'rollback; nothing changed')+(' †' if p['status']!='MATCH' else ''),guard='technical failure',pc=p['MG'])
 m('view','actor','response','','return',1120,label='failure response',guard='technical failure',pc=p['MG'])
 c.text('pointer',wrap(p['ssd_occurrence'],110),600,1165,18)
 c.text('legend','† design target, not yet in code at C0 (see P4 input '+p['P4_input']+')',600,1205,18)
 p['phase3']={'diagram_type':'sequence','UC':p['UC'],'op_id':p['op_id'],'operation':p['operation'],'parameters':p['parameters'],'ssd_occurrence':p['ssd_occurrence'],'elements':[element('admin',[],[p['view_method'],'hub_menu'] if p['operation']=='listCatalogue' else [p['view_method']]),element(ctrl,[],[p['method'],'_require_admin']),element(cls,p['domain_attributes'],[])],'dependencies':[next((dict(d) for d in load()['dependencies'] if d['source']==source and d['target']==target),{'source':source,'target':target,'kind':'dependency'}) for source,target in [('admin',ctrl),(ctrl,cls)]],'lifelines':[{'id':i,'class':('Admin' if i=='actor' else 'admin' if i=='view' else ctrl if i=='controller' else cls),'role':i} for i in xs],'messages':msg,'states':p.get('states',[]),'interaction_fragments':[{'id':'alt','operator':'alt','guard':p['reject_guard'],'x':30,'y':410,'w':1140,'h':715,'message_indices':[i for i,y in enumerate(message_y) if 410<=y<=1125],'operands':[{'guard':p['reject_guard'],'guard_label_id':'alt_label','x':30,'y':410,'w':1140,'h':170,'bottom_divider_id':'divide1','message_indices':[i for i,y in enumerate(message_y) if 410<=y<580]},{'guard':'authorized; valid; selected change completes','guard_label_id':'guardok','x':30,'y':580,'w':1140,'h':420,'bottom_divider_id':'divide2','message_indices':[i for i,y in enumerate(message_y) if 580<=y<1000]},{'guard':'technical read/save failure','guard_label_id':'fail_guard','x':30,'y':1000,'w':1140,'h':125,'message_indices':[i for i,y in enumerate(message_y) if 1000<=y<=1125]}]}]};c.finish(target,p)
def build(path):
 path=Path(path);p=json.loads(path.read_text(encoding='utf-8'));(dcd if p['type']=='dcd' else sequence)(p,path.with_suffix(''))
if __name__=='__main__':build(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.json'))
