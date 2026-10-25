## 4.1 Design Classes for the Subsystem

Author: 722I0004 · AI-assisted (Codex)

The subsystem design joins the six main use cases and their supporting account, tracking, kitchen, voucher, user-administration and archive responsibilities. It is a set of filtered views of [the shared design model](../../../models/shared/design_model.json), at committed application baseline `C0 = 45ac76221b0a103174c7c01d17577e6e49cfd665`. Its declarations describe static correspondence and explicitly marked design targets. They do not establish application execution or completion of P4.

The 68 continued parts cover all **104 canonical class/module roles**, all **365 declared methods** and **278 displayed attributes**. Every method and every displayed attribute has one full-detail occurrence. Reference boxes in relationship parts repeat only the canonical name and stereotype; they do not repeat full member lists. No framework, exception or module role in the shared model is silently excluded. Root-annotated domain foreign-key scalars are omitted in favor of the named associations; their physical mapping remains in section 4.3.1.

**How to read the parts.** Figures 4.1A–4.1AL hold the member declarations by layer, in the order view → controller → domain → data access. Figures 4.1AM–4.1AX show twelve labelled responsibility slices for all six main use cases and shared supporting controllers. Figures 4.1AY–4.1BK draw all 38 model associations/generalizations; Figures 4.1BL–4.1BP draw domain-to-enumeration dependencies. Each part names its preceding and following part, and the member index below resolves the full declaration of every reference box.

A public `+` or convention-private `-` precedes each member. Method parameters, defaults, return types and property/static/class-method tags come from the current shared-model declaration. Implicit `self`/`cls` receivers are suppressed on the drawing; full original signatures are retained in each adjacent JSON. `Any [inferred]` marks an absent annotation rather than a new claim about the value. Attributes inferred from assignments are also labelled `[inferred]`. The renderer introduces no getters, setters, route functions or view classes.

**Status.** `MATCH` means static correspondence at C0. A `P4-TARGET` or `GAP` member carries `†` and its explicit status; the legend names the corresponding F-/P2-S-/P3-S input IDs. A reference-box dagger summarizes non-MATCH declarations of that canonical role; its member part identifies each affected declaration. The renderer resolves types, signatures and daggers from the sole model every time. A reviewed change to `MATCH` removes its dagger automatically; a signature match alone does not establish contract behavior.

The actual Flask blueprints are the «view» modules `account`, `admin`, `auth`, `delivery`, `kitchen`, `main`, `order` and `reports`. Their real route functions carry HTTP method/rule notes (63 route records, including route aliases). Presentation helpers and `SessionUser` retain their real module/value roles. Jinja templates are presentation resources, not design classes: the `account/`, `admin/`, `delivery/`, `kitchen/`, `order/` and `reports/` template areas, plus `base.html`, `home.html`, `login.html`, `error.html` and `_form.html`, serve the real routes; the per-UC detailed class sections identify their selected template resources.

The structural parts preserve `Order` composition of `OrderLine`, the `LocalCustomer`/`TouristCustomer` generalizations to `Customer` without multiplicities, and `HubMenuItem` as the association class of Hub × MenuItem. Every ordinary association has its named role, navigation and both multiplicities. A multiplicity at the left belongs to the named source; the one at the right belongs to the named target. Enumeration boxes show the real literals. `HubStatus.busy` and `quiet` remain derived properties, `archived_at` remains nullable text, and active/availability remain boolean attributes. No additional lifecycle enum is introduced.

**Dependency projection.** The relationship set contains 84 unique selected dependencies and all 38 associations/generalizations from the sole model. Responsibility slices select direct blueprint→controller and controller→domain/data-access links that explain the named area; the enum parts select every allowed domain→enumeration dependency. Other call/type/helper dependencies are retained in the shared model and the per-UC design packages. This is an explicit readability projection, not a claim that every import or call is reproduced on every sheet. Only dependencies with `allowed_on_layered_diagram = true` are selected, with downward application-layer direction. Domain dependencies remain within the domain. Actual forbidden imports are assessed separately in section 4.2 as **P3-S04 / P4.9**; no mapper exception or runtime-failure inference is adopted here.

