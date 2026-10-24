"""Build split analysis domain model; all persistence comparisons remain Static.
Author: 722I0004 · AI-assisted (Codex). Shared renderer: use_case_diagram.py.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import importlib.util,json,shutil,xml.etree.ElementTree as ET
from pathlib import Path
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('p2_b_renderer',OUT/'use_case_diagram.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
Page=R.Page

def cls(p,name,x,y,w,attrs):
    return p.node(name,name,x,y,w,65+31*len(attrs),'class',attrs=attrs)
def ref(p,name,x,y,w=390):
    return p.node(name,'«reference» '+name,x,y,w,65,'ref','#F5F8FA')
def assoc(p,id,a,b,pts,ma,mb,pa,pb,label='',lp=None,kind='assoc'):
    p.edge(id,a,b,pts,label,*(lp or (0,0)),kind=kind,ends=[(ma,*pa),(mb,*pb)])
def build():
    pages=[]
    p=Page('domain_model_PartA','Domain model · identity, addresses and hub responsibility','2.2A',1800,1350)
    cls(p,'UserAccount',50,145,550,['id: Integer','username: String','password_hash: String','display_name: String','role: String','is_active: Boolean','created_at: DateTime'])
    cls(p,'Customer',740,145,460,['id: Integer','full_name: String'])
    cls(p,'Address',1300,145,450,['id: Integer','label: String','full_address: String','district: String','latitude: Real','longitude: Real','archived_at: DateTime?'])
    cls(p,'LocalCustomer',510,650,480,['phone: String','email: String?'])
    cls(p,'TouristCustomer',1110,650,530,['phone: String?','email: String','passport_no: String','nationality: String'])
    cls(p,'Hub',50,760,420,['id: Integer','code: String','name: String','address_text: String','latitude: Real','longitude: Real','max_active_orders: Integer','base_delivery_fee: Integer','archived_at: DateTime?'])
    assoc(p,'account_profile','UserAccount','Customer',[(600,205),(740,205)],'1','0..1',(615,165),(665,165))
    assoc(p,'addresses','Customer','Address',[(1200,205),(1300,205)],'1','0..*',(1205,165),(1250,215))
    p.edge('local_general','LocalCustomer','Customer',[(750,650),(750,580),(650,580),(650,250),(740,250)],kind='general')
    p.edge('tourist_general','TouristCustomer','Customer',[(1375,650),(1375,550),(1240,550),(1240,250),(1200,250)],kind='general')
    assoc(p,'kitchen_hub','UserAccount','Hub',[(260,427),(260,760)],'0..*','0..1',(275,448),(275,718),'works at\n{role = KITCHEN_STAFF}',(290,485))
    p.text(740,315,'Customer: {complete, disjoint}.\nOne CUSTOMER account per customer.\nOther roles have no Customer profile.',26)
    p.text(640,970,'Shipper is a UserAccount role (SHIPPER), not another class.\nA kitchen account has exactly one Hub; all other roles have none.\nBusy / quiet / workload are derived, never persisted Hub states.',26)
    p.text(640,1100,'? = optional value; money = Integer whole VND.\nDates use Date; timestamps use DateTime (UTC).\nNo methods or foreign-key attributes appear in this analysis model.',26)
    pages.append(p)
    p=Page('domain_model_PartB','Domain model · catalogue, hub listings and vouchers','2.2B',1800,1310)
    cls(p,'Brand',55,150,400,['id: Integer','name: String','archived_at: DateTime?'])
    cls(p,'MenuItem',665,150,530,['id: Integer','name: String','description: String','price: Integer','archived_at: DateTime?'])
    ref(p,'Hub',1350,150,390)
    # The association-class tether joins the Hub–MenuItem association itself.
    p.node('listing_link','',1270,245,4,4,'rect','white')
    assoc(p,'brand_items','Brand','MenuItem',[(455,215),(665,215)],'1','0..*',(475,171),(565,171),'offers',(490,240))
    assoc(p,'listed','MenuItem','Hub',[(1195,280),(1272,280),(1272,182),(1350,182)],'0..*','0..*',(1200,320),(1250,130),'listed at',(1320,255))
    cls(p,'HubMenuItem',1050,530,680,['is_available: Boolean'])
    p.edge('association_class','HubMenuItem','listing_link',[(1272,530),(1272,247)],kind='anchor')
    cls(p,'Voucher',55,530,800,['id: Integer','code: String','description: String','discount_type: String','discount_value: Integer','min_subtotal: Integer','max_discount: Integer?','valid_from: Date','valid_until: Date','archived_at: DateTime?'])
    p.text(1050,710,'HubMenuItem is the association class of\nHub ↔ MenuItem (one row per pair).\nListed row absent = unlisted.\nAvailable = true / false is per hub.',26)
    p.text(1050,895,'Catalogue archive never rewrites order snapshots.\nArchived brand or item cannot be ordered.\nHub details appear in Figure 2.2A.\nVoucher → Order appears in Figure 2.2C.',26)
    p.text(60,1105,'Quote, report filters/rows and receipts are computed views; they are not persistent classes.',26)
    pages.append(p)
    p=Page('domain_model_PartC','Domain model · order snapshots, payment, delivery and replacement','2.2C',1800,1490)
    cls(p,'Order',610,120,580,['id: Integer','delivery_address_text: String','distance_km: Real','state: String','item_subtotal: Integer','voucher_discount: Integer','delivery_fee: Integer','quiet_discount: Integer','total_amount: Integer','idempotency_token: String','reject_reason: String?','placed_at: DateTime','confirmed_at: DateTime?','ready_at: DateTime?','closed_at: DateTime?','archived_at: DateTime?'])
    cls(p,'Payment',1290,120,460,['id: Integer','method: String','online_option: String?','provider_ref: String?','state: String','amount: Integer','refund_amount: Integer','created_at: DateTime','updated_at: DateTime'])
    cls(p,'Delivery',1290,690,460,['id: Integer','state: String','ready_at: DateTime','picked_up_at: DateTime?','finished_at: DateTime?','failure_reason: String?','cash_collected: Integer?'])
    cls(p,'OrderLine',50,940,450,['id: Integer','item_name: String','unit_price: Integer','quantity: Integer'])
    cls(p,'ReplacementOffer',610,995,580,['id: Integer','original_item_name: String','original_unit_price: Integer','new_item_name: String','new_unit_price: Integer','state: String','offered_at: DateTime','decided_at: DateTime?'])
    for n,y in [('Customer',120),('Hub',330),('Address',540),('Voucher',750)]:ref(p,n,50,y,440)
    ref(p,'MenuItem',50,1250,450)
    ref(p,'UserAccount',1290,1085,460)
    p.node('NewMenuItem','«reference» MenuItem\n(replacement target)',1290,1240,460,100,'ref','#F5F8FA')
    for id,n,y,oy,m in [('cust','Customer',152,165,'1'),('hub','Hub',362,365,'1'),('address','Address',572,565,'1'),('voucher','Voucher',782,635,'0..1')]:
        assoc(p,id,n,'Order',[(490,y),(550,y),(550,oy),(610,oy)],m,'0..*',(500,y-37),(550,oy+10))
    assoc(p,'payment','Order','Payment',[(1190,260),(1290,260)],'1','1',(1200,220),(1250,280))
    assoc(p,'delivery','Order','Delivery',[(1190,640),(1240,640),(1240,760),(1290,760)],'1','0..1',(1200,598),(1210,780))
    assoc(p,'offers','Order','ReplacementOffer',[(1120,681),(1120,710),(1220,710),(1220,960),(1130,960),(1130,995)],'1','0..*',(1195,680),(1140,925),'offers',(1125,865))
    assoc(p,'lines','Order','OrderLine',[(650,681),(650,870),(275,870),(275,940)],'1','1..*',(665,690),(290,902),'contains',(315,830),'composition')
    assoc(p,'offer_line','ReplacementOffer','OrderLine',[(610,1100),(500,1100)],'0..*','1',(545,1060),(510,1120),'for line',(505,1160),'nav')
    assoc(p,'line_item','OrderLine','MenuItem',[(275,1129),(275,1250)],'0..*','1',(295,1145),(295,1210))
    assoc(p,'assigned','Delivery','UserAccount',[(1510,972),(1510,1085)],'0..*','0..1',(1525,985),(1525,1045),'shipper role',(1295,1010))
    assoc(p,'target_item','ReplacementOffer','NewMenuItem',[(1190,1280),(1290,1280)],'0..*','1',(1198,1235),(1245,1300),kind='nav')
    p.text(700,735,'S − D + F − Q = T (snapshots).\nONLINE amount = captured C.\nrefund_amount = owed, not paid.\nOne OFFERED offer per Order.\nOffer/line share the same Order.\nREFUNDED/payout deferred (L3).',26)
    pages.append(p)
    result=[p.export() for p in pages]
    for suffix in ['drawio','png','svg','json']:shutil.copyfile(OUT/f'domain_model_PartA.{suffix}',OUT/f'domain_model.{suffix}')
    combined=ET.Element('mxfile',{'host':'app.diagrams.net','type':'device'})
    for p in pages:combined.append(ET.parse(OUT/(p.stem+'.drawio')).getroot().find('diagram'))
    ET.indent(combined);ET.ElementTree(combined).write(OUT/'domain_model.drawio',encoding='utf-8',xml_declaration=True)
    (OUT/'domain_model.json').write_text(json.dumps({'parts':result,'main_image':'first-page alias; use every PartA–PartC in the report','author':'722I0004 · AI-assisted (Codex)','persistent_base_classes':['Hub','Brand','MenuItem','HubMenuItem','UserAccount','Customer','Address','Voucher','Order','OrderLine','Payment','Delivery','ReplacementOffer'],'subclasses':['LocalCustomer','TouristCustomer'],'reference_nodes':'repeat an existing class, never another persistent class'},indent=2),encoding='utf-8')
    return result
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');build();print('Domain exports generated; XML, endpoint and font checks passed.')
