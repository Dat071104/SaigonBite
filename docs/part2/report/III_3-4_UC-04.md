# 3.4 Design for Use Case 4: Produce management reports: sales, workload, delivery performance (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

The design was recorded as a target at C0 (`45ac762`); P4 resolution records 5 UC-04 entries, with their scoped evidence and limitations in the P4 status appendix. The † symbol in a diagram refers to the historical C0 target, not a current implementation verdict.

## 3.4.1 Design Classes in Detailed Design

One typed table per participating class/module follows.

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-04_design_classes.md -->

## 3.4.2 Design Class Diagram

### i. Domain design class

HubStatus and Hub are the real domain participants. Period, report rows and report results belong to the actual controller module; no Report domain class or lifecycle is invented.

![UC-04 domain design classes: No Report domain class or lifecycle exists; report values stay in the controller module.](../../../models/UC-04/dcd_uc04_domain.png)

Figure 3.4.2.i-A. UC-04 domain design classes: No Report domain class or lifecycle exists; report values stay in the controller module. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### ii. Controller

ReportController validates manager access and filters, then builds ephemeral report value objects. DeliveryRow exposes the real wait/ride/failure calculations; zero denominators display n/a.

![UC-04 controller/value roles: Sales value roles continue in Part B; other report operations continue in Parts C–F.](../../../models/UC-04/dcd_uc04_controller_PartA.png)

Figure 3.4.2.ii-A. UC-04 controller/value roles: Sales value roles continue in Part B; other report operations continue in Parts C–F. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 controller/value roles: Part A contains authorization/filter helpers; F-03/F-09 design targets at C0.](../../../models/UC-04/dcd_uc04_controller_PartB.png)

Figure 3.4.2.ii-B. UC-04 controller/value roles: Part A contains authorization/filter helpers; F-03/F-09 are historical C0 targets. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 controller/value roles: Workload value roles continue in Part D.](../../../models/UC-04/dcd_uc04_controller_PartC.png)

Figure 3.4.2.ii-C. UC-04 controller/value roles: Workload value roles continue in Part D. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 controller/value roles: Part C contains authorization; workload targets retain archived hubs (P2-S18).](../../../models/UC-04/dcd_uc04_controller_PartD.png)

Figure 3.4.2.ii-D. UC-04 controller/value roles: Part C contains authorization; workload targets retain archived hubs (P2-S18). — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 controller/value roles: Delivery metric value roles continue in Part F.](../../../models/UC-04/dcd_uc04_controller_PartE.png)

Figure 3.4.2.ii-E. UC-04 controller/value roles: Delivery metric value roles continue in Part F. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 controller/value roles: Part E contains authorization and interval helpers; rows and sample counts are non-persisted.](../../../models/UC-04/dcd_uc04_controller_PartF.png)

Figure 3.4.2.ii-F. UC-04 controller/value roles: Part E contains authorization and interval helpers; rows and sample counts are non-persisted. — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### iii. UI (view)

saigonbite.presentation.reports is the «view» blueprint module. It maps the SSD filters to actual route/controller arguments; it is not a fabricated view class.

![UC-04 view module](../../../models/UC-04/dcd_uc04_view.png)

Figure 3.4.2.iii. UC-04 view module — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### iv. Data access

Reports issue read-only selections. Workload’s target retains archived hub identities with zero open work (P2-S18). The F-09/P4.8 target groups by menu_item_id and carries identity through ReportDAO.top_items, SalesReport.top_items and reports.sales. SalesReport.top_items is list[tuple[int, str, int, int]]: item ID, snapshot name, quantity and revenue; equal snapshot names do not merge distinct items.

![UC-04 data-access classes](../../../models/UC-04/dcd_uc04_dao.png)

Figure 3.4.2.iv. UC-04 data-access classes — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### v. Design class (all layers together)