The supporting declaration coverage includes `AccountController` profile/address operations, `VoucherController` maintenance, `UserAdminController` active-account administration and both archive granularities. In particular, **`MenuController.list_catalogue(...)` is GAP † / P2-S14 / P4.6**: it composes catalogue, hubs and optional hub listings while retaining existing helpers. **`OrderArchiveController.archive_order(user_id, order_id)` is GAP † / P2-S06 / P4.7**: it supplies the per-ID closed-order archive contract alongside the separately named batch `archive(...)`. `UserAccount.created_at` remains GAP † / P2-S02 / P4.1. These are design inputs, not existing code claims.

All parts declare a 1200 × 850 canvas and **230 mm landscape placement**, with minimum 18 px text, equivalent to **9.780 pt** at that width. Scaling them below the declared width requires another legibility check. The editable draw.io, PNG, SVG, JSON and standalone generator share each figure stem. Native draw.io editing and final DOCX/PDF placement remain UNTESTED.

**Member index**

| Canonical role | Layer | Full member figure(s) |
|---|---|---|
| `account` | view | 4.1A |
| `admin` | view | 4.1A, 4.1B, 4.1C |
| `SessionUser` | view | 4.1C |
| `auth` | view | 4.1C |
| `presentation.db` | view | 4.1C |
| `delivery` | view | 4.1D |
| `presentation.helpers` | view | 4.1D |
| `kitchen` | view | 4.1D, 4.1E |
| `main` | view | 4.1E |
| `order` | view | 4.1E, 4.1F |
| `reports` | view | 4.1F |
| `presentation.security` | view | 4.1F |
| `Profile` | controller | 4.1G |
| `AccountController` | controller | 4.1G, 4.1H |
| `AuthController` | controller | 4.1H |
| `BaseController` | controller | 4.1H |
| `controllers.common` | controller | 4.1I |
| `DeliveryView` | controller | 4.1I |
| `ShipperBoard` | controller | 4.1I |
| `DeliveryController` | controller | 4.1J |
| `BusinessError` | controller | 4.1J |
| `ValidationError` | controller | 4.1J |
| `AuthorizationError` | controller | 4.1J |
| `NotFoundError` | controller | 4.1K |
| `ConflictError` | controller | 4.1K |
| `QuoteChangedError` | controller | 4.1K |
| `HubUnavailableError` | controller | 4.1K |
| `PaymentDeclinedError` | controller | 4.1K |
| `HubAdminView` | controller | 4.1K |
| `HubController` | controller | 4.1L |
| `BoardEntry` | controller | 4.1L |
| `KitchenBoard` | controller | 4.1L |
| `KitchenOrderView` | controller | 4.1L |
| `KitchenController` | controller | 4.1M |
| `Catalogue` | controller | 4.1M |
| `HubMenu` | controller | 4.1N |
| `MenuController` | controller | 4.1N, 4.1O |
| `ArchivePreview` | controller | 4.1O |
| `OrderArchiveController` | controller | 4.1O |
| `OrderDetail` | controller | 4.1P |
| `OrderSummary` | controller | 4.1P |
| `OrderTrackingController` | controller | 4.1P |
| `HubMenuView` | controller | 4.1Q |
| `OrderConfirmation` | controller | 4.1Q |
| `PaymentChoice` | controller | 4.1Q |
| `PlaceOrderController` | controller | 4.1Q, 4.1R |
| `Period` | controller | 4.1R |
| `SalesRow` | controller | 4.1S |
| `SalesReport` | controller | 4.1S |
| `WorkloadRow` | controller | 4.1S |
| `WorkloadReport` | controller | 4.1S |
| `DeliveryRow` | controller | 4.1T |
| `DeliveryReport` | controller | 4.1T |
| `ReportController` | controller | 4.1T |
| `controllers.report_controller` | controller | 4.1U |
| `UserAdminController` | controller | 4.1U, 4.1V |
| `VoucherController` | controller | 4.1V |
| `OrderState` | domain | 4.1W |
| `PaymentMethod` | domain | 4.1W |
| `OnlineOption` | domain | 4.1W |
| `PaymentState` | domain | 4.1W |
| `DeliveryState` | domain | 4.1X |
| `OfferState` | domain | 4.1X |
| `Role` | domain | 4.1X |
| `CustomerType` | domain | 4.1X |
| `DiscountType` | domain | 4.1X |
| `InvalidTransition` | domain | 4.1Y |
| `UserAccount` | domain | 4.1Y |
| `Customer` | domain | 4.1Y |
| `LocalCustomer` | domain | 4.1Y |
| `TouristCustomer` | domain | 4.1Y |
| `Address` | domain | 4.1Z |
| `Hub` | domain | 4.1Z |
| `HubStatus` | domain | 4.1AA |
| `Brand` | domain | 4.1AA |
| `MenuItem` | domain | 4.1AA |
| `HubMenuItem` | domain | 4.1AA |
| `Voucher` | domain | 4.1AB |
| `OrderLine` | domain | 4.1AB |
| `Quote` | domain | 4.1AC |
| `Payment` | domain | 4.1AC |
| `Order` | domain | 4.1AD |
| `Delivery` | domain | 4.1AE |
| `ReplacementOffer` | domain | 4.1AE |
| `domain.models` | domain | 4.1AE |
| `domain.rules` | domain | 4.1AF |
| `CustomerDAO` | data_access | 4.1AG |
| `data_access.customer_dao` | data_access | 4.1AG |
| `data_access.database` | data_access | 4.1AG |
| `DeliveryDAO` | data_access | 4.1AH |
| `data_access.delivery_dao` | data_access | 4.1AH |
| `HubDAO` | data_access | 4.1AH |
| `MenuDAO` | data_access | 4.1AI |
| `ReplacementOfferDAO` | data_access | 4.1AI |
| `data_access.offer_dao` | data_access | 4.1AJ |
| `OrderDAO` | data_access | 4.1AJ |
| `PaymentDAO` | data_access | 4.1AK |
| `Authorisation` | data_access | 4.1AK |
| `PaymentGatewaySimulator` | data_access | 4.1AK |
| `ReportDAO` | data_access | 4.1AK |
| `UserDAO` | data_access | 4.1AL |
| `data_access.user_dao` | data_access | 4.1AL |
| `VoucherDAO` | data_access | 4.1AL |
| `data_access.voucher_dao` | data_access | 4.1AL |

