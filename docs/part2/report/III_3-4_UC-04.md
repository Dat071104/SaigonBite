# 3.4 Design for Use Case 4: Produce management reports: sales, workload, delivery performance (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

Baseline: 45ac76221b0a103174c7c01d17577e6e49cfd665. All application observations below are Static from the frozen AST inventory and shared model. Target behavior marked † is not a test or runtime result.

## 3.4.1 Design Classes in Detailed Design

One typed table per participating class/module follows.

<!-- include: ../UC-04/design_classes.md -->

## 3.4.2 Design Class Diagram

### i. Domain design class

HubStatus and Hub are the real domain participants. Period, report rows and report results belong to the actual controller module; no Report domain class or lifecycle is invented.

![UC-04 domain design classes: No Report domain class or lifecycle exists; report values stay in the controller module.](../../../models/UC-04/dcd_uc04_domain.png)

Figure 3.4.2.i-A. UC-04 domain design classes: No Report domain class or lifecycle exists; report values stay in the controller module. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_domain.drawio) · [SVG](../../../models/UC-04/dcd_uc04_domain.svg) · [Generator](../../../models/UC-04/dcd_uc04_domain.py) · [Data](../../../models/UC-04/dcd_uc04_domain.json)

### ii. Controller

ReportController validates manager access and filters, then builds ephemeral report value objects. DeliveryRow exposes the real wait/ride/failure calculations; zero denominators display n/a.

![UC-04 controller/value roles: Sales value roles continue in Part B; other report operations continue in Parts C–F.](../../../models/UC-04/dcd_uc04_controller_PartA.png)

Figure 3.4.2.ii-A. UC-04 controller/value roles: Sales value roles continue in Part B; other report operations continue in Parts C–F. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartA.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartA.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartA.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartA.json)

![UC-04 controller/value roles: Part A contains authorization/filter helpers; F-03/F-09 remain † targets.](../../../models/UC-04/dcd_uc04_controller_PartB.png)

Figure 3.4.2.ii-B. UC-04 controller/value roles: Part A contains authorization/filter helpers; F-03/F-09 remain † targets. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartB.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartB.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartB.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartB.json)

![UC-04 controller/value roles: Workload value roles continue in Part D.](../../../models/UC-04/dcd_uc04_controller_PartC.png)

Figure 3.4.2.ii-C. UC-04 controller/value roles: Workload value roles continue in Part D. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartC.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartC.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartC.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartC.json)

![UC-04 controller/value roles: Part C contains authorization; workload targets retain archived hubs (P2-S18).](../../../models/UC-04/dcd_uc04_controller_PartD.png)

Figure 3.4.2.ii-D. UC-04 controller/value roles: Part C contains authorization; workload targets retain archived hubs (P2-S18). — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartD.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartD.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartD.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartD.json)

![UC-04 controller/value roles: Delivery metric value roles continue in Part F.](../../../models/UC-04/dcd_uc04_controller_PartE.png)

Figure 3.4.2.ii-E. UC-04 controller/value roles: Delivery metric value roles continue in Part F. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartE.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartE.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartE.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartE.json)

![UC-04 controller/value roles: Part E contains authorization and interval helpers; rows and sample counts are non-persisted.](../../../models/UC-04/dcd_uc04_controller_PartF.png)

Figure 3.4.2.ii-F. UC-04 controller/value roles: Part E contains authorization and interval helpers; rows and sample counts are non-persisted. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartF.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartF.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartF.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartF.json)

### iii. UI (view)

saigonbite.presentation.reports is the «view» blueprint module. It maps the SSD filters to actual route/controller arguments; it is not a fabricated view class.

![UC-04 view module](../../../models/UC-04/dcd_uc04_view.png)

Figure 3.4.2.iii. UC-04 view module — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_view.drawio) · [SVG](../../../models/UC-04/dcd_uc04_view.svg) · [Generator](../../../models/UC-04/dcd_uc04_view.py) · [Data](../../../models/UC-04/dcd_uc04_view.json)

### iv. Data access

Reports issue read-only selections. Workload’s target retains archived hub identities with zero open work (P2-S18). The F-09/P4.8 target groups by menu_item_id and carries identity through ReportDAO.top_items, SalesReport.top_items and reports.sales. SalesReport.top_items is list[tuple[int, str, int, int]]: item ID, snapshot name, quantity and revenue; equal snapshot names do not merge distinct items.