Parts A-I show operation paths and controller value roles across all four layers, with mutual continuation notes. The integrated DCD keeps receiver names/return types compact; exact signatures remain in the class tables and filtered layer diagrams.

![UC-04 all layers: Sales operation and data grain](../../../models/UC-04/dcd_uc04_all_PartA.png)

Figure 3.4.2.v-A. UC-04 all layers: Sales operation and data grain — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Manager guard and VN filter helpers](../../../models/UC-04/dcd_uc04_all_PartB.png)

Figure 3.4.2.v-B. UC-04 all layers: Manager guard and VN filter helpers — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Sales row and filter value objects](../../../models/UC-04/dcd_uc04_all_PartC.png)

Figure 3.4.2.v-C. UC-04 all layers: Sales row and filter value objects — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Sales report result object](../../../models/UC-04/dcd_uc04_all_PartD.png)

Figure 3.4.2.v-D. UC-04 all layers: Sales report result object — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Current workload and archived hubs](../../../models/UC-04/dcd_uc04_all_PartE.png)

Figure 3.4.2.v-E. UC-04 all layers: Current workload and archived hubs — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Workload snapshot value objects](../../../models/UC-04/dcd_uc04_all_PartF.png)

Figure 3.4.2.v-F. UC-04 all layers: Workload snapshot value objects — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Delivery interval and metric source](../../../models/UC-04/dcd_uc04_all_PartG.png)

Figure 3.4.2.v-G. UC-04 all layers: Delivery interval and metric source — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Delivery metric and report value objects](../../../models/UC-04/dcd_uc04_all_PartH.png)

Figure 3.4.2.v-H. UC-04 all layers: Delivery metric and report value objects — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



![UC-04 all layers: Delivery report result object](../../../models/UC-04/dcd_uc04_all_PartI.png)

Figure 3.4.2.v-I. UC-04 all layers: Delivery report result object — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



## 3.4.3 OOD with CRC Cards or Communication Diagram

The CRC include lists actual collaborators from the AST-derived call/type model and distinguishes controller values from domain entities.

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-04_crc.md -->

## 3.4.4 OOD with Sequence Diagram

Each request independently rechecks active Manager access. Calls use the real view/controller/value roles; DAO/SQL is omitted and noted for 4.3.2. Sales keeps refunds owed separate from T and marks the F-09 item-identity target. Every outcome preserves UC04-MG01; the denial operand carries UC04-MG02.

### salesReport — startDateVN, endDateVN, hubId?

OP-26 salesReport(startDateVN, endDateVN, hubId?): models/UC-04/ssd_uc04.drawio#M01

![UC-04 design sequence: salesReport](../../../models/UC-04/seq_uc04_salesReport.png)

Figure 3.4.4.1. UC-04 design sequence: salesReport — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### workloadReport — no parameters

OP-27 workloadReport(): models/UC-04/ssd_uc04.drawio#M02

![UC-04 design sequence: workloadReport](../../../models/UC-04/seq_uc04_workloadReport.png)

Figure 3.4.4.2. UC-04 design sequence: workloadReport — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### deliveryReport — startDateVN, endDateVN, hubId?

OP-28 deliveryReport(startDateVN, endDateVN, hubId?): models/UC-04/ssd_uc04.drawio#M03

![UC-04 design sequence: deliveryReport](../../../models/UC-04/seq_uc04_deliveryReport.png)

Figure 3.4.4.3. UC-04 design sequence: deliveryReport — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



## 3.4.5 Final Design Class Diagram
Author: 722I0004 · AI-assisted (Claude)

The final design class diagram refines the layer views of 3.4.2 with what the sequence diagrams in 3.4.4 and the implementation settled. Figure 3.4.5A is an overview of all classes; the detail sheets after it give the members of one controller at a time.

