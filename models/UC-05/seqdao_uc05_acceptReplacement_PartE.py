"""P3-F document renderer; no application imports or execution.
Author: 722I0004 · AI-assisted (Codex).
Balanced-diagrams: fixed 1.28 landscape plate, bounded columns and row bands.
The per-figure copy is standalone and consumes its adjacent JSON.
"""
from pathlib import Path
import sys,json,re,math,hashlib,xml.etree.ElementTree as ET
from html import escape
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
W,H,FS=1600,1250,24
BLUE,INK='#004387','#202B36'
def font(n=FS,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
def wrap(text,width,n=FS,b=False):
 out=[]
 for line in str(text).split('\n'):
  cur=''
  for word in line.split():
   pieces=[]
   while font(n,b).getlength(word)>width:
    k=len(word)-1
    while font(n,b).getlength(word[:k])>width:k-=1
    pieces.append(word[:k]);word=word[k:]
   for w in pieces+[word]:
    if cur and font(n,b).getlength(cur+' '+w)>width:out.append(cur);cur=w
    else:cur=(cur+' '+w).strip()
  out.append(cur)
 return out
def refresh(d,p):
 modelpath=p.parents[1]/'shared/design_model.json';m=json.loads(modelpath.read_text(encoding='utf-8'));classes=m['classes']
 for e in d['phase3']['elements']:
  for method,signature in e.get('method_signatures',{}).items():
   current=next(x for x in classes[e['class']]['methods'] if x['name']==method)
   if signature!=current['signature']:raise ValueError('Reviewed signature changed; explicit lane/alias review required: '+e['class']+'.'+method)
 for msg in d['phase3']['messages']:
  if msg['kind']!='call':continue
  lf=next(x for x in d['phase3']['lifelines'] if x['id']==msg['to']);method=next(x for x in classes[lf['class']]['methods'] if x['name']==msg['method'])
  msg['label']=msg['base_label'].replace('{dagger}','†' if method['status'] in ('P4-TARGET','GAP') else '')
  msg['status']=method['status'];msg['receiver_signature']=method['signature'];msg['P4_input']=method.get('P4_input','')
 # Signature equality never clears behavior targets. Operation and all methods
 # must be explicitly reviewed MATCH before target prose can lose its dagger.
 row=next(x for x in m['operation_rows'] if x['UC']==d['UC'] and x['operation']==d['phase3']['operation'])
 selected=[]
 for e in d['phase3']['elements']:
  selected.extend(x for x in classes[e['class']]['methods'] if x['name'] in e.get('methods',[]))
  selected.extend(x for x in classes[e['class']]['attributes'] if x['name'] in e.get('attributes',[]))
 if row['status']=='MATCH' and all(x.get('status','MATCH')=='MATCH' for x in d['phase3']['messages']+selected):
  d['target_note']='Reviewed MATCH in the sole model; static correspondence only. P2-S12 connection runtime qualification remains separate.'
  d['transaction_summary']=d['transaction_summary'].replace('†','')
  for msg in d['phase3']['messages']:msg['label']=msg['label'].replace('†','');msg['guard']=msg['guard'].replace('†','')
  d['target_cleared_by_reviewed_MATCH']=True
 d['shared_model_sha256']=hashlib.sha256(modelpath.read_bytes()).hexdigest()
 return d
class Canvas:
 def __init__(self,d):
  self.d=d;self.im=Image.new('RGB',(W,H),'white');self.dr=ImageDraw.Draw(self.im);self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>'];self.mx=ET.Element('mxfile',host='SaigonBite P3-F',type='device');dg=ET.SubElement(self.mx,'diagram',id=d['stem'],name=d['title']);mo=ET.SubElement(dg,'mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H));self.root=ET.SubElement(mo,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0');self.i=0;self.bounds=[];self.edges=[]
 def cell(self,id,x,y,w,h,label='',style=''):
  c=ET.SubElement(self.root,'mxCell',id=id,vertex='1',parent='1',value=label,style=style);ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'});return c
 def text(self,x,y,t,w,n=FS,b=False,bg=False,id=None):
  lines=wrap(t,w,n,b);lh=n*1.16;h=len(lines)*lh
  assert x>=0 and y>=0 and x+w<=W+1 and y+h<=H+1,(self.d['stem'],t,x,y,w,h)
  if bg:
   self.dr.rectangle((x-3,y-1,x+w+3,y+h+2),fill='white');self.s.append(f'<rect x="{x-3}" y="{y-1}" width="{w+6}" height="{h+3}" fill="white"/>')
  for i,line in enumerate(lines):
   self.dr.text((x,y+i*lh),line,font=font(n,b),fill=INK)
   self.s.append(f'<text x="{x}" y="{y+i*lh+n*.93}" font-family="Arial" font-size="{n}" font-weight="{"bold" if b else "normal"}" fill="{INK}">{escape(line)}</text>')
  self.cell(id or 'txt'+str(self.i),x,y,w,h,'\n'.join(lines),f'text;html=0;whiteSpace=wrap;align=left;verticalAlign=top;strokeColor=none;fillColor=none;fontFamily=Arial;fontSize={n};fontStyle={1 if b else 0};');self.i+=1;self.bounds.append([x,y,w,h]);return h
 def rect(self,x,y,w,h,fill='white',id=None):
  self.dr.rectangle((x,y,x+w,y+h),outline=BLUE,fill=fill,width=2);self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" stroke="{BLUE}" fill="{fill}" stroke-width="2"/>');self.cell(id or 'box'+str(self.i),x,y,w,h,'',f'fillColor={fill};strokeColor={BLUE};');self.i+=1
 def line(self,pts,dash=False,arrow=False,source=None,target=None,eid=None,filled=False):
  for a,b in zip(pts,pts[1:]):
   if dash:
    count=max(1,int(math.dist(a,b)/8))
    for k in range(0,count,2):self.dr.line([(a[0]+(b[0]-a[0])*q/count,a[1]+(b[1]-a[1])*q/count) for q in (k,min(k+1,count))],fill=BLUE,width=2)
   else:self.dr.line([a,b],fill=BLUE,width=2)
  self.s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{BLUE}" stroke-width="2"'+(' stroke-dasharray="7 7"' if dash else '')+'/>')
  if arrow:
   a,b=pts[-2:];angle=math.atan2(b[1]-a[1],b[0]-a[0]);p=[(b[0]-14*math.cos(angle-.45),b[1]-14*math.sin(angle-.45)),b,(b[0]-14*math.cos(angle+.45),b[1]-14*math.sin(angle+.45))]
   if filled:self.dr.polygon(p,fill=BLUE);self.s.append('<polygon data-edge-head="'+str(eid)+'" points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="{BLUE}" stroke="{BLUE}" stroke-width="2"/>')
   else:self.dr.line(p,fill=BLUE,width=2);self.s.append('<polyline data-edge-head="'+str(eid)+'" points="'+' '.join(f'{x},{y}' for x,y in p)+f'" fill="none" stroke="{BLUE}" stroke-width="2"/>')
  if source:
   id=eid or 'edge'+str(self.i);c=ET.SubElement(self.root,'mxCell',id=id,edge='1',parent='1',source=source,target=target,style='edgeStyle=none;endArrow='+('block;endFill=1;' if filled else 'open;endFill=0;')+'strokeColor='+BLUE+';'+('dashed=1;' if dash else '')+'exitX=0.5;entryX=0.5;exitPerimeter=0;entryPerimeter=0;');g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});a=ET.SubElement(g,'Array',attrib={'as':'points'})
   for x,y in pts[1:-1]:ET.SubElement(a,'mxPoint',x=str(x),y=str(y))
   self.edges.append({'id':id,'source':source,'target':target,'points':pts,'filled':filled,'dashed':dash});self.i+=1
 def finish(self,p):
  self.s.append('</svg>');p.with_suffix('.svg').write_text('\n'.join(self.s),encoding='utf-8');self.im.save(p.with_suffix('.png'));ET.indent(self.mx);ET.ElementTree(self.mx).write(p.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
  self.d['render_receipt']={'canvas':[W,H],'minimum_font_px':FS,'placed_width_mm':230,'minimum_pt':FS*230*72/(W*25.4),'native_font_matches_svg':True,'label_bounds':self.bounds,'edges':self.edges,'author_native_cell':True};p.with_suffix('.json').write_text(json.dumps(self.d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def old_render(d,p):
 c=Canvas(d);c.text(35,15,d['title'],1530,28,True);c.text(35,54,d['scope'],1530)
 lfs=d['phase3']['lifelines'];xs={l['id']:120+i*1360/max(1,len(lfs)-1) for i,l in enumerate(lfs)};bw=min(224,1360/max(1,len(lfs)-1)-14)
 for l in lfs:
  x=xs[l['id']];c.rect(x-bw/2,100,bw,120,'#F1F6FA',l['id']);label=l.get('label',l['class']);label=re.sub(r'(?<=[a-z])(?=[A-Z])','\n',label);c.text(x-bw/2+7,105,label,bw-14);c.line([(x,220),(x,1030)],True)
 for i,msg in enumerate(d['phase3']['messages']):
  y=242+i*125;msg['y']=y+99;label=msg['label'];kind=msg['kind']
  if msg.get('guard'):label='['+msg['guard']+'] '+label
  if kind=='note' and not msg.get('draw_arrow'):
   c.rect(35,y,1530,111,'#FFF8E9')
   if msg.get('fragment'):
    c.rect(35,y,66,32,'#F1F6FA');c.text(42,y,'alt',56);c.text(110,y+5,label,1440)
   else:c.text(45,y+5,label,1510)
   continue
  # Each semantic message occupies a band: a full-width label above the arrow.
  # Long SSD parameters therefore stay readable without shrinking or collisions.
  c.text(45,y,label,1510,bg=True)
  a,b=xs[msg['from']],xs[msg['to']];yy=y+99
  # Zero-width anchors lie exactly on actual lifelines, at the actual endpoint.
  # Native edge attachment and rendered polylines share the same coordinates.
  src=f'm{i}s';dst=f'm{i}t';c.cell(src,a,yy,0,0,'','opacity=0;');c.cell(dst,b,yy+(22 if a==b else 0),0,0,'','opacity=0;')
  pts=[(a,yy),(a+35,yy),(a+35,yy+22),(a,yy+22)] if a==b else [(a,yy),(b,yy)]
  c.line(pts,kind=='return',True,src,dst,'message'+str(i));msg['edge_id']='message'+str(i)
  if kind in ('call','create'):c.rect(b-5,yy,10,18,'#DAE9F5')
 c.text(35,1035,d['continuation'],1530)
 c.text(35,1070,d['transaction_summary'],1530)
 c.text(35,1130,d['target_note'],1530)
 c.text(35,1190,'Figure '+d['figure']+'. '+d['phase3']['operation']+' / '+d['part']+' — Author: 722I0004 · AI-assisted (Codex)',1530)
 c.text(35,1220,'Static only · 230 mm landscape · minimum 9.78 pt · native draw.io and final DOCX/PDF placement UNTESTED',1530)
 c.finish(p)
def is_arrow(m):return m['kind']!='note' or bool(m.get('draw_arrow'))
def layout(d):
 messages=d['phase3']['messages'];fragments=d['phase3']['interaction_fragments'];y=232;rows=[]
 for i,msg in enumerate(messages):
  opened=sorted([f for f in fragments if f['start_index']==i],key=lambda f:(-f['end_index'],f['id']))
  for f in opened:
   f['x']=25+12*f.get('depth',0);f['y']=y;f['w']=1550-24*f.get('depth',0)
   f['guard_height']=max(30,len(wrap('['+f['guard']+']',f['w']-120))*27.84+5);y+=f['guard_height']+5
  label=msg['label'];text_width=1470
  if msg.get('guard'):label='['+msg['guard']+'] '+label
  h=len(wrap(label,text_width))*27.84;top=y
  if is_arrow(msg):
   ay=top+h+11;bottom=ay+(24 if msg['from']==msg['to'] else 17)
   msg['y']=ay;msg['label_box']=[65,top,text_width,h];msg['native_edge_id']='message'+str(i);msg['edge_id']=msg['native_edge_id']
  else:
   bottom=top+h+12;msg['y']=top+h;msg['label_box']=[65,top+4,text_width,h];msg.pop('native_edge_id',None);msg.pop('edge_id',None)
  rows.append((top,bottom,label));y=bottom+10
  closed=sorted([f for f in fragments if f['end_index']==i],key=lambda f:f.get('depth',0),reverse=True)
  for f in closed:
   f['h']=y-f['y'];f['message_indices']=[j for j in range(f['start_index'],f['end_index']+1) if is_arrow(messages[j])];assert f['message_indices'],(d['stem'],'empty guarded frame',f)
   y+=5
 assert y<=1026,(d['stem'],'split required',y)
 return rows
def render(d,p):
 c=Canvas(d);rows=layout(d);c.text(35,15,d['title'],1530,28,True);c.text(35,54,d['scope'],1530)
 assert len(wrap(d['continuation'],1530))==1,(d['stem'],'continuation needs a shorter line')
 lfs=d['phase3']['lifelines'];xs={l['id']:120+i*1360/max(1,len(lfs)-1) for i,l in enumerate(lfs)};bw=min(224,1360/max(1,len(lfs)-1)-14)
 # Actual enclosing rectangles are drawn before messages and remain transparent.
 for f in d['phase3']['interaction_fragments']:
  x,y,w,h=(f[k] for k in ('x','y','w','h'));c.dr.rectangle((x,y,x+w,y+h),outline=BLUE,width=2);c.s.append(f'<rect data-fragment-id="{f["id"]}" x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{BLUE}" stroke-width="2"/>');c.cell(f['id'],x,y,w,h,'','shape=umlFrame;fillColor=none;strokeColor='+BLUE+';');c.i+=1
 for l in lfs:
  x=xs[l['id']];c.rect(x-bw/2,100,bw,120,'#F1F6FA',l['id']);label=re.sub(r'(?<=[a-z])(?=[A-Z])','\n',l.get('label',l['class']));c.text(x-bw/2+7,105,label,bw-14);c.line([(x,220),(x,1026)],True)
 for f in d['phase3']['interaction_fragments']:
  x,y,w,h=(f[k] for k in ('x','y','w','h'));c.text(x+6,y+1,f['operator'],84,b=True,bg=True,id=f['id']+'_operator');c.text(x+102,y+1,'['+f['guard']+']',w-112,bg=True,id=f['id']+'_guard')
 for i,(msg,row) in enumerate(zip(d['phase3']['messages'],rows)):
  top,bottom,label=row;kind=msg['kind']
  if not is_arrow(msg):
   c.rect(55,top,1490,bottom-top,'#FFF8E9');c.text(65,top+4,label,1470);continue
  c.text(65,top,label,1470,bg=True);a,b=xs[msg['from']],xs[msg['to']];yy=msg['y'];src=f'm{i}s';dst=f'm{i}t';c.cell(src,a,yy,0,0,'','opacity=0;');c.cell(dst,b,yy+(22 if a==b else 0),0,0,'','opacity=0;');pts=[(a,yy),(a+35,yy),(a+35,yy+22),(a,yy+22)] if a==b else [(a,yy),(b,yy)]
  # Actual methods, SSD requests, construction and DB requests are synchronous.
  # Attribute/property notes keep their separate open annotation arrow.
  database=next(l for l in lfs if l['id']==msg['to'])['role']=='database'
  filled=kind in ('call','ssd','create') or (database and kind!='return')
  c.line(pts,kind=='return',True,src,dst,msg['native_edge_id'],filled=filled);msg['arrow_style']='closed_filled_synchronous' if filled else 'dashed_open_reply' if kind=='return' else 'open_attribute_note'
  if kind in ('call','create'):c.rect(b-5,yy,10,18,'#DAE9F5')
 c.text(35,1035,d['continuation'],1530)
 c.text(35,1070,d['transaction_summary'],1530)
 c.text(35,1130,d['target_note'],1530)
 c.text(35,1190,'Figure '+d['figure']+'. '+d['phase3']['operation']+' / '+d['part']+' — Author: 722I0004 · AI-assisted (Codex)',1530)
 c.text(35,1220,'Static only · 230 mm landscape · minimum 9.78 pt · native draw.io and final DOCX/PDF placement UNTESTED',1530)
 c.finish(p)
if __name__=='__main__':
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.json');d=refresh(json.loads(p.read_text(encoding='utf-8-sig')),p);render(d,p.with_suffix(''))
