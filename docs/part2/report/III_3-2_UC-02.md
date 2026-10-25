# 3.2 Design for Use Case 2: Deliver an order: pick up, deliver with cash collection, or report failure (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

Baseline: 45ac76221b0a103174c7c01d17577e6e49cfd665. All application observations below are Static from the frozen AST inventory and shared model. Target behavior marked † is not a test or runtime result.

## 3.2.1 Design Classes in Detailed Design

One typed table per participating class/module follows.

<!-- include: ../UC-02/design_classes.md -->

## 3.2.2 Design Class Diagram

### i. Domain design class

Order, Delivery and Payment retain their real lifecycle roles; their associations carry persisted relationships. Hub, Customer and UserAccount are read participants. Passport is excluded from the shipper projection.

![UC-02 domain design classes: Lifecycle classes continue in Part B for party/hub associations.](../../../models/UC-02/dcd_uc02_domain_PartA.png)

Figure 3.2.2.i-A. UC-02 domain design classes: Lifecycle classes continue in Part B for party/hub associations. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_domain_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_domain_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_domain_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_domain_PartA.json)

![UC-02 domain design classes: Part A continues here. Domain FK scalars are omitted in favour of these navigable associations.](../../../models/UC-02/dcd_uc02_domain_PartB.png)

Figure 3.2.2.i-B. UC-02 domain design classes: Part A continues here. Domain FK scalars are omitted in favour of these navigable associations. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_domain_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_domain_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_domain_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_domain_PartB.json)

### ii. Controller

DeliveryController coordinates active-shipper checks, pickup/finish/failure work and the returned delivery view. The shared controllers.common module owns the real order/payment helper functions.

![UC-02 controller/value roles: Read and pickup operations continue in Part B.](../../../models/UC-02/dcd_uc02_controller_PartA.png)

Figure 3.2.2.ii-A. UC-02 controller/value roles: Read and pickup operations continue in Part B. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_controller_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_controller_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_controller_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_controller_PartA.json)

![UC-02 controller/value roles: Part A continues through the two mutually exclusive completion outcomes.](../../../models/UC-02/dcd_uc02_controller_PartB.png)

Figure 3.2.2.ii-B. UC-02 controller/value roles: Part A continues through the two mutually exclusive completion outcomes. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_controller_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_controller_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_controller_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_controller_PartB.json)

### iii. UI (view)

saigonbite.presentation.delivery is the «view» blueprint module; its route functions are operations with METHOD/rule metadata, not an invented view class.

![UC-02 view module](../../../models/UC-02/dcd_uc02_view.png)

Figure 3.2.2.iii. UC-02 view module — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_view.drawio) · [SVG](../../../models/UC-02/dcd_uc02_view.svg) · [Generator](../../../models/UC-02/dcd_uc02_view.py) · [Data](../../../models/UC-02/dcd_uc02_view.json)

### iv. Data access

The DAO projection includes only methods relevant to these five SSD occurrences. Section III shows persistence notes, not DAO or SQL messages; transaction detail is deferred to 4.3.2.

![UC-02 data-access classes](../../../models/UC-02/dcd_uc02_dao.png)

Figure 3.2.2.iv. UC-02 data-access classes — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_dao.drawio) · [SVG](../../../models/UC-02/dcd_uc02_dao.svg) · [Generator](../../../models/UC-02/dcd_uc02_dao.py) · [Data](../../../models/UC-02/dcd_uc02_dao.json)

### v. Design class (all layers together)

Parts A-J are operation-aligned views across the same four layers, with mutual continuation notes. The integrated DCD keeps receiver names/return types compact; exact signatures remain in the class tables and filtered layer diagrams.

![UC-02 all layers: Ready board authorization and retrieval](../../../models/UC-02/dcd_uc02_all_PartA.png)

Figure 3.2.2.v-A. UC-02 all layers: Ready board authorization and retrieval — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartA.json)

![UC-02 all layers: Board row projection](../../../models/UC-02/dcd_uc02_all_PartB.png)

Figure 3.2.2.v-B. UC-02 all layers: Board row projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartB.json)

![UC-02 all layers: Inspect assignment and access](../../../models/UC-02/dcd_uc02_all_PartC.png)

Figure 3.2.2.v-C. UC-02 all layers: Inspect assignment and access — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartC.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartC.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartC.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartC.json)

![UC-02 all layers: Delivery contact projection](../../../models/UC-02/dcd_uc02_all_PartD.png)

Figure 3.2.2.v-D. UC-02 all layers: Delivery contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartD.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartD.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartD.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartD.json)