**Continued subsystem figures**

Presentation member declarations.

![4.1A View members](../../../models/shared/dcd_subsystem_PartA.png)

Figure 4.1A. Shared subsystem: View members — Author: 722I0004 · AI-assisted (Codex)

![4.1B View members](../../../models/shared/dcd_subsystem_PartB.png)

Figure 4.1B. Shared subsystem: View members — Author: 722I0004 · AI-assisted (Codex)

![4.1C View members](../../../models/shared/dcd_subsystem_PartC.png)

Figure 4.1C. Shared subsystem: View members — Author: 722I0004 · AI-assisted (Codex)

![4.1D View members](../../../models/shared/dcd_subsystem_PartD.png)

Figure 4.1D. Shared subsystem: View members — Author: 722I0004 · AI-assisted (Codex)

![4.1E View members](../../../models/shared/dcd_subsystem_PartE.png)

Figure 4.1E. Shared subsystem: View members — Author: 722I0004 · AI-assisted (Codex)

![4.1F View members](../../../models/shared/dcd_subsystem_PartF.png)

Figure 4.1F. Shared subsystem: View members — Author: 722I0004 · AI-assisted (Codex)

Controller, value and error member declarations.

![4.1G Controller members](../../../models/shared/dcd_subsystem_PartG.png)

Figure 4.1G. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1H Controller members](../../../models/shared/dcd_subsystem_PartH.png)

Figure 4.1H. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1I Controller members](../../../models/shared/dcd_subsystem_PartI.png)

Figure 4.1I. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1J Controller members](../../../models/shared/dcd_subsystem_PartJ.png)

Figure 4.1J. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1K Controller members](../../../models/shared/dcd_subsystem_PartK.png)

Figure 4.1K. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1L Controller members](../../../models/shared/dcd_subsystem_PartL.png)

Figure 4.1L. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1M Controller members](../../../models/shared/dcd_subsystem_PartM.png)

Figure 4.1M. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1N Controller members](../../../models/shared/dcd_subsystem_PartN.png)

Figure 4.1N. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1O Controller members](../../../models/shared/dcd_subsystem_PartO.png)

Figure 4.1O. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1P Controller members](../../../models/shared/dcd_subsystem_PartP.png)

Figure 4.1P. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1Q Controller members](../../../models/shared/dcd_subsystem_PartQ.png)

Figure 4.1Q. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1R Controller members](../../../models/shared/dcd_subsystem_PartR.png)

Figure 4.1R. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1S Controller members](../../../models/shared/dcd_subsystem_PartS.png)

Figure 4.1S. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1T Controller members](../../../models/shared/dcd_subsystem_PartT.png)

Figure 4.1T. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1U Controller members](../../../models/shared/dcd_subsystem_PartU.png)

