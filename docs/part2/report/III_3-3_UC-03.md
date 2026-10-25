## 3.3 Design for Use Case 3: Maintain hubs and kitchen capacity (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

### 3.3.1 Design Classes in Detailed Design

<!-- include: ../UC-03/design_classes.md -->

### 3.3.2 Design Class Diagram

Each sheet is generated from the shared model. Method-rich layer views and operation projections are split at 230 mm landscape width; sequences use 170 mm portrait width; all parts must be retained. The full typed class table resolves members omitted in narrow operation projections. A downward dashed arrow is a dependency; a solid domain association has multiplicities and navigability. Domain classes own no application dependency.

#### i. Domain design class

![UC-03 domain 1](../../../models/UC-03/dcd_uc03_domain_PartA.png)

Figure 3.3.2iA. UC-03 domain projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 domain 2](../../../models/UC-03/dcd_uc03_domain_PartB.png)

Figure 3.3.2iB. UC-03 domain projection 2 — Author: 722I0004 · AI-assisted (Codex)

#### ii. Controller

![UC-03 controller 1](../../../models/UC-03/dcd_uc03_controller_PartA.png)

Figure 3.3.2iiA. UC-03 controller projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 controller 2](../../../models/UC-03/dcd_uc03_controller_PartB.png)

Figure 3.3.2iiB. UC-03 controller projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 controller 3](../../../models/UC-03/dcd_uc03_controller_PartC.png)

Figure 3.3.2iiC. UC-03 controller projection 3 — Author: 722I0004 · AI-assisted (Codex)

#### iii. UI (view)

![UC-03 view 1](../../../models/UC-03/dcd_uc03_view_PartA.png)

Figure 3.3.2iiiA. UC-03 view projection 1 — Author: 722I0004 · AI-assisted (Codex)

#### iv. Data access

![UC-03 dao 1](../../../models/UC-03/dcd_uc03_dao_PartA.png)

Figure 3.3.2ivA. UC-03 dao projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 dao 2](../../../models/UC-03/dcd_uc03_dao_PartB.png)

Figure 3.3.2ivB. UC-03 dao projection 2 — Author: 722I0004 · AI-assisted (Codex)

#### v. Design class (all layers together)

![UC-03 all 1](../../../models/UC-03/dcd_uc03_all_PartA.png)

Figure 3.3.2vA. UC-03 all projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 2](../../../models/UC-03/dcd_uc03_all_PartB.png)

Figure 3.3.2vB. UC-03 all projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 3](../../../models/UC-03/dcd_uc03_all_PartC.png)

Figure 3.3.2vC. UC-03 all projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 4](../../../models/UC-03/dcd_uc03_all_PartD.png)

Figure 3.3.2vD. UC-03 all projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 5](../../../models/UC-03/dcd_uc03_all_PartE.png)

Figure 3.3.2vE. UC-03 all projection 5 — Author: 722I0004 · AI-assisted (Codex)

### 3.3.3 OOD with CRC Cards or Communication Diagram

<!-- include: ../UC-03/crc.md -->

### 3.3.4 OOD with Sequence Diagram

Place the following sequence figures at **170 mm portrait width** (23 px minimum source text = 9.236 pt at placement). DCD sheets use **230 mm landscape width** (18 px = 9.780 pt).

Each exact SSD boundary request maps to a real blueprint route adapter and controller method. The active server session supplies uid(); camelCase names map to validated Python arguments/form keys in .1. The domain objects are dataclasses: a create arrow denotes implicit construction and a note denotes state inspection; no invented domain archive/update method is called. Return labels name outcomes, not callable methods. Persistence is a note referring to 4.3.2; Section III contains no DAO lifeline or SQL. Every guard is checked again at the mutation boundary. Technical-failure operands require rollback before acknowledging a no-change outcome.

![UC-03 sequence 1](../../../models/UC-03/seq_uc03_listHubs.png)

Figure 3.3.4A. UC-03 sequence projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 2](../../../models/UC-03/seq_uc03_getHub.png)

Figure 3.3.4B. UC-03 sequence projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 3](../../../models/UC-03/seq_uc03_createHub.png)

Figure 3.3.4C. UC-03 sequence projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 4](../../../models/UC-03/seq_uc03_updateHub.png)

Figure 3.3.4D. UC-03 sequence projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 5](../../../models/UC-03/seq_uc03_archiveHub.png)

Figure 3.3.4E. UC-03 sequence projection 5 — Author: 722I0004 · AI-assisted (Codex)

### 3.3.5 Final Design Class Diagram

Changes from 3.3.2: none in selected signatures. The final figures repeat the reconciled operation projections explicitly; the union includes every view/controller call shown in .4, including `_require_admin`. Domain create/note messages are construction/attribute facts, not additional callable operations. Full attributes and support authorization/DTO collaborators remain in the layer views and .1. Every final part continues the same UC projection set.

![UC-03 final 1](../../../models/UC-03/dcd_uc03_final_PartA.png)

Figure 3.3.5A. UC-03 final projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 2](../../../models/UC-03/dcd_uc03_final_PartB.png)

Figure 3.3.5B. UC-03 final projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 3](../../../models/UC-03/dcd_uc03_final_PartC.png)

Figure 3.3.5C. UC-03 final projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 4](../../../models/UC-03/dcd_uc03_final_PartD.png)

Figure 3.3.5D. UC-03 final projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 5](../../../models/UC-03/dcd_uc03_final_PartE.png)

Figure 3.3.5E. UC-03 final projection 5 — Author: 722I0004 · AI-assisted (Codex)

† design target, not yet in code at C0 (see the operation-specific P4 input in the figure and `operation_realisation.csv`). Shared busy/commit/rowcount requirements are P2-S13/P3-S03 targets; no runtime correctness is asserted. Native draw.io editing and final DOCX/PDF placement remain UNTESTED.

Integration maintenance (Author: 722I0004 · AI-assisted (Codex)): native draw.io text now has explicit actual font sizes and bold styles matching the SVG/PNG labels: 18 px minimum at 230 mm for DCDs and 23 px minimum at 170 mm for sequences. Native editing remains UNTESTED. Reviewed behavioral targets remain daggered; mere symbol/signature correspondence does not clear them.