![UC-02 all layers: Atomic pickup and paired Order transition](../../../models/UC-02/dcd_uc02_all_PartE.png)

Figure 3.2.2.v-E. UC-02 all layers: Atomic pickup and paired Order transition — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartE.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartE.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartE.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartE.json)

![UC-02 all layers: Successful delivery and paired states](../../../models/UC-02/dcd_uc02_all_PartF.png)

Figure 3.2.2.v-F. UC-02 all layers: Successful delivery and paired states — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartF.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartF.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartF.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartF.json)

![UC-02 all layers: Failure state and full refund obligation](../../../models/UC-02/dcd_uc02_all_PartG.png)

Figure 3.2.2.v-G. UC-02 all layers: Failure state and full refund obligation — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartG.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartG.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartG.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartG.json)

![UC-02 all layers: Completion contact and cash projection](../../../models/UC-02/dcd_uc02_all_PartH.png)

Figure 3.2.2.v-H. UC-02 all layers: Completion contact and cash projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartH.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartH.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartH.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartH.json)

![UC-02 all layers: Contact and archived-hub projection](../../../models/UC-02/dcd_uc02_all_PartI.png)

Figure 3.2.2.v-I. UC-02 all layers: Contact and archived-hub projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartI.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartI.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartI.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartI.json)

![UC-02 all layers: Completion contact projection](../../../models/UC-02/dcd_uc02_all_PartJ.png)

Figure 3.2.2.v-J. UC-02 all layers: Completion contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartJ.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartJ.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartJ.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartJ.json)

## 3.2.3 OOD with CRC Cards or Communication Diagram

The CRC include lists actual collaborators from the AST-derived call/type model and distinguishes controller values from domain entities.

<!-- include: ../UC-02/crc.md -->

## 3.2.4 OOD with Sequence Diagram

Every sequence keeps the exact SSD operation/parameter string at the actor-to-view boundary, then maps it to real blueprint/controller/domain methods. Solid arrows are calls; dashed arrows are results. Dataclass creation and property reads are distinct from business methods. No DAO or SQL appears; persistence is noted for 4.3.2. † identifies target transaction/rowcount/commit/busy behavior, not C0 success.

### viewReadyDeliveries — no parameters

OP-21 viewReadyDeliveries() — models/UC-02/ssd_uc02_PartA.drawio#M01

![UC-02 design sequence: viewReadyDeliveries](../../../models/UC-02/seq_uc02_viewReadyDeliveries.png)

Figure 3.2.4.1. UC-02 design sequence: viewReadyDeliveries — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_viewReadyDeliveries.drawio) · [SVG](../../../models/UC-02/seq_uc02_viewReadyDeliveries.svg) · [Generator](../../../models/UC-02/seq_uc02_viewReadyDeliveries.py) · [Data](../../../models/UC-02/seq_uc02_viewReadyDeliveries.json)

### viewDelivery — orderId

OP-22 viewDelivery(orderId) — models/UC-02/ssd_uc02_PartA.drawio#M02

![UC-02 design sequence: viewDelivery](../../../models/UC-02/seq_uc02_viewDelivery.png)

Figure 3.2.4.2. UC-02 design sequence: viewDelivery — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_viewDelivery.drawio) · [SVG](../../../models/UC-02/seq_uc02_viewDelivery.svg) · [Generator](../../../models/UC-02/seq_uc02_viewDelivery.py) · [Data](../../../models/UC-02/seq_uc02_viewDelivery.json)

### takeDelivery — orderId

OP-10 takeDelivery(orderId) — models/UC-02/ssd_uc02_PartA.drawio#M03

![UC-02 design sequence: takeDelivery](../../../models/UC-02/seq_uc02_takeDelivery.png)

Figure 3.2.4.3. UC-02 design sequence: takeDelivery — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_takeDelivery.drawio) · [SVG](../../../models/UC-02/seq_uc02_takeDelivery.svg) · [Generator](../../../models/UC-02/seq_uc02_takeDelivery.py) · [Data](../../../models/UC-02/seq_uc02_takeDelivery.json)

### confirmDelivered — orderId, cashCollected?

OP-11 confirmDelivered(orderId, cashCollected?) — models/UC-02/ssd_uc02_PartB.drawio#M04

![UC-02 design sequence: confirmDelivered](../../../models/UC-02/seq_uc02_confirmDelivered.png)