Figure 4.1U. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

![4.1V Controller members](../../../models/shared/dcd_subsystem_PartV.png)

Figure 4.1V. Shared subsystem: Controller members — Author: 722I0004 · AI-assisted (Codex)

Domain, rule and enum member declarations.

![4.1W Domain members](../../../models/shared/dcd_subsystem_PartW.png)

Figure 4.1W. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1X Domain members](../../../models/shared/dcd_subsystem_PartX.png)

Figure 4.1X. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1Y Domain members](../../../models/shared/dcd_subsystem_PartY.png)

Figure 4.1Y. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1Z Domain members](../../../models/shared/dcd_subsystem_PartZ.png)

Figure 4.1Z. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1AA Domain members](../../../models/shared/dcd_subsystem_PartAA.png)

Figure 4.1AA. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1AB Domain members](../../../models/shared/dcd_subsystem_PartAB.png)

Figure 4.1AB. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1AC Domain members](../../../models/shared/dcd_subsystem_PartAC.png)

Figure 4.1AC. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1AD Domain members](../../../models/shared/dcd_subsystem_PartAD.png)

Figure 4.1AD. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1AE Domain members](../../../models/shared/dcd_subsystem_PartAE.png)

Figure 4.1AE. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

![4.1AF Domain members](../../../models/shared/dcd_subsystem_PartAF.png)

Figure 4.1AF. Shared subsystem: Domain members — Author: 722I0004 · AI-assisted (Codex)

DAO, mapping-helper and local gateway member declarations.

![4.1AG Data access members](../../../models/shared/dcd_subsystem_PartAG.png)

Figure 4.1AG. Shared subsystem: Data access members — Author: 722I0004 · AI-assisted (Codex)

![4.1AH Data access members](../../../models/shared/dcd_subsystem_PartAH.png)

Figure 4.1AH. Shared subsystem: Data access members — Author: 722I0004 · AI-assisted (Codex)

![4.1AI Data access members](../../../models/shared/dcd_subsystem_PartAI.png)

Figure 4.1AI. Shared subsystem: Data access members — Author: 722I0004 · AI-assisted (Codex)

![4.1AJ Data access members](../../../models/shared/dcd_subsystem_PartAJ.png)

Figure 4.1AJ. Shared subsystem: Data access members — Author: 722I0004 · AI-assisted (Codex)

![4.1AK Data access members](../../../models/shared/dcd_subsystem_PartAK.png)

Figure 4.1AK. Shared subsystem: Data access members — Author: 722I0004 · AI-assisted (Codex)

![4.1AL Data access members](../../../models/shared/dcd_subsystem_PartAL.png)

Figure 4.1AL. Shared subsystem: Data access members — Author: 722I0004 · AI-assisted (Codex)

Selected layered responsibility links for the six main UCs and shared supporting controllers.

![4.1AM UC-01 / ordering](../../../models/shared/dcd_subsystem_PartAM.png)

Figure 4.1AM. Shared subsystem: UC-01 / ordering — Author: 722I0004 · AI-assisted (Codex)

![4.1AN UC-02 / delivery](../../../models/shared/dcd_subsystem_PartAN.png)

Figure 4.1AN. Shared subsystem: UC-02 / delivery — Author: 722I0004 · AI-assisted (Codex)

![4.1AO UC-03 / hubs](../../../models/shared/dcd_subsystem_PartAO.png)

Figure 4.1AO. Shared subsystem: UC-03 / hubs — Author: 722I0004 · AI-assisted (Codex)

![4.1AP UC-04 / reports](../../../models/shared/dcd_subsystem_PartAP.png)

Figure 4.1AP. Shared subsystem: UC-04 / reports — Author: 722I0004 · AI-assisted (Codex)

![4.1AQ UC-05 / kitchen decisions](../../../models/shared/dcd_subsystem_PartAQ.png)

Figure 4.1AQ. Shared subsystem: UC-05 / kitchen decisions — Author: 722I0004 · AI-assisted (Codex)

![4.1AR UC-06 / catalogue](../../../models/shared/dcd_subsystem_PartAR.png)

Figure 4.1AR. Shared subsystem: UC-06 / catalogue — Author: 722I0004 · AI-assisted (Codex)

![4.1AS SUC-01 / authentication](../../../models/shared/dcd_subsystem_PartAS.png)

Figure 4.1AS. Shared subsystem: SUC-01 / authentication — Author: 722I0004 · AI-assisted (Codex)

