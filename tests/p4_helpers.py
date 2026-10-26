"""P4 behavioral setup, never an independent pricing oracle. Author: 722I0004 · AI-assisted (Codex)."""
import uuid
from saigonbite.business.controllers import PlaceOrderController, PaymentChoice

def place(conn,user=1,hub=1,address=1,lines=None,payment=None,voucher=None,token=None):
    c=PlaceOrderController(conn)
    lines=lines if lines is not None else {1:'1'}
    q=c.request_quote(user,hub,address,lines,voucher)
    kwargs={}
    if hasattr(q,'fingerprint'):
        choice=payment or PaymentChoice()
        kwargs['quote_fingerprint']=q.fingerprint(choice.method,choice.option)
    return c.confirm_order(user,hub,address,lines,token or uuid.uuid4().hex,q.total,voucher,payment,**kwargs)
