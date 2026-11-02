# 3.2 Design for Use Case 2: Deliver an order: pick up, deliver with cash collection, or report failure (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

The design was recorded as a target at C0 (`45ac762`); P4 resolution records 5 UC-02 entries, with their scoped evidence and limitations in the P4 status appendix. The † symbol in a diagram refers to the historical C0 target, not a current implementation verdict.

## 3.2.1 Design Classes in Detailed Design

One typed table per participating class/module follows.

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-02_design_classes.md -->

## 3.2.2 Design Class Diagram

### i. Domain design class

Order, Delivery and Payment retain their real lifecycle roles; their associations carry persisted relationships. Hub, Customer and UserAccount are read participants. Passport is excluded from the shipper projection.

![UC-02 domain design classes: Lifecycle classes continue in Part B for party/hub associations.](../../../models/UC-02/dcd_uc02_domain_PartA.png)

Figure 3.2.2.i-A. UC-02 domain design classes: Lifecycle classes continue in Part B for party/hub associations. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 domain design classes: Part A continues here. Domain FK scalars are omitted in favour of these navigable associations.](../../../models/UC-02/dcd_uc02_domain_PartB.png)

Figure 3.2.2.i-B. UC-02 domain design classes: Part A continues here. Domain FK scalars are omitted in favour of these navigable associations. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### ii. Controller

DeliveryController coordinates active-shipper checks, pickup/finish/failure work and the returned delivery view. The shared controllers.common module owns the real order/payment helper functions.

![UC-02 controller/value roles: Read and pickup operations continue in Part B.](../../../models/UC-02/dcd_uc02_controller_PartA.png)

Figure 3.2.2.ii-A. UC-02 controller/value roles: Read and pickup operations continue in Part B. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 controller/value roles: Part A continues through the two mutually exclusive completion outcomes.](../../../models/UC-02/dcd_uc02_controller_PartB.png)

Figure 3.2.2.ii-B. UC-02 controller/value roles: Part A continues through the two mutually exclusive completion outcomes. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### iii. UI (view)

saigonbite.presentation.delivery is the «view» blueprint module; its route functions are operations with METHOD/rule metadata, not an invented view class.

![UC-02 view module](../../../models/UC-02/dcd_uc02_view.png)

Figure 3.2.2.iii. UC-02 view module — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### iv. Data access

The DAO projection includes only methods relevant to these five SSD occurrences. Section III shows persistence notes, not DAO or SQL messages; transaction detail is deferred to 4.3.2.

![UC-02 data-access classes](../../../models/UC-02/dcd_uc02_dao.png)

Figure 3.2.2.iv. UC-02 data-access classes — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### v. Design class (all layers together)

Parts A-J are operation-aligned views across the same four layers, with mutual continuation notes. The integrated DCD keeps receiver names/return types compact; exact signatures remain in the class tables and filtered layer diagrams.

![UC-02 all layers: Ready board authorization and retrieval](../../../models/UC-02/dcd_uc02_all_PartA.png)

Figure 3.2.2.v-A. UC-02 all layers: Ready board authorization and retrieval — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Board row projection](../../../models/UC-02/dcd_uc02_all_PartB.png)

Figure 3.2.2.v-B. UC-02 all layers: Board row projection — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Inspect assignment and access](../../../models/UC-02/dcd_uc02_all_PartC.png)

Figure 3.2.2.v-C. UC-02 all layers: Inspect assignment and access — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Delivery contact projection](../../../models/UC-02/dcd_uc02_all_PartD.png)

Figure 3.2.2.v-D. UC-02 all layers: Delivery contact projection — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Atomic pickup and paired Order transition](../../../models/UC-02/dcd_uc02_all_PartE.png)

Figure 3.2.2.v-E. UC-02 all layers: Atomic pickup and paired Order transition — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Successful delivery and paired states](../../../models/UC-02/dcd_uc02_all_PartF.png)

Figure 3.2.2.v-F. UC-02 all layers: Successful delivery and paired states — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Failure state and full refund obligation](../../../models/UC-02/dcd_uc02_all_PartG.png)

Figure 3.2.2.v-G. UC-02 all layers: Failure state and full refund obligation — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Completion contact and cash projection](../../../models/UC-02/dcd_uc02_all_PartH.png)

Figure 3.2.2.v-H. UC-02 all layers: Completion contact and cash projection — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Contact and archived-hub projection](../../../models/UC-02/dcd_uc02_all_PartI.png)

Figure 3.2.2.v-I. UC-02 all layers: Contact and archived-hub projection — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-02 all layers: Completion contact projection](../../../models/UC-02/dcd_uc02_all_PartJ.png)

Figure 3.2.2.v-J. UC-02 all layers: Completion contact projection — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



## 3.2.3 OOD with CRC Cards or Communication Diagram

The CRC include lists actual collaborators from the AST-derived call/type model and distinguishes controller values from domain entities.

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-02_crc.md -->