Figure 3.2.4.4. UC-02 design sequence: confirmDelivered — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_confirmDelivered.drawio) · [SVG](../../../models/UC-02/seq_uc02_confirmDelivered.svg) · [Generator](../../../models/UC-02/seq_uc02_confirmDelivered.py) · [Data](../../../models/UC-02/seq_uc02_confirmDelivered.json)

### reportFailure — orderId, reason

OP-12 reportFailure(orderId, reason) — models/UC-02/ssd_uc02_PartB.drawio#M05

![UC-02 design sequence: reportFailure](../../../models/UC-02/seq_uc02_reportFailure.png)

Figure 3.2.4.5. UC-02 design sequence: reportFailure — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_reportFailure.drawio) · [SVG](../../../models/UC-02/seq_uc02_reportFailure.svg) · [Generator](../../../models/UC-02/seq_uc02_reportFailure.py) · [Data](../../../models/UC-02/seq_uc02_reportFailure.json)

## 3.2.5 Final Design Class Diagram

All message receivers in the five design sequences are present. Changes from 3.2.2: none in the class/method/association set; the final views repeat the operation-partitioned all-layer diagrams after sequence reconciliation.

![UC-02 final design classes: Ready board authorization and retrieval](../../../models/UC-02/dcd_uc02_final_PartA.png)

Figure 3.2.5-A. UC-02 final design classes: Ready board authorization and retrieval — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartA.json)

![UC-02 final design classes: Board row projection](../../../models/UC-02/dcd_uc02_final_PartB.png)

Figure 3.2.5-B. UC-02 final design classes: Board row projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartB.json)

![UC-02 final design classes: Inspect assignment and access](../../../models/UC-02/dcd_uc02_final_PartC.png)

Figure 3.2.5-C. UC-02 final design classes: Inspect assignment and access — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartC.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartC.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartC.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartC.json)

![UC-02 final design classes: Delivery contact projection](../../../models/UC-02/dcd_uc02_final_PartD.png)

Figure 3.2.5-D. UC-02 final design classes: Delivery contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartD.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartD.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartD.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartD.json)

![UC-02 final design classes: Atomic pickup and paired Order transition](../../../models/UC-02/dcd_uc02_final_PartE.png)

Figure 3.2.5-E. UC-02 final design classes: Atomic pickup and paired Order transition — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartE.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartE.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartE.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartE.json)

![UC-02 final design classes: Successful delivery and paired states](../../../models/UC-02/dcd_uc02_final_PartF.png)

Figure 3.2.5-F. UC-02 final design classes: Successful delivery and paired states — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartF.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartF.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartF.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartF.json)

![UC-02 final design classes: Failure state and full refund obligation](../../../models/UC-02/dcd_uc02_final_PartG.png)

Figure 3.2.5-G. UC-02 final design classes: Failure state and full refund obligation — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartG.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartG.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartG.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartG.json)

![UC-02 final design classes: Completion contact and cash projection](../../../models/UC-02/dcd_uc02_final_PartH.png)

Figure 3.2.5-H. UC-02 final design classes: Completion contact and cash projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartH.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartH.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartH.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartH.json)

![UC-02 final design classes: Contact and archived-hub projection](../../../models/UC-02/dcd_uc02_final_PartI.png)

Figure 3.2.5-I. UC-02 final design classes: Contact and archived-hub projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartI.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartI.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartI.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartI.json)

![UC-02 final design classes: Completion contact projection](../../../models/UC-02/dcd_uc02_final_PartJ.png)

Figure 3.2.5-J. UC-02 final design classes: Completion contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartJ.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartJ.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartJ.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartJ.json)

Every received sequence method appears on its actual receiver in the final DCD: blueprint routes, DeliveryController/BaseController helpers, controllers.common functions, domain move_to/refund behavior and controller value roles. The operation-specific P4 targets remain †; the final DCD does not imply those behaviors already pass at C0.

## Integration repair evidence

Author: 722I0004 · AI-assisted (Codex)

The diagrams and typed metadata were refreshed against the corrected root-owned shared model. Allowed layered dependencies are drawn; actual upward DAO-to-domain imports are retained only as the static P4.9 architecture finding in report 4.2, not as permitted arrows. Shared transaction targets P2-S13/P3-S03 remain target behavior for guarded writes, commit failures and busy handling. Read paths remain read-only. Native draw.io XML and connected edge endpoints are structurally checked; native-app editing and final report placement remain UNTESTED.

DeliveryController calls the Delivery and Payment domain receivers. The local variable delivery is resolved to Delivery; it is not an upward call to the delivery blueprint.
