"""Freeze analysis anchors and observable operation names before drafting."""
from pathlib import Path
import csv
import json
import re

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; DOC=REPO/'docs/part2'
PLAN=(ROOT/'PLAN_SaigonBite_Part2_Final.md').read_text(encoding='utf-8')
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'

def write(n,t):
    p=DOC/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t,encoding='utf-8')

def main():
    anchors=[]
    table=PLAN.split('**P2.3 Postcondition anchors',1)[1].split('Exit G2:',1)[0]
    # Semicolon is an anchor separator only when followed by another PC/MG token.
    maps={
      '01': [('confirmCheckout','BR-01; BR-02; BR-05; BR-06; BR-08; BR-09; BR-10; BR-11; BR-14')]*9,
      '02': [('takeDelivery','BR-25'),('confirmDelivered','BR-25'),('reportFailure','BR-17; BR-25'),('takeDelivery; confirmDelivered; reportFailure','BR-25')],
      '03': [('createHub; updateHub','BR-18'),('archiveHub','BR-18'),('createHub; updateHub; archiveHub','BR-18')],
      '04': [('salesReport; workloadReport; deliveryReport','BR-20; BR-21; BR-22; BR-23; BR-24'),('deliveryReport','BR-23'),('salesReport; workloadReport; deliveryReport','BR-24'),('salesReport; workloadReport; deliveryReport','plan §5.4')],
      '05': [('confirmOrder','BR-26'),('rejectOrder','BR-16; BR-17; BR-26'),('offerReplacement','BR-26; plan §3.3'),('acceptReplacement','plan §3.3'),('confirmOrder; offerReplacement; acceptReplacement','BR-26; plan §3.3')],
      '06': [('createBrand; updateBrand; archiveBrand; createMenuItem; updateMenuItem; archiveMenuItem','BR-19'),('listItemAtHub; unlistItemAtHub; setListingAvailability','BR-19'),('archiveBrand; archiveMenuItem; setListingAvailability','BR-19'),('updateMenuItem; archiveMenuItem; archiveBrand; unlistItemAtHub','BR-19'),('createBrand; updateBrand; createMenuItem; updateMenuItem; listItemAtHub','BR-19')]
    }
    for line in table.splitlines():
        if not line.startswith('| UC-'): continue
        uc,pcs,mgs=[x.strip() for x in line.strip('|').split('|')]
        n=uc[-2:]; i=0
        for field in (pcs,mgs):
            for entry in re.split(r'; (?=(?:PC|MG)\d\d )',field):
                tag,text=entry.split(' ',1); op,br=maps[n][i]; i+=1
                fact=text
                if tag.startswith('MG'): fact='Invariant / refusal outcome: '+text
                anchors.append([f'UC{n}-{tag}',uc,text,fact,br,op])
    with (DOC/'pc_mg_register.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['id','UC','text','state or stored fact','BR','ssd op']); w.writerows(anchors)
    rows=[]
    def add(op,params,ret,actor,uc,change,br,method,note='Contract operation; candidate mapping is Static only; P3 confirms design.'):
        ids='; '.join(a[0] for a in anchors if op in a[5].split('; '))
        rows.append([f'OP-{len(rows)+1:02}',op,params,ret,actor,uc,change,br,ids,method,note])
    common='session actor identity is supplied by authenticated context; never trusted from posted actor ID'
    add('confirmCheckout','hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken','placedOrderAndReceipt | existingOrder | revisedQuote | refusal | busySuggestions','Customer','UC-01','— → PLACED; insert snapshots, lines, COD PENDING / ONLINE PAID; load +1','BR-01–BR-14','PlaceOrderController.confirm_order (place_order_controller.py:86)','Contract fingerprint absent in draft (F-07). '+common)
    events=[
      ('confirmOrder','orderId','confirmedOrder | refusal','Kitchen staff','UC-05','PLACED → CONFIRMED; confirmed_at','BR-26; no open offer','KitchenController.confirm_order'),
      ('rejectOrder','orderId, reason','rejectedOrder | refusal','Kitchen staff','UC-05','PLACED → REJECTED; offer WITHDRAWN; BR-17; closed_at','BR-16; BR-17; BR-26','KitchenController.reject_order'),
      ('offerReplacement','orderId, orderLineId, targetItemId','offeredReplacement | refusal','Kitchen staff','UC-05','PLACED → PLACED; insert OFFERED','plan §3.3 1–3; BR-26','KitchenController.offer_replacement'),
      ('acceptReplacement','orderId, offerId','acceptedOrderAndAmounts | withdrawnOfferAndReason | staleRefusal','Customer','SUC-03; UC-05','PLACED → PLACED; offer ACCEPTED; line/totals/payment; invalid target → WITHDRAWN only','plan §3.3 5–7','OrderTrackingController.answer_replacement (accept=True)'),
      ('declineReplacement','orderId, offerId','rejectedOrderAndAmounts | staleRefusal','Customer','SUC-03; UC-05','PLACED → REJECTED; offer DECLINED; BR-17','plan §3.3 8; BR-17','OrderTrackingController.answer_replacement (accept=False)'),
      ('cancelOrder','orderId','cancelledOrderAndAmounts | refusal','Customer','SUC-04; UC-01','PLACED / CONFIRMED → CANCELLED; offer WITHDRAWN; BR-17','BR-15; BR-17','OrderTrackingController.cancel_order'),
      ('startPreparing','orderId','preparingOrder | refusal','Kitchen staff','SUC-05; UC-05','CONFIRMED → PREPARING','BR-26; no open offer','KitchenController.start_preparing'),
      ('markReady','orderId','readyOrderAndDelivery | refusal','Kitchen staff','SUC-05; UC-02','PREPARING → READY; insert Delivery AWAITING_PICKUP; ready_at','BR-26','KitchenController.mark_ready'),
      ('takeDelivery','orderId','assignedDelivery | refusal','Shipper','UC-02','READY → OUT_FOR_DELIVERY; AWAITING_PICKUP → PICKED_UP; shipper and time','BR-25; unassigned','DeliveryController.pick_up'),
      ('confirmDelivered','orderId, cashCollected?','deliveredOrderAndPayment | refusal','Shipper','UC-02','OUT_FOR_DELIVERY → DELIVERED; Delivery DELIVERED; COD PAID; finish/close time','BR-25; assigned; COD cash = T','DeliveryController.confirm_delivered'),
      ('reportFailure','orderId, reason','failedOrderAndPayment | refusal','Shipper','UC-02','OUT_FOR_DELIVERY → DELIVERY_FAILED; Delivery FAILED; reason; BR-17; finish/close time','BR-17; BR-25; assigned','DeliveryController.report_failure')]
    for e in events: add(*e)
    queries=[
      ('browseHubs','', 'activeHubsWithLoadAndCapacity','Customer','UC-01','BR-01; BR-02; BR-03','PlaceOrderController.list_hubs'),
      ('selectHub','hubId','availableMenuAndOwnAddresses | refusal','Customer','UC-01','BR-19','PlaceOrderController.select_hub'),
      ('requestQuote','hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?','quoteWithFingerprintAndSD FQT | refusal | busySuggestions','Customer','UC-01','BR-01–BR-10; BR-14','PlaceOrderController.request_quote (payment/fingerprint gap for P4)'),
      ('viewReceipt','orderId','ownOrderReceipt | refusal','Customer','SUC-03; UC-01','BR-12; BR-13','OrderTrackingController.get_order (receipt formatting in presentation; Static)'),
      ('viewMyOrders','', 'ownOrdersAndOpenOffers','Customer','SUC-03','BR-12','OrderTrackingController.list_my_orders'),
      ('viewReplacement','orderId','originalAndOfferedLineQuantityTotalRefundOwed | refusal','Customer','SUC-03; UC-05','plan §3.3 4','OrderTrackingController.get_order'),
      ('viewKitchenOrders','', 'ownHubOrdersAndOffers','Kitchen staff','UC-05','BR-26','KitchenController.board'),
      ('viewKitchenOrder','orderId','ownHubOrderAndLines | refusal','Kitchen staff','UC-05','BR-12; BR-26','KitchenController.get_order'),
      ('viewReadyDeliveries','', 'readyAndOwnAssignedDeliveries','Shipper','UC-02','BR-12; BR-25','DeliveryController.board'),
      ('viewDelivery','orderId','deliveryContactSnapshotAndCashDue | refusal','Shipper','UC-02','BR-12; BR-25','DeliveryController.get_delivery'),
      ('listHubs','includeArchived?', 'hubRecordsAndLoad','Admin','UC-03','BR-18','HubController.list_hubs'),
      ('getHub','hubId','hubAndArchiveGuard | refusal','Admin','UC-03','BR-18','HubController.get_hub'),
      ('listCatalogue','hubId?', 'brandsItemsHubsAndListings','Admin','UC-06','BR-19','MenuController.catalogue; hub_menu'),
      ('salesReport','startDateVN, endDateVN, hubId?','operationalSalesAndRefundsOwed | invalidFilter | denied','Manager','UC-04','BR-20; BR-21; BR-24','ReportController.sales_report'),
      ('workloadReport','', 'currentHubLoadCapacityReadyOutForDelivery | denied','Manager','UC-04','BR-01; BR-22; BR-24','ReportController.workload_report'),
      ('deliveryReport','startDateVN, endDateVN, hubId?','waitRideFailureRatesWithNAndNA | invalidFilter | denied','Manager','UC-04','BR-20; BR-23; BR-24','ReportController.delivery_report'),
      ('listAvailability','', 'ownHubListings','Kitchen staff','SUC-06','BR-26','KitchenController.list_availability'),
      ('viewProfile','', 'ownCustomerAndAddresses','Customer','SUC-02','BR-12','AccountController.get_profile'),
      ('listVouchers','', 'voucherRecords','Admin','SUC-07','BR-08','VoucherController.list_vouchers'),
      ('listUsers','', 'userAccountsAndPermittedCustomerDetails','Admin','SUC-08','BR-12; BR-25','UserAdminController.list_users'),
      ('viewArchivedOrders','', 'authorizedClosedHistoryIncludingChildren','Admin','SUC-09','BR-24','OrderArchiveController.list_archived')]
    for op,params,ret,actor,uc,br,method in queries: add(op,params,ret,actor,uc,'Read only; zero persistent writes',br,method)
    crud=[
      ('createHub','code, name, address, latitude, longitude, baseDeliveryFee, capacity','Admin','UC-03','new ACTIVE Hub','BR-18','HubController.create_hub'),
      ('updateHub','hubId, code, name, address, latitude, longitude, baseDeliveryFee, capacity','Admin','UC-03','valid Hub attributes updated','BR-18','HubController.update_hub'),
      ('archiveHub','hubId','Admin','UC-03','ACTIVE → ARCHIVED','BR-18; no open orders','HubController.archive_hub'),
      ('createBrand','name','Admin','UC-06','new ACTIVE Brand','BR-19','MenuController.create_brand'),
      ('updateBrand','brandId, name','Admin','UC-06','Brand name updated; snapshots unchanged','BR-19','MenuController.rename_brand'),
      ('archiveBrand','brandId','Admin','UC-06','Brand ACTIVE → ARCHIVED; descendants hidden operationally','BR-19','MenuController.archive_brand'),
      ('createMenuItem','brandId, name, description, price','Admin','UC-06','new ACTIVE MenuItem','BR-19','MenuController.create_item'),
      ('updateMenuItem','itemId, brandId, name, description, price','Admin','UC-06','MenuItem attributes updated; snapshots unchanged','BR-19','MenuController.update_item'),
      ('archiveMenuItem','itemId','Admin','UC-06','MenuItem ACTIVE → ARCHIVED','BR-19','MenuController.archive_item'),
      ('listItemAtHub','hubId, itemId, available','Admin','UC-06','create HubMenuItem AVAILABLE / SOLD_OUT','BR-19; active parents','MenuController.list_item_at_hub; set_availability (initial availability mapping needs P3 confirmation)'),
      ('setListingAvailability','hubId, itemId, available','Admin','UC-06','AVAILABLE ↔ SOLD_OUT','BR-19','MenuController.set_availability'),
      ('unlistItemAtHub','hubId, itemId','Admin','UC-06','listing removed; snapshots unchanged','BR-19','MenuController.unlist_item_at_hub'),
      ('setMenuAvailability','itemId, available','Kitchen staff','SUC-06','own-hub AVAILABLE ↔ SOLD_OUT','BR-19; BR-26','KitchenController.set_availability'),
      ('registerCustomer','username, password, type, fullName, phone?, email?, passport?, nationality?','Customer','SUC-02','create UserAccount ACTIVE and Local/Tourist Customer','BR-12','AccountController.register'),
      ('updateProfile','fullName, phone?, email?, passport?, nationality?','Customer','SUC-02','own profile updated','BR-12','AccountController.update_profile'),
      ('addAddress','label, fullAddress, district','Customer','SUC-02','new own Address','BR-12; BR-05','AccountController.add_address'),
      ('updateAddress','addressId, label, fullAddress, district','Customer','SUC-02','own Address updated; order snapshots unchanged','BR-12; BR-05','AccountController.update_address'),
      ('archiveAddress','addressId','Customer','SUC-02','own Address archived; history preserved','BR-12','AccountController.archive_address'),
      ('createVoucher','code, type, value, minSubtotal, maxDiscount?, validFrom, validUntil','Admin','SUC-07','new active Voucher','BR-08','VoucherController.create_voucher'),
      ('updateVoucher','voucherId, code, type, value, minSubtotal, maxDiscount?, validFrom, validUntil','Admin','SUC-07','Voucher updated; snapshots unchanged','BR-08','VoucherController.update_voucher'),
      ('archiveVoucher','voucherId','Admin','SUC-07','Voucher archived','BR-08','VoucherController.archive_voucher'),
      ('createUserAccount','username, password, displayName, role, hubId?','Admin','SUC-08','new ACTIVE staff account','BR-25; BR-26','UserAdminController.create_staff'),
      ('updateUserAccount','targetId, displayName, role, hubId?','Admin','SUC-08','account attributes updated','BR-25; BR-26','UserAdminController.update_user'),
      ('setUserActive','targetId, active','Admin','SUC-08','ACTIVE ↔ INACTIVE; session rejected next request','BR-25; no PICKED_UP delivery on deactivation','UserAdminController.set_active'),
      ('archiveClosedOrder','orderId','Admin','SUC-09','closed Order and children hidden operationally; authorized history retained','BR-24; terminal order only','No per-ID method: OrderArchiveController.archive is batch by closed_before (Static gap; P3/P4)')]
    for op,params,actor,uc,change,br,method in crud: add(op,params,'savedRecord | controlledRefusal',actor,uc,change,br,method)
    add('logIn','username, password','authenticatedRoleContext | denied','All human actors','SUC-01','authenticated session; no domain row mutation','plan §5.4','AuthController.authenticate')
    add('logOut','','sessionEnded','All human actors','SUC-01','session invalidated; no domain row mutation','plan §5.4','No controller method; presentation auth blueprint logout (Static)')
    with (DOC/'ssd_operations.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['op_id','operation','parameters','returns','actor','UC/SUC','state change (plan §4)','guards (BR)','PC/MG','candidate controller method (Static)','note']); w.writerows(rows)
    print(len(anchors),'anchors;',len(rows),'operations')

if __name__=='__main__': main()