- **Overview first, then detail sheets.** Figure 3.4.5A shows every class of the four layers by name, with the calls, the «persists» and «loads» links and the domain associations, drawn as plain lines; their multiplicities and navigability are in the domain views of 3.4.2 and the domain model (2.1.7), because the labels pile up at the small name boxes. The detail sheets leave the associations out. The members are too many to print readably on the same page, so the detail sheets take one controller at a time and show the view functions that call it and the DAOs and domain classes it uses, with member signatures. A controller that needs more than one sheet has them numbered (A1, A2 and so on); each caption says what the sheet shows. Each figure is laid out for its page so that the estimated smallest text is 9 pt or more.
- **Only the members this use case calls.** The sequence diagrams fixed which operations each class must offer; the complete member lists stay in the 3.4.1 tables and 3.4.2 views.
- **Signatures read from the code.** Parameter names and types are read from the source by `models/shared/final_dcd.py` when the figures are generated, and each member is matched with the operation rows of the design model. This is a cross-check at generation time, not a guarantee: the figures must be regenerated after a code change.
- **Navigability and persistence.** Layers run top to bottom (view, controller, data access, domain) and the dashed arrows run the same way: view to controller, controller to the DAOs and domain classes it uses, and DAO to the entity it maps. «persists» marks a DAO that writes the entity's table in this use case (an INSERT, UPDATE or DELETE in a method the use case calls); «loads» marks one that only reads it. The arrow points from the DAO to the entity, so the domain layer does not depend on data access. Domain associations keep their multiplicities from the domain model (2.1.7).

![UC-04 final design class diagram, overview (class names only)](../../../models/UC-04/dcd_uc04_final_overview.png)

Figure 3.4.5A. UC-04 final design class diagram, overview (class names only) — Author: 722I0004 · AI-assisted (Claude).

![UC-04 final design class diagram, detail sheet A1 (ReportController, view, controller and domain)](../../../models/UC-04/dcd_uc04_final_detail_A1.png)

Figure 3.4.5B. UC-04 final design class diagram, detail sheet A1 (ReportController, view, controller and domain) — Author: 722I0004 · AI-assisted (Claude).

![UC-04 final design class diagram, detail sheet A2 (ReportController, data access)](../../../models/UC-04/dcd_uc04_final_detail_A2.png)

Figure 3.4.5C. UC-04 final design class diagram, detail sheet A2 (ReportController, data access) — Author: 722I0004 · AI-assisted (Claude).

Behaviour refined between the first design and the final design (each refinement is covered by the tests in 5.1). Every state-changing operation runs in one `BEGIN IMMEDIATE` transaction and checks the row count of each guarded UPDATE, so a stale page, a guessed ID or a competing user changes nothing.

| System operation | Refinement in the final design |
|---|---|
| `salesReport` | Sales no longer subtract a refund twice, and top items are grouped by item ID instead of name. |
| `workloadReport` | Workload is a current snapshot: it ignores the date filter and keeps archived hubs that still have orders. |

Editable sources: `models/UC-04/dcd_uc04_final_overview.dot`, `models/UC-04/dcd_uc04_final_detail_A1.dot` and `models/UC-04/dcd_uc04_final_detail_A2.dot` (Graphviz, generated by `models/shared/final_dcd.py`), with SVG exports beside them.

## Integration repair evidence


The diagrams and typed metadata were refreshed against the corrected shared model. Allowed layered dependencies are drawn; the twelve retained dependency-policy entries are documented as static policy checks in report 4.2 and Table P4-1, not as runtime tests. P2-S13/P3-S03 identified C0 targets for guarded writes, commit failures and busy handling; their final scoped evidence is recorded in Table P4-1. Read paths remain read-only.

Diagram notation (R1–R4): the external SSD request now precedes two actual guarded operands. Each accepted path retains its named success response; refusal/controlled-failure responses are drawn inside the alternate operand, with an optional controller response only when the controller was invoked. Synchronous calls use visible closed filled heads; all replies use dashed open heads. Reports remain read-only, and empty/zero-denominator data remains an accepted result.