![UC-04 data-access classes](../../../models/UC-04/dcd_uc04_dao.png)

Figure 3.4.2.iv. UC-04 data-access classes — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_dao.drawio) · [SVG](../../../models/UC-04/dcd_uc04_dao.svg) · [Generator](../../../models/UC-04/dcd_uc04_dao.py) · [Data](../../../models/UC-04/dcd_uc04_dao.json)

### v. Design class (all layers together)

Parts A-I show operation paths and controller value roles across all four layers, with mutual continuation notes. The integrated DCD keeps receiver names/return types compact; exact signatures remain in the class tables and filtered layer diagrams.

![UC-04 all layers: Sales operation and data grain](../../../models/UC-04/dcd_uc04_all_PartA.png)

Figure 3.4.2.v-A. UC-04 all layers: Sales operation and data grain — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartA.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartA.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartA.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartA.json)

![UC-04 all layers: Manager guard and VN filter helpers](../../../models/UC-04/dcd_uc04_all_PartB.png)

Figure 3.4.2.v-B. UC-04 all layers: Manager guard and VN filter helpers — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartB.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartB.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartB.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartB.json)

![UC-04 all layers: Sales row and filter value objects](../../../models/UC-04/dcd_uc04_all_PartC.png)

Figure 3.4.2.v-C. UC-04 all layers: Sales row and filter value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartC.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartC.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartC.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartC.json)

![UC-04 all layers: Sales report result object](../../../models/UC-04/dcd_uc04_all_PartD.png)

Figure 3.4.2.v-D. UC-04 all layers: Sales report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartD.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartD.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartD.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartD.json)

![UC-04 all layers: Current workload and archived hubs](../../../models/UC-04/dcd_uc04_all_PartE.png)

Figure 3.4.2.v-E. UC-04 all layers: Current workload and archived hubs — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartE.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartE.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartE.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartE.json)

![UC-04 all layers: Workload snapshot value objects](../../../models/UC-04/dcd_uc04_all_PartF.png)

Figure 3.4.2.v-F. UC-04 all layers: Workload snapshot value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartF.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartF.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartF.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartF.json)

![UC-04 all layers: Delivery interval and metric source](../../../models/UC-04/dcd_uc04_all_PartG.png)

Figure 3.4.2.v-G. UC-04 all layers: Delivery interval and metric source — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartG.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartG.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartG.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartG.json)

![UC-04 all layers: Delivery metric and report value objects](../../../models/UC-04/dcd_uc04_all_PartH.png)

Figure 3.4.2.v-H. UC-04 all layers: Delivery metric and report value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartH.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartH.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartH.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartH.json)

![UC-04 all layers: Delivery report result object](../../../models/UC-04/dcd_uc04_all_PartI.png)

Figure 3.4.2.v-I. UC-04 all layers: Delivery report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartI.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartI.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartI.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartI.json)

## 3.4.3 OOD with CRC Cards or Communication Diagram

The CRC include lists actual collaborators from the AST-derived call/type model and distinguishes controller values from domain entities.

<!-- include: ../UC-04/crc.md -->

## 3.4.4 OOD with Sequence Diagram

Each request independently rechecks active Manager access. Calls use the real view/controller/value roles; DAO/SQL is omitted and noted for 4.3.2. Sales keeps refunds owed separate from T and marks the F-09 item-identity target. Every outcome preserves UC04-MG01; the denial operand carries UC04-MG02.

### salesReport — startDateVN, endDateVN, hubId?

OP-26 salesReport(startDateVN, endDateVN, hubId?) — models/UC-04/ssd_uc04.drawio#M01

![UC-04 design sequence: salesReport](../../../models/UC-04/seq_uc04_salesReport.png)

Figure 3.4.4.1. UC-04 design sequence: salesReport — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/seq_uc04_salesReport.drawio) · [SVG](../../../models/UC-04/seq_uc04_salesReport.svg) · [Generator](../../../models/UC-04/seq_uc04_salesReport.py) · [Data](../../../models/UC-04/seq_uc04_salesReport.json)

### workloadReport — no parameters

OP-27 workloadReport() — models/UC-04/ssd_uc04.drawio#M02

![UC-04 design sequence: workloadReport](../../../models/UC-04/seq_uc04_workloadReport.png)