![4.1AT SUC-02 / profile and addresses](../../../models/shared/dcd_subsystem_PartAT.png)

Figure 4.1AT. Shared subsystem: SUC-02 / profile and addresses — Author: 722I0004 · AI-assisted (Codex)

![4.1AU SUC-03 / SUC-04 / tracking](../../../models/shared/dcd_subsystem_PartAU.png)

Figure 4.1AU. Shared subsystem: SUC-03 / SUC-04 / tracking — Author: 722I0004 · AI-assisted (Codex)

![4.1AV SUC-07 / vouchers](../../../models/shared/dcd_subsystem_PartAV.png)

Figure 4.1AV. Shared subsystem: SUC-07 / vouchers — Author: 722I0004 · AI-assisted (Codex)

![4.1AW SUC-08 / accounts](../../../models/shared/dcd_subsystem_PartAW.png)

Figure 4.1AW. Shared subsystem: SUC-08 / accounts — Author: 722I0004 · AI-assisted (Codex)

![4.1AX SUC-09 / retained order history](../../../models/shared/dcd_subsystem_PartAX.png)

Figure 4.1AX. Shared subsystem: SUC-09 / retained order history — Author: 722I0004 · AI-assisted (Codex)

Canonical associations, generalizations and real-enum dependencies.

![4.1AY Associations and generalizations](../../../models/shared/dcd_subsystem_PartAY.png)

Figure 4.1AY. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1AZ Associations and generalizations](../../../models/shared/dcd_subsystem_PartAZ.png)

Figure 4.1AZ. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BA Associations and generalizations](../../../models/shared/dcd_subsystem_PartBA.png)

Figure 4.1BA. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BB Associations and generalizations](../../../models/shared/dcd_subsystem_PartBB.png)

Figure 4.1BB. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BC Associations and generalizations](../../../models/shared/dcd_subsystem_PartBC.png)

Figure 4.1BC. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BD Associations and generalizations](../../../models/shared/dcd_subsystem_PartBD.png)

Figure 4.1BD. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BE Associations and generalizations](../../../models/shared/dcd_subsystem_PartBE.png)

Figure 4.1BE. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BF Associations and generalizations](../../../models/shared/dcd_subsystem_PartBF.png)

Figure 4.1BF. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BG Associations and generalizations](../../../models/shared/dcd_subsystem_PartBG.png)

Figure 4.1BG. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BH Associations and generalizations](../../../models/shared/dcd_subsystem_PartBH.png)

Figure 4.1BH. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BI Associations and generalizations](../../../models/shared/dcd_subsystem_PartBI.png)

Figure 4.1BI. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BJ Associations and generalizations](../../../models/shared/dcd_subsystem_PartBJ.png)

Figure 4.1BJ. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BK Associations and generalizations](../../../models/shared/dcd_subsystem_PartBK.png)

Figure 4.1BK. Shared subsystem: Associations and generalizations — Author: 722I0004 · AI-assisted (Codex)

![4.1BL Domain enumeration dependencies](../../../models/shared/dcd_subsystem_PartBL.png)

Figure 4.1BL. Shared subsystem: Domain enumeration dependencies — Author: 722I0004 · AI-assisted (Codex)

![4.1BM Domain enumeration dependencies](../../../models/shared/dcd_subsystem_PartBM.png)

Figure 4.1BM. Shared subsystem: Domain enumeration dependencies — Author: 722I0004 · AI-assisted (Codex)

![4.1BN Domain enumeration dependencies](../../../models/shared/dcd_subsystem_PartBN.png)

Figure 4.1BN. Shared subsystem: Domain enumeration dependencies — Author: 722I0004 · AI-assisted (Codex)

![4.1BO Domain enumeration dependencies](../../../models/shared/dcd_subsystem_PartBO.png)

Figure 4.1BO. Shared subsystem: Domain enumeration dependencies — Author: 722I0004 · AI-assisted (Codex)

![4.1BP Domain enumeration dependencies](../../../models/shared/dcd_subsystem_PartBP.png)

Figure 4.1BP. Shared subsystem: Domain enumeration dependencies — Author: 722I0004 · AI-assisted (Codex)

The member and relation declarations above are generated from the same shared model used by the six report III design packages. Transactional message ordering and rollback behavior belong to the operation sequences in 3.x.4 and their DAO enrichments in 4.3.2; this class view does not infer those behaviors from a method signature.