## 3.2.4 OOD with Sequence Diagram

Every sequence keeps the exact SSD operation/parameter string at the actor-to-view boundary, then maps it to real blueprint/controller/domain methods. Solid arrows are calls; dashed arrows are results. Dataclass creation and property reads are distinct from business methods. No DAO or SQL appears; persistence is noted for 4.3.2. The historical annotation identifies target transaction/rowcount/commit/busy behavior, not C0 success.

### viewReadyDeliveries — no parameters

OP-21 viewReadyDeliveries() — models/UC-02/ssd_uc02_PartA.drawio#M01

![UC-02 design sequence: viewReadyDeliveries](../../../models/UC-02/seq_uc02_viewReadyDeliveries.png)

Figure 3.2.4.1. UC-02 design sequence: viewReadyDeliveries — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### viewDelivery — orderId

OP-22 viewDelivery(orderId) — models/UC-02/ssd_uc02_PartA.drawio#M02

![UC-02 design sequence: viewDelivery](../../../models/UC-02/seq_uc02_viewDelivery.png)

Figure 3.2.4.2. UC-02 design sequence: viewDelivery — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### takeDelivery — orderId

OP-10 takeDelivery(orderId) — models/UC-02/ssd_uc02_PartA.drawio#M03

![UC-02 design sequence: takeDelivery](../../../models/UC-02/seq_uc02_takeDelivery.png)

Figure 3.2.4.3. UC-02 design sequence: takeDelivery — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### confirmDelivered — orderId, cashCollected?

OP-11 confirmDelivered(orderId, cashCollected?) — models/UC-02/ssd_uc02_PartB.drawio#M04

![UC-02 design sequence: confirmDelivered](../../../models/UC-02/seq_uc02_confirmDelivered.png)

Figure 3.2.4.4. UC-02 design sequence: confirmDelivered — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### reportFailure — orderId, reason

OP-12 reportFailure(orderId, reason) — models/UC-02/ssd_uc02_PartB.drawio#M05

![UC-02 design sequence: reportFailure](../../../models/UC-02/seq_uc02_reportFailure.png)

Figure 3.2.4.5. UC-02 design sequence: reportFailure — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



## 3.2.5 Final Design Class Diagram
Author: 722I0004 · AI-assisted (Claude)

The final design class diagram refines the layer views of 3.2.2 with what the sequence diagrams in 3.2.4 and the implementation settled:

- **One diagram, four layers.** View (Flask blueprint functions with their routes), controller, domain and data access are drawn together, so every message in the sequence diagrams can be followed from the screen to the table.
- **Only the members this use case calls.** The sequence diagrams fixed which operations each class must offer; the complete member lists stay in the 3.2.1 tables and 3.2.2 views.
- **Signatures from the code.** Parameter names and types are read from the source at the release commit by `models/shared/final_dcd.py`, so the diagram and the program cannot differ.
- **Navigability and persistence.** Dashed arrows show which layer calls which; each DAO has a «persists» link to the entity it stores; domain associations keep their multiplicities from the domain model (2.1.7).

![UC-02 final design class diagram](../../../models/UC-02/dcd_uc02_final_overview.png)

Figure 3.2.5. UC-02 final design class diagram — Author: 722I0004 · AI-assisted (Claude).

Behaviour refined between the first design and the final design (each refinement is covered by the tests in 5.1). Every state-changing operation runs in one `BEGIN IMMEDIATE` transaction and checks the row count of each guarded UPDATE, so a stale page, a guessed ID or a competing user changes nothing.

| System operation | Refinement in the final design |
|---|---|
| `takeDelivery` | Taking a delivery is a guarded UPDATE: only one of two competing shippers succeeds. |
| `confirmDelivered` | Only the assigned shipper can finish; COD cash must equal the order total. |
| `reportFailure` | A failed delivery voids COD or records the full online amount as refund owed. |

Editable sources: `models/UC-02/dcd_uc02_final_overview.dot` (Graphviz), with SVG exports beside them.

## Integration repair evidence


The diagrams and typed metadata were refreshed against the corrected shared model. Allowed layered dependencies are drawn; the twelve retained dependency-policy entries are documented as static policy checks in report 4.2 and Table P4-1, not as runtime tests. P2-S13/P3-S03 identified C0 targets for guarded writes, commit failures and busy handling; their final scoped evidence is recorded in Table P4-1. Read paths remain read-only.

DeliveryController calls the Delivery and Payment domain receivers. The local variable delivery is resolved to Delivery; it is not an upward call to the delivery blueprint.

Diagram notation (R1–R4): every displayed association now has separate multiplicity text at its actual attached source and target ends, plus a separate role label. The initial SSD request precedes actual accepted/refused interaction operands; both success and refusal response paths are visible. The controller refusal reply is conditional on controller invocation. Read guards state no writes; command success requires commit. Call heads are closed/filled and reply heads are dashed/open.