Figure 3.4.4.2. UC-04 design sequence: workloadReport — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/seq_uc04_workloadReport.drawio) · [SVG](../../../models/UC-04/seq_uc04_workloadReport.svg) · [Generator](../../../models/UC-04/seq_uc04_workloadReport.py) · [Data](../../../models/UC-04/seq_uc04_workloadReport.json)

### deliveryReport — startDateVN, endDateVN, hubId?

OP-28 deliveryReport(startDateVN, endDateVN, hubId?) — models/UC-04/ssd_uc04.drawio#M03

![UC-04 design sequence: deliveryReport](../../../models/UC-04/seq_uc04_deliveryReport.png)

Figure 3.4.4.3. UC-04 design sequence: deliveryReport — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/seq_uc04_deliveryReport.drawio) · [SVG](../../../models/UC-04/seq_uc04_deliveryReport.svg) · [Generator](../../../models/UC-04/seq_uc04_deliveryReport.py) · [Data](../../../models/UC-04/seq_uc04_deliveryReport.json)

## 3.4.5 Final Design Class Diagram

All sequence receiver methods are present. Changes from 3.4.2: no local class/method/association change; final all-layer views repeat the sequence-reconciled design. The accepted shared F-09 annotation marks the DAO grouping, identity-bearing result and reports.sales presentation as P4-TARGET.

![UC-04 final design classes: Sales operation and data grain](../../../models/UC-04/dcd_uc04_final_PartA.png)

Figure 3.4.5-A. UC-04 final design classes: Sales operation and data grain — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartA.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartA.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartA.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartA.json)

![UC-04 final design classes: Manager guard and VN filter helpers](../../../models/UC-04/dcd_uc04_final_PartB.png)

Figure 3.4.5-B. UC-04 final design classes: Manager guard and VN filter helpers — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartB.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartB.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartB.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartB.json)

![UC-04 final design classes: Sales row and filter value objects](../../../models/UC-04/dcd_uc04_final_PartC.png)

Figure 3.4.5-C. UC-04 final design classes: Sales row and filter value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartC.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartC.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartC.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartC.json)

![UC-04 final design classes: Sales report result object](../../../models/UC-04/dcd_uc04_final_PartD.png)

Figure 3.4.5-D. UC-04 final design classes: Sales report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartD.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartD.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartD.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartD.json)

![UC-04 final design classes: Current workload and archived hubs](../../../models/UC-04/dcd_uc04_final_PartE.png)

Figure 3.4.5-E. UC-04 final design classes: Current workload and archived hubs — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartE.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartE.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartE.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartE.json)

![UC-04 final design classes: Workload snapshot value objects](../../../models/UC-04/dcd_uc04_final_PartF.png)

Figure 3.4.5-F. UC-04 final design classes: Workload snapshot value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartF.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartF.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartF.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartF.json)

![UC-04 final design classes: Delivery interval and metric source](../../../models/UC-04/dcd_uc04_final_PartG.png)

Figure 3.4.5-G. UC-04 final design classes: Delivery interval and metric source — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartG.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartG.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartG.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartG.json)

![UC-04 final design classes: Delivery metric and report value objects](../../../models/UC-04/dcd_uc04_final_PartH.png)

Figure 3.4.5-H. UC-04 final design classes: Delivery metric and report value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartH.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartH.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartH.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartH.json)

![UC-04 final design classes: Delivery report result object](../../../models/UC-04/dcd_uc04_final_PartI.png)

Figure 3.4.5-I. UC-04 final design classes: Delivery report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartI.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartI.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartI.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartI.json)

No Report state is drawn. Filters, report rows and returned reports are non-persisted controller values. The final DCD keeps † on F-03/F-09/P2-S18 targets; UC04-PC01 remains a required oracle correspondence, not a measured result.

## Integration repair evidence

Author: 722I0004 · AI-assisted (Codex)

The diagrams and typed metadata were refreshed against the corrected root-owned shared model. Allowed layered dependencies are drawn; actual upward DAO-to-domain imports are retained only as the static P4.9 architecture finding in report 4.2, not as permitted arrows. Shared transaction targets P2-S13/P3-S03 remain target behavior for guarded writes, commit failures and busy handling. Read paths remain read-only. Native draw.io XML and connected edge endpoints are structurally checked; native-app editing and final report placement remain UNTESTED.
