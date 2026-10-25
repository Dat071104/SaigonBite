## 4.2 Package Diagram for the Subsystem

Author: 722I0004 · AI-assisted (Codex)

![Package architecture and C0 import audit](../../../models/shared/package_diagram.png)

Figure 4.2. Package architecture and C0 dependency policy — Author: 722I0004 · AI-assisted (Codex)

The diagram shows the permitted package dependencies: presentation routes depend on controllers; controllers depend on domain objects and data access; the domain package has no outward application-layer dependency. Dashed arrows show only those permitted dependencies. The import audit beside the packages reports actual C0 violations separately, without drawing them as allowed architecture.

The comparison resolves both absolute and relative `saigonbite.*` imports in all 48 inventory modules. It accounts for 392 application-internal import records: 152 permitted cross-layer imports (24 presentation→controllers, 82 controllers→domain, 46 controllers→data_access), 182 imports within a layer, 43 strict-layer violations, and 15 root-boundary imports. Imports from Flask, Flask-Login, Werkzeug, SQLite and the Python standard library are outside the application-layer comparison.

| Strict C0 violation | Evidence from `code_inventory.json` |
|---|---|
| presentation→business.domain: 12 imports in 7 modules | `presentation/account.py` imports `Role` and `rules`; `admin.py` imports `DiscountType` and `Role`; `auth.py` imports `Role` and `UserAccount`; `delivery.py`, `kitchen.py` and `reports.py` import `Role`; `order.py` imports `OnlineOption`, `PaymentMethod` and `Role`. |
| presentation→data_access: 3 imports in 2 modules | `presentation/db.py` imports `connect`; `presentation/order.py` imports `APPROVE` and `DECLINE`. |
| data_access→business.domain: 28 imports in 10 modules | `customer_dao.py`, `delivery_dao.py`, `hub_dao.py`, `menu_dao.py`, `offer_dao.py`, `order_dao.py`, `payment_dao.py`, `payment_gateway.py`, `user_dao.py` and `voucher_dao.py` import domain objects, factories, enums or rules for row materialisation and gateway typing. |

The remaining 15 records sit at the composition boundary: `saigonbite/__init__.py` imports 3 controller error types and 10 presentation modules to assemble the application; `app.py` imports `create_app`; and `presentation/auth.py` imports the root-level `saigonbite.NAV` constant. The first two are bootstrap wiring outside the four named packages. The last is a direct view-to-root import and is called out separately because it does not match the strict package graph.

**Root disposition — accepted as P3-S04 / P4.9.** A strict-layer boundary decision is required before treating the package graph as satisfied at C0. Resolve the 12 presentation→domain imports and 3 presentation→data_access imports at the presentation/controller boundary, decide whether DAO-to-domain materialisation receives an explicit persistence-mapper exception or moves behind a lower-level mapping boundary, and resolve the `NAV` root import. No exception or architectural change is adopted in P3. The shared annotations account for all 44 finding records across 23 module pairs (43 cross-layer records plus the `NAV` root import). These are static policy findings; they do not establish a runtime failure. The figure shows three permitted arrows across four packages and keeps observed violations visible.

Evidence is Static at C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. The machine-readable import audit is in `models/shared/package_diagram.json`. No application import, execution, test, or runtime qualification was performed.
