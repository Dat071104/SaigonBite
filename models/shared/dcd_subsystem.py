"""P3-55 subsystem projections of the sole shared design model.

Author: 722I0004 · AI-assisted (Codex)
No application imports or execution. Run --plan once to construct projections;
run without arguments to refresh every existing owned projection from the model.
Each figure's adjacent wrapper regenerates that projection independently.
"""
from pathlib import Path
import ast, collections, hashlib, json, math, sys, textwrap
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SCRATCH = Path('D:/RAD/FINAL/Part2/notes/P3-E')
MODEL = HERE / 'design_model.json'
AUTHOR = 'Author: 722I0004 · AI-assisted (Codex)'
W, H, FONT, LH = 1200, 850, 18, 23
INK, BLUE = '#233348', '#174976'
COLORS = {'view':'#E6F3FC','controller':'#E9EFFA','domain':'#EAF5EC','data_access':'#FFF2DE'}
LAYERS = {'view':'View','controller':'Controller','domain':'Domain','data_access':'Data access'}

def read_model():
    return json.loads(MODEL.read_text(encoding='utf-8'))

def font(size=FONT, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/arial'+('bd' if bold else '')+'.ttf', size)

def wrap(text, width, size=FONT, bold=False):
    result=[]
    for para in str(text).split('\n'):
        current=''
        for word in para.split(' '):
            trial=(current+' '+word).strip()
            if current and font(size,bold).getlength(trial)>width:
                result.append(current);current=word
            else:current=trial
        result.append(current)
    assert all(font(size,bold).getlength(line)<=width+.1 for line in result),(text,width,result)
    return result

def mark(item):
    return (' † ['+item['status']+']') if item['status']!='MATCH' else ''

def method_text(m):
    node=ast.parse('def '+m['signature']+':\n pass').body[0]
    args=node.args;values=[];inferred=False
    allargs=args.posonlyargs+args.args
    defaults=[None]*(len(allargs)-len(args.defaults))+args.defaults
    for i,(arg,default) in enumerate(zip(allargs,defaults)):
        if arg.arg not in ('self','cls'):
            inferred |= arg.annotation is None
            value=arg.arg+': '+(ast.unparse(arg.annotation) if arg.annotation else 'Any')
            if default is not None:value+=' = '+ast.unparse(default)
            values.append(value)
        if args.posonlyargs and i+1==len(args.posonlyargs):values.append('/')
    if args.vararg:
        a=args.vararg;values.append('*'+a.arg+': '+(ast.unparse(a.annotation) if a.annotation else 'Any'));inferred |= a.annotation is None
    elif args.kwonlyargs:values.append('*')
    for a,d in zip(args.kwonlyargs,args.kw_defaults):
        value=a.arg+': '+(ast.unparse(a.annotation) if a.annotation else 'Any');inferred |= a.annotation is None
        if d is not None:value+=' = '+ast.unparse(d)
        values.append(value)
    if args.kwarg:
        a=args.kwarg;values.append('**'+a.arg+': '+(ast.unparse(a.annotation) if a.annotation else 'Any'));inferred |= a.annotation is None
    inferred |= node.returns is None
    ret=ast.unparse(node.returns) if node.returns else 'Any'
    tags=[]
    for tag in ('property','staticmethod','classmethod'):
        if tag in m.get('decorators',[]):tags.append(tag)
    return m['visibility']+' '+node.name+'('+', '.join(values)+') -> '+ret+(' {'+', '.join(tags)+'}' if tags else '')+(' [inferred]' if inferred else '')+mark(m)

def member_units(c, attrs=None, methods=None):
    attrs={a['name'] for a in c['attributes'] if not a.get('diagram_omit')} if attrs is None else set(attrs)
    methods={m['name'] for m in c['methods']} if methods is None else set(methods)
    units=[]
    for a in c['attributes']:
        if a['name'] not in attrs:continue
        t=a['visibility']+' '+a['name']+': '+a['type']
        if c['stereotype']=='enumeration':t+=' = '+str(a['default'])
        t+=(' [inferred]' if a.get('inferred') or not a.get('annotated') else '')+mark(a)
        units.append({'kind':'attribute','name':a['name'],'lines':wrap(t,510)})
    for m in c['methods']:
        if m['name'] not in methods:continue
        lines=wrap(method_text(m),510)
        for route in c.get('routes',[]):
            if route['view_function']==m['name']:lines+=wrap('{'+('/'.join(route['methods']))+' '+route['rule']+'}',510)
        units.append({'kind':'method','name':m['name'],'lines':lines})
    return units

class Canvas:
    def __init__(self,p):
        self.p=p;self.nodes={};self.edges=[];self.texts=[]
        self.im=Image.new('RGB',(W*2,H*2),'white');self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>']
        self.mx=ET.Element('mxGraphModel',page='1',pageWidth=str(W),pageHeight=str(H),grid='1')
        self.xr=ET.SubElement(self.mx,'root');ET.SubElement(self.xr,'mxCell',id='0');ET.SubElement(self.xr,'mxCell',id='1',parent='0')
        self.text('title',p['figure']+'. '+p['title'],35,18,1130,23,True)
        self.text('sub','Shared subsystem · C0 45ac762 · '+p['subtitle'],35,50,1130)

    def cell(self,id,value,x,y,w,h,style):
        assert id not in self.nodes,id
        self.nodes[id]=(x,y,w,h)
        c=ET.SubElement(self.xr,'mxCell',id=id,value=value,vertex='1',parent='1',style='html=0;fontFamily=Arial;'+style)
        ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})

    def text(self,id,t,x,y,width=1100,size=FONT,bold=False,fill=INK):
        lines=wrap(t,width,size,bold)
        for i,line in enumerate(lines):
            yy=y+i*(size+5)
            self.d.text((x*2,yy*2),line,font=ImageFont.truetype('C:/Windows/Fonts/arial'+('bd' if bold else '')+'.ttf',size*2),fill=fill)
            self.svg.append(f'<text x="{x}" y="{yy+size*.91}" font-family="Arial" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{fill}">{escape(line)}</text>')
            self.texts.append({'id':id,'text':line,'x':x,'y':yy,'w':font(size,bold).getlength(line),'h':size+2,'font':size})
        self.cell(id,'\n'.join(lines),x,y,width,len(lines)*(size+5),f'text;fillColor=none;strokeColor=none;fontSize={size};fontStyle={int(bold)};align=left;verticalAlign=top;spacing=0;whiteSpace=wrap;')
        return len(lines)*(size+5)

    def rect(self,id,x,y,w,h,fill,stroke=BLUE):
        self.d.rectangle((x*2,y*2,(x+w)*2,(y+h)*2),fill=fill,outline=stroke,width=3)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.cell(id,'',x,y,w,h,'fillColor='+fill+';strokeColor='+stroke+';fontSize=18;fontStyle=0;')

    def segment(self,pts,dashed=False):
        for a,b in zip(pts,pts[1:]):
            length=math.dist(a,b)
            if not length:continue
            if dashed:
                dx,dy=b[0]-a[0],b[1]-a[1]
                for z in range(0,int(length),12):
                    end=min(z+6,length)
                    self.d.line(((a[0]+dx*z/length)*2,(a[1]+dy*z/length)*2,(a[0]+dx*end/length)*2,(a[1]+dy*end/length)*2),fill=BLUE,width=3)
            else:self.d.line([(x*2,y*2) for x,y in (a,b)],fill=BLUE,width=3)
        self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{BLUE}" stroke-width="1.5"'+(' stroke-dasharray="6 6"' if dashed else '')+'/>')

    def edge(self,id,dep,pts,source_id=None,target_id=None):
        source_id=source_id or dep['source'];target_id=target_id or dep['target']
        source=self.nodes[source_id];target=self.nodes[target_id]
        dashed=dep['kind']=='dependency';self.segment(pts,dashed)
        kind=dep['kind'];end=pts[-1];prior=pts[-2];theta=math.atan2(end[1]-prior[1],end[0]-prior[0])
        if kind=='generalization':
            poly=[end,(end[0]-16*math.cos(theta-.45),end[1]-16*math.sin(theta-.45)),(end[0]-16*math.cos(theta+.45),end[1]-16*math.sin(theta+.45))]
            self.d.polygon([(x*2,y*2) for x,y in poly],fill='white',outline=BLUE,width=3)
            self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in poly)+f'" fill="white" stroke="{BLUE}" stroke-width="1.5"/>')
        elif dep.get('navigable',True) or dashed:
            a=(end[0]-12*math.cos(theta-.4),end[1]-12*math.sin(theta-.4));b=(end[0]-12*math.cos(theta+.4),end[1]-12*math.sin(theta+.4));self.segment([a,end,b])
        if kind=='composition':
            a=pts[0];b=pts[1];theta=math.atan2(b[1]-a[1],b[0]-a[0]);u=(math.cos(theta),math.sin(theta));v=(-u[1],u[0]);poly=[a,(a[0]+10*u[0]+5*v[0],a[1]+10*u[1]+5*v[1]),(a[0]+20*u[0],a[1]+20*u[1]),(a[0]+10*u[0]-5*v[0],a[1]+10*u[1]-5*v[1])]
            self.d.polygon([(x*2,y*2) for x,y in poly],fill=BLUE);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in poly)+f'" fill="{BLUE}"/>')
        x,y,w,h=source;xx,yy,ww,hh=target
        style=f'edgeStyle=none;rounded=0;strokeColor={BLUE};dashed={int(dashed)};endArrow={"block" if kind=="generalization" else "open" if dep.get("navigable",True) or dashed else "none"};endFill=0;startArrow={"diamond" if kind=="composition" else "none"};startFill=1;exitX={(pts[0][0]-x)/w};exitY={(pts[0][1]-y)/h};entryX={(end[0]-xx)/ww};entryY={(end[1]-yy)/hh};exitPerimeter=0;entryPerimeter=0;fontSize=18;fontStyle=0;'
        e=ET.SubElement(self.xr,'mxCell',id=id,value='',edge='1',parent='1',source=source_id,target=target_id,style=style)
        g=ET.SubElement(e,'mxGeometry',relative='1',attrib={'as':'geometry'});ar=ET.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in pts[1:-1]:ET.SubElement(ar,'mxPoint',x=str(x),y=str(y))
        self.edges.append({'id':id,'source_shape':source_id,'target_shape':target_id,'source':dep['source'],'target':dep['target'],'kind':kind,'points':pts})

    def finish(self,path,model,elements,deps):
        p=self.p
        self.text('continue',p['continuation'],35,713,1130)
        inputs=sorted({x.strip() for e in elements for kind in ('attributes','methods') for x0 in model['classes'][e['class']][kind] if (x0['name'] in e[kind] or (not e['attributes'] and not e['methods'])) and x0['status']!='MATCH' for x in x0.get('P4_input','').split(';') if x.strip()} | {x.strip() for d in deps if d.get('status')!='MATCH' for x in d.get('P4_input','').split(';') if x.strip()})
        legend='† P4-TARGET / GAP: design target, not yet in code at C0.'
        if inputs:legend+=' P4 input: '+', '.join(inputs)+'.'
        else:legend='MATCH = static correspondence at C0. No runtime or implementation-completion claim.'
        self.text('legend',legend,35,758,1130)
        self.text('author',AUTHOR,35,818,1130)
        self.svg.append('</svg>');path.with_suffix('.svg').write_text(''.join(self.svg),encoding='utf-8');self.im.save(path.with_suffix('.png'))
        root=ET.Element('mxfile',host='SaigonBite P3-E');d=ET.SubElement(root,'diagram',name=p['figure']+' '+p['title'],id=path.stem);d.append(self.mx);ET.ElementTree(root).write(path.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
        states=[]
        for e in elements:
            name=e['class'];c=model['classes'][name]
            if name in ('OrderState','PaymentState','DeliveryState','OfferState') and e['attributes']:
                states.append({'class':name,'attribute':'value','values':[ast.literal_eval(a['default']) for a in c['attributes'] if a['name'] in e['attributes']]})
        p.update(model_source='models/shared/design_model.json',model_sha256=hashlib.sha256(MODEL.read_bytes()).hexdigest(),C0=model['C0'],placed_width_mm=230)
        p['phase3']={'diagram_type':'dcd','elements':elements,'dependencies':deps,'states':states,'association_classes':[{'class':e['class'],'classification':'association class'} for e in elements if model['classes'][e['class']].get('association_class')]}
        p['qa']={'canvas':[W,H],'placed_width_mm':230,'minimum_font_px':18,'minimum_pt':18*230*72/(W*25.4),'native_minimum_font_px':18,'native_minimum_pt':18*230*72/(W*25.4),'native_explicit_font_styles':True,'xml_valid':True,'connected_edges':len(self.edges),'geometry_edges':self.edges,'text_bounds':self.texts}
        path.with_suffix('.json').write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf-8')

def element(model,name,attrs,methods):
    c=model['classes'][name]
    return {'class':name,'attributes':attrs,'methods':methods,'attribute_types':{a['name']:a['type'] for a in c['attributes'] if a['name'] in attrs},'method_signatures':{m['name']:m['signature'] for m in c['methods'] if m['name'] in methods}}

def refs(model,name):
    return 'Members: '+', '.join(COVERAGE.get(name,[]))

def small_box(canvas,model,name,x,y,w=280,h=90,id=None):
    c=model['classes'][name];id=id or name;canvas.rect(id,x,y,w,h,COLORS[c['layer']]);st='association class' if c.get('association_class') else c['stereotype']
    canvas.text(id+'_st','«'+st+'»'+(' †' if c['status']!='MATCH' else ''),x+9,y+4,w-18)
    canvas.text(id+'_name',name,x+9,y+28,w-18,18,True)
    # Reference cards carry no hidden members in normalized metadata.
    return element(model,name,[],[])

def render(path):
    p=json.loads(path.with_suffix('.json').read_text(encoding='utf-8'));m=read_model();c=Canvas(p);elements=[];deps=[]
    if p['projection']=='members':
        layer=p['layer'];c.rect('layer',25,90,1150,610,COLORS[layer]);c.text('layer_title',LAYERS[layer]+' · complete declared members across the continued cards',40,94,1120,18,True)
        for i,b in enumerate(p['cards']):
            cc=m['classes'][b['class']];units=member_units(cc,b['attributes'],b['methods']);lines=[];last=None
            for u in units:
                if u['kind']!=last:lines.append('— '+('attributes' if u['kind']=='attribute' else 'operations')+' —');last=u['kind']
                lines+=u['lines']
            x,y=b['x'],b['y'];title='«'+('association class' if cc.get('association_class') else cc['stereotype'])+'» '+b['class']
            selected_statuses=[item['status'] for kind in ('attributes','methods') for item in cc[kind] if item['name'] in b[kind]]
            shown_status='GAP' if 'GAP' in selected_statuses else 'P4-TARGET' if 'P4-TARGET' in selected_statuses else 'MATCH'
            header=wrap(title,510,18,True);status='Shown: ['+shown_status+']'+(' †' if shown_status!='MATCH' else '')+' · '+b['part']
            height=(len(header)+1+max(1,len(lines)))*LH+21
            assert y+height<=692,(path,b['class'],y,height)
            id='card'+str(i);c.rect(id,x,y,540,height,'white');c.text(id+'_title','\n'.join(header),x+12,y+7,516,18,True);yy=y+9+len(header)*LH;c.text(id+'_status',status,x+12,yy,516);yy+=LH+4
            c.rect(id+'_separator',x,yy-3,540,1,BLUE)
            if lines:
                for j,line in enumerate(lines):
                    if line=='— operations —' and j>0:c.rect(id+'_operation_separator',x,yy+j*LH-3,540,1,BLUE)
                    c.text(id+'_line'+str(j),line,x+12,yy+j*LH,516)
            else:c.text(id+'_empty','(no declared attributes or methods)',x+12,yy,516)
            elements.append(element(m,b['class'],b['attributes'],b['methods']))
        c.finish(path,m,elements,[])
    elif p['projection']=='layered':
        view,ctrl=p['view'],p['controller'];domains=p['domains'];daos=p['daos']
        for layer,y in [('view',91),('controller',235),('domain',395),('data_access',565)]:
            c.rect('band_'+layer,26,y,1148,125,COLORS[layer]);c.text('bandlabel_'+layer,LAYERS[layer],35,y+4,1120,18,True)
        elements+=[small_box(c,m,view,440,120,320,79),small_box(c,m,ctrl,390,266,420,79)]
        for layer,names,y in [('domain',domains,426),('data_access',daos,596)]:
            width= min(340,(1100-(len(names)-1)*25)/max(1,len(names)));total=len(names)*width+(len(names)-1)*25;x=(1200-total)/2
            for name in names:elements.append(small_box(c,m,name,x,y,width,79));x+=width+25
        pairs=[(view,ctrl)]+[(ctrl,n) for n in domains+daos]
        for i,(s,t) in enumerate(pairs):
            d=next(d for d in m['dependencies'] if d['source']==s and d['target']==t and d['allowed_on_layered_diagram']);a=c.nodes[s];b=c.nodes[t]
            if t in daos:
                lane=12+5*daos.index(t);pts=[(a[0],a[1]+35+4*daos.index(t)),(lane,a[1]+35+4*daos.index(t)),(lane,555),(b[0]+b[2]/2,555),(b[0]+b[2]/2,b[1])]
            else:pts=[(a[0]+a[2]/2,a[1]+a[3]),(b[0]+b[2]/2,b[1])]
            c.edge('dep'+str(i),d,pts);deps.append(d)
        c.finish(path,m,elements,deps)
    else:
        # Three isolated relation rows prevent crossings and attach labels to the
        # named source/target ends. Full member details occur only in member pages.
        for i,d0 in enumerate(p['relations']):
            pool=m['associations'] if d0['kind']!='dependency' else m['dependencies']
            d=next(d for d in pool if all(d.get(k)==d0.get(k) for k in ('source','target','kind')))
            y=125+i*187;s,t=d['source'],d['target'];sid='s'+str(i);tid='t'+str(i)
            elements+=[small_box(c,m,s,35,y,375,109,sid),small_box(c,m,t,790,y,375,109,tid)]
            c.text(sid+'_ref',refs(m,s),47,y+78,350);c.text(tid+'_ref',refs(m,t),802,y+78,350)
            pts=[(410,y+65),(790,y+65)];c.edge('rel'+str(i),d,pts,sid,tid);deps.append(d)
            label=d.get('role','uses') if d['kind']!='dependency' else 'depends on'+(' †' if d['status']!='MATCH' else '')
            c.text('label'+str(i),label,445,y+6,325)
            if d.get('source_multiplicity'):
                c.text('source_mult'+str(i),d['source_multiplicity'],437,y+37,90)
                tw=font().getlength(d['target_multiplicity']);c.text('target_mult'+str(i),d['target_multiplicity'],770-tw,y+37,100)
            if s=='HubMenuItem' or t=='HubMenuItem':c.text('association_note'+str(i),'Association class: Hub × MenuItem; availability belongs to this link.',35,y+123,1120)
        # Repeated reference cards are one canonical class in the metadata.
        elements=list({e['class']:e for e in elements}.values());c.finish(path,m,elements,deps)

def letters(number):
    s=''
    while number>=0:s=chr(number%26+65)+s;number=number//26-1
    return s

def planning():
    m=read_model();pages=[]
    # Member projections retain every canonical role and every declared method.
    # Only root-annotated diagram_omit scalars are removed, in favor of relations.
    for layer in ('view','controller','domain','data_access'):
        chunks=[]
        for name,c in m['classes'].items():
            if c['layer']!=layer:continue
            units=member_units(c);groups=[];group=[];count=0
            for unit in units:
                if group and count+len(unit['lines'])>18:groups.append(group);group=[];count=0
                group.append(unit);count+=len(unit['lines'])
            groups.append(group)
            for j,group in enumerate(groups):
                headerlen=len(wrap('«'+('association class' if c.get('association_class') else c['stereotype'])+'» '+name,510,18,True))
                section_count=len({u['kind'] for u in group})
                h=(headerlen+1+max(1,sum(len(u['lines']) for u in group)+section_count))*LH+21
                chunks.append({'class':name,'attributes':[u['name'] for u in group if u['kind']=='attribute'],'methods':[u['name'] for u in group if u['kind']=='method'],'part':f'members {j+1}/{len(groups)}','height':h})
        current=[];ys=[132,132];col=0
        for chunk in chunks:
            if ys[col]+chunk['height']>692:
                col+=1
                if col==2:pages.append({'projection':'members','layer':layer,'title':LAYERS[layer]+' members','subtitle':'Complete member projection; types and statuses resolve from the model.','cards':current});current=[];ys=[132,132];col=0
            chunk.update(x=40 if col==0 else 620,y=ys[col]);ys[col]+=chunk['height']+14;chunk.pop('height');current.append(chunk)
        if current:pages.append({'projection':'members','layer':layer,'title':LAYERS[layer]+' members','subtitle':'Complete member projection; types and statuses resolve from the model.','cards':current})
    member_count=len(pages)
    maps=[
      ('UC-01 / ordering','order','PlaceOrderController',['Quote','Order','Hub'],['OrderDAO','PaymentDAO','PaymentGatewaySimulator']),
      ('UC-02 / delivery','delivery','DeliveryController',['Delivery','Payment','UserAccount'],['DeliveryDAO','OrderDAO','PaymentDAO']),
      ('UC-03 / hubs','admin','HubController',['Hub','HubStatus'],['HubDAO','data_access.database']),
      ('UC-04 / reports','reports','ReportController',['Hub','HubStatus','OrderState'],['ReportDAO','HubDAO']),
      ('UC-05 / kitchen decisions','kitchen','KitchenController',['Order','ReplacementOffer','Delivery'],['OrderDAO','ReplacementOfferDAO','PaymentDAO']),
      ('UC-06 / catalogue','admin','MenuController',['Brand','MenuItem','HubMenuItem'],['MenuDAO','HubDAO','data_access.database']),
      ('SUC-01 / authentication','auth','AuthController',['UserAccount'],['UserDAO']),
      ('SUC-02 / profile and addresses','account','AccountController',['Customer','Address','UserAccount'],['CustomerDAO','data_access.database']),
      ('SUC-03 / SUC-04 / tracking','order','OrderTrackingController',['Order','Customer'],['OrderDAO','PaymentDAO','ReplacementOfferDAO']),
      ('SUC-07 / vouchers','admin','VoucherController',['Voucher','DiscountType'],['VoucherDAO','data_access.database']),
      ('SUC-08 / accounts','admin','UserAdminController',['UserAccount','Role','Hub'],['HubDAO','data_access.database']),
      ('SUC-09 / retained order history','admin','OrderArchiveController',['Order'],['OrderDAO','data_access.database'])]
    for title,view,ctrl,domains,daos in maps:pages.append({'projection':'layered','title':title,'subtitle':'Selected responsibility links; all declared members are in the member parts.','view':view,'controller':ctrl,'domains':domains,'daos':daos})
    # All canonical associations/generalizations are drawn, including support/error
    # inheritance. Enum dependencies are selected without duplicating associations.
    for start in range(0,len(m['associations']),3):pages.append({'projection':'relations','title':'Associations and generalizations','subtitle':'Named source is at left; each multiplicity belongs to its adjacent end.','relations':m['associations'][start:start+3]})
    enums=[d for d in m['dependencies'] if m['classes'][d['source']]['layer']=='domain' and m['classes'][d['target']]['stereotype']=='enumeration' and d['allowed_on_layered_diagram']]
    for start in range(0,len(enums),3):pages.append({'projection':'relations','title':'Domain enumeration dependencies','subtitle':'Real enums; state/flag/derived facts retain their original representations.','relations':enums[start:start+3]})
    SCRATCH.mkdir(parents=True,exist_ok=True)
    for i,p in enumerate(pages):
        p.update(figure='4.1'+letters(i),stem='dcd_subsystem_Part'+letters(i))
    global COVERAGE
    COVERAGE=collections.defaultdict(list)
    for p in pages[:member_count]:
        for card in p['cards']:
            if p['figure'] not in COVERAGE[card['class']]:COVERAGE[card['class']].append(p['figure'])
    for i,p in enumerate(pages):
        prev=pages[i-1]['figure'] if i else pages[-1]['figure'];nxt=pages[(i+1)%len(pages)]['figure']
        p['continuation']=f'Continues from Figure {prev}; continues in Figure {nxt}. Read 4.1A–4.1{letters(len(pages)-1)} together.'
        path=HERE/p['stem'];path.with_suffix('.json').write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf-8')
        path.with_suffix('.py').write_text('"""Author: 722I0004 · AI-assisted (Codex). Re-render this shared-model projection."""\nfrom pathlib import Path\nimport runpy, sys\nsys.dont_write_bytecode = True\nif __name__ == "__main__":\n    coordinator = Path(__file__).with_name("dcd_subsystem.py")\n    sys.argv = [str(coordinator), str(Path(__file__).with_suffix(".json"))]\n    runpy.run_path(str(coordinator), run_name="__main__")\n',encoding='utf-8')
    coverage={'class_count':len(m['classes']),'method_count':sum(len(c['methods']) for c in m['classes'].values()),'member_figures':member_count,'figure_count':len(pages),'roles':dict(COVERAGE),'dependency_selector':'Twelve labelled responsibility slices; domain→enum dependencies; all model associations/generalizations. Additional call/type/helper dependencies remain in the sole model and per-UC designs; forbidden import directions remain in report 4.2, P3-S04/P4.9.','excluded_classes':[],'excluded_attributes':[{'class':n,'attribute':a['name'],'reason':'Root diagram_omit annotation: domain foreign-key scalar replaced by named association.'} for n,c in m['classes'].items() for a in c['attributes'] if a.get('diagram_omit')]}
    (SCRATCH/'coverage.json').write_text(json.dumps(coverage,indent=2,ensure_ascii=False),encoding='utf-8')
    return pages

def get_coverage():
    coverage=collections.defaultdict(list)
    for path in HERE.glob('dcd_subsystem_Part*.json'):
        p=json.loads(path.read_text(encoding='utf-8'))
        if p['projection']=='members':
            for b in p['cards']:
                if p['figure'] not in coverage[b['class']]:coverage[b['class']].append(p['figure'])
    return coverage

COVERAGE=get_coverage()
if __name__=='__main__':
    if '--plan' in sys.argv:planning()
    target=Path(sys.argv[1]).resolve() if len(sys.argv)>1 and sys.argv[1]!='--plan' else None
    if target and target.stem.startswith('dcd_subsystem_Part'):render(target.with_suffix(''))
    else:
        for p in sorted(HERE.glob('dcd_subsystem_Part*.json')):render(p.with_suffix(''))
    print('Rendered subsystem DCD projections from',MODEL)
