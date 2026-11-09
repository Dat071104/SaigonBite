## 3.3 Design for Use Case 3: Maintain hubs and kitchen capacity (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

The design was recorded as a target at C0 (`45ac762`); P4 resolution records 4 UC-03 entries, with their scoped evidence and limitations in the P4 status appendix. The † symbol in a diagram refers to the historical C0 target, not a current implementation verdict.

### 3.3.1 Design Classes in Detailed Design

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-03_design_classes.md -->

### 3.3.2 Design Class Diagram

Each sheet is generated from the shared model. The full typed class table resolves members omitted in narrow operation projections. A downward dashed arrow is a dependency; a solid domain association has multiplicities and navigability. Each displayed association has two separate multiplicity labels next to its attached endpoints and a separate role name. Generalization has no multiplicities. Domain classes own no application dependency.

#### i. Domain design class

![UC-03 domain 1](../../../models/UC-03/dcd_uc03_domain_PartA.png)

Figure 3.3.2iA. UC-03 domain projection 1 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 domain 2](../../../models/UC-03/dcd_uc03_domain_PartB.png)

Figure 3.3.2iB. UC-03 domain projection 2 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

#### ii. Controller

![UC-03 controller 1](../../../models/UC-03/dcd_uc03_controller_PartA.png)

Figure 3.3.2iiA. UC-03 controller projection 1 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 controller 2](../../../models/UC-03/dcd_uc03_controller_PartB.png)

Figure 3.3.2iiB. UC-03 controller projection 2 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 controller 3](../../../models/UC-03/dcd_uc03_controller_PartC.png)

Figure 3.3.2iiC. UC-03 controller projection 3 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

#### iii. UI (view)

![UC-03 view 1](../../../models/UC-03/dcd_uc03_view_PartA.png)

Figure 3.3.2iiiA. UC-03 view projection 1 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

#### iv. Data access

![UC-03 dao 1](../../../models/UC-03/dcd_uc03_dao_PartA.png)

Figure 3.3.2ivA. UC-03 dao projection 1 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 dao 2](../../../models/UC-03/dcd_uc03_dao_PartB.png)

Figure 3.3.2ivB. UC-03 dao projection 2 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

#### v. Design class (all layers together)

![UC-03 all 1](../../../models/UC-03/dcd_uc03_all_PartA.png)

Figure 3.3.2vA. UC-03 all projection 1 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 all 2](../../../models/UC-03/dcd_uc03_all_PartB.png)

Figure 3.3.2vB. UC-03 all projection 2 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 all 3](../../../models/UC-03/dcd_uc03_all_PartC.png)

Figure 3.3.2vC. UC-03 all projection 3 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 all 4](../../../models/UC-03/dcd_uc03_all_PartD.png)

Figure 3.3.2vD. UC-03 all projection 4 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 all 5](../../../models/UC-03/dcd_uc03_all_PartE.png)

Figure 3.3.2vE. UC-03 all projection 5 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### 3.3.3 OOD with CRC Cards or Communication Diagram

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-03_crc.md -->

### 3.3.4 OOD with Sequence Diagram



Each exact SSD boundary request maps to a real blueprint route adapter and controller method. The active server session supplies uid(); camelCase names map to validated Python arguments/form keys in 3.3.1. The domain objects are dataclasses: a create arrow denotes implicit construction and a note denotes state inspection; no invented domain archive/update method is called. Return labels name outcomes, not callable methods. Persistence is a note referring to 4.3.2; Section III contains no DAO lifeline or SQL. Every guard is checked again at the mutation boundary. Technical-failure operands require rollback before acknowledging a no-change outcome. The actual alt frame separates refusal, successful completion and technical failure with operand dividers. Solid filled heads denote synchronous calls; dashed open heads denote returns.

![UC-03 sequence 1](../../../models/UC-03/seq_uc03_listHubs.png)

Figure 3.3.4A. UC-03 sequence projection 1 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 sequence 2](../../../models/UC-03/seq_uc03_getHub.png)

Figure 3.3.4B. UC-03 sequence projection 2 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 sequence 3](../../../models/UC-03/seq_uc03_createHub.png)

Figure 3.3.4C. UC-03 sequence projection 3 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 sequence 4](../../../models/UC-03/seq_uc03_updateHub.png)

Figure 3.3.4D. UC-03 sequence projection 4 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

![UC-03 sequence 5](../../../models/UC-03/seq_uc03_archiveHub.png)

Figure 3.3.4E. UC-03 sequence projection 5 — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### 3.3.5 Final Design Class Diagram
Author: 722I0004 · AI-assisted (Claude)

The final design class diagram refines the layer views of 3.3.2 with what the sequence diagrams in 3.3.4 and the implementation settled. Figure 3.3.5A is an overview of all classes; the detail sheets after it give the members of one controller at a time.

- **Overview first, then detail sheets.** Figure 3.3.5A shows every class of the four layers by name, with the calls, the «persists» and «loads» links and the domain associations, drawn as plain lines; their multiplicities and navigability are in the domain views of 3.3.2 and the domain model (2.1.7), because the labels pile up at the small name boxes. The detail sheets leave the associations out. The members are too many to print readably on the same page, so the detail sheets take one controller at a time and show the view functions that call it and the DAOs and domain classes it uses, with member signatures. Each figure is laid out for its page so that the estimated smallest text is 9 pt or more.
- **Only the members this use case calls.** The sequence diagrams fixed which operations each class must offer; the complete member lists stay in the 3.3.1 tables and 3.3.2 views.
- **Signatures read from the code.** Parameter names and types are read from the source by `models/shared/final_dcd.py` when the figures are generated, and each member is matched with the operation rows of the design model. This is a cross-check at generation time, not a guarantee: the figures must be regenerated after a code change.
- **Navigability and persistence.** Layers run top to bottom (view, controller, data access, domain) and the dashed arrows run the same way: view to controller, controller to the DAOs and domain classes it uses, and DAO to the entity it maps. «persists» marks a DAO that writes the entity's table in this use case (an INSERT, UPDATE or DELETE in a method the use case calls); «loads» marks one that only reads it. The arrow points from the DAO to the entity, so the domain layer does not depend on data access. Domain associations keep their multiplicities from the domain model (2.1.7).

![UC-03 final design class diagram, overview (class names only)](../../../models/UC-03/dcd_uc03_final_overview.png)

Figure 3.3.5A. UC-03 final design class diagram, overview (class names only) — Author: 722I0004 · AI-assisted (Claude).

![UC-03 final design class diagram, detail sheet A (HubController)](../../../models/UC-03/dcd_uc03_final_detail_A.png)

Figure 3.3.5B. UC-03 final design class diagram, detail sheet A (HubController) — Author: 722I0004 · AI-assisted (Claude).

Behaviour refined between the first design and the final design (each refinement is covered by the tests in 5.1). Every state-changing operation runs in one `BEGIN IMMEDIATE` transaction and checks the row count of each guarded UPDATE, so a stale page, a guessed ID or a competing user changes nothing.

| System operation | Refinement in the final design |
|---|---|
| `listHubs` | The admin list can include archived hubs, so history stays reachable. |
| `createHub, updateHub, archiveHub` | Hub writes use guarded, row-count-checked transactions; archive is refused while the hub has open orders. |

Editable sources: `models/UC-03/dcd_uc03_final_overview.dot` and `models/UC-03/dcd_uc03_final_detail_A.dot` (Graphviz, generated by `models/shared/final_dcd.py`), with SVG exports beside them.
