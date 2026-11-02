# Executive Summary (0.25 point)

Author: 722I0004 · AI-assisted (Codex, Claude)

**The system.** SaigonBite runs delivery-only kitchens (hubs) in Ho Chi Minh City under several online brands. Orders used to arrive by phone, Zalo and third-party apps and were copied onto paper, so no one could see a hub's load, dishes ran out after orders were taken, and cash and refunds were tracked by hand. The SaigonBite platform replaces this with one shared order record used by five actors: customers (local residents and tourists), kitchen staff, shippers, the admin and the manager.

**What we analysed, designed and built.** Following an iterative Unified Process in six iterations, the team modelled six main use cases, two per student: UC-01 Place an order, UC-02 Deliver an order, UC-03 Maintain hubs and kitchen capacity, UC-04 Produce management reports, UC-05 Decide an incoming order (confirm, reject or offer a replacement) and UC-06 Maintain brands, menu items and hub listings. Nine supporting use cases complete login, profiles, tracking, cancellation, preparation, availability, vouchers, accounts and order archive, so every persistent class has a running create, read, update and archive path.

- **Business requirements (I):** vision, stakeholders, Gantt chart with planned and actual dates, ranked backlog, eleven risks with status, Assumption Log of 19 entries, business process and swim-lane diagrams, 40 functional and 12 non-functional requirements, each traced to its tests.
- **Analysis (II):** 32 events, a domain model of 13 persistent classes with generalisation, composition and an association class, a fully developed description, activity diagram, SSD and state machines for each use case, and CRUD verification for all five actors.
- **Design (III):** three-layer design classes (view, controller, domain, data access), CRC cards, sequence diagrams for the system operations of each main use case and a final design class diagram per use case whose signatures are read from the code.
- **Implementation (IV):** Python/Flask with hand-written SQL on SQLite (13 tables), a UI designed from sketch to Figma prototype and traced from the SSDs, and one integrated system.
- **Testing and deployment (V):** test cases derived from all 30 postconditions and minimum guarantees, and a public HTTPS deployment on Google Cloud.

**Results.** 928 automated tests pass (27/10/2026, commit 252ada1). Seven browser scenarios follow one order through all roles and pass 60 of 60 steps, and 22 of 22 steps pass on the deployed site https://saigonbite.io.vn. All 52 requirements are verified except NFR-09 (phone width), which is partly verified. Two weeks of schedule reserve remain before the 15/11 target.

Codes used throughout the report (BR-xx, FR-xx, PC/MG, OP-xx, A-xx, Q1–Q5, L1–L6, D-xx) are explained in the Glossary in the Appendix.

**Limitations and recommendations.** Online payment is a simulator, a refund owed is recorded but not paid out, distance is estimated to a district centre, and complaint handling and rating are deferred. Business figures such as the 25 % quiet threshold and the 8 km radius are team defaults because the client has not answered Q1–Q5. Section "Conclusions" lists what we recommend next. AI tools were used for code, diagrams and text and are declared in Appendix 5; whether that use is accepted (course clarification L6) is still to be confirmed by the lecturer.
