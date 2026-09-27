# Meridian Global Retail Group — Business Scenario and Decision Playbook

**Document Type:** Internal Reference — Applied Investigation Scenarios
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is **fictional internal scenario documentation** created for this AI/ML portfolio project. It is not an official document of the original Global Superstore dataset provider. Scenarios describe **how** to investigate a situation using Meridian's data and documentation — they do not assert that any specific result described hypothetically has actually occurred, except where explicitly noted as an observed pattern in the transaction dataset.

---

## How to Use This Playbook

Each scenario below follows the same structure: Business Question → Required Data → SQL Analysis → Relevant Business Documents → Possible Evidence → Possible Interpretations → Unknown Factors → Recommended Next Investigation → Example Report Structure. Apply the seven-step methodology in `root_cause_analysis_playbook.md` within each scenario.

---

## Scenario 1 — Sales Decline Investigation

**Business Question:** "Why did Sales decline in [Region/Category] during [period]?"

**Required Data:** Sales by period, Region, Category, Sub-Category, Segment; Quantity and Discount for the same cuts.

**SQL Analysis:** Aggregate Sales by month for the affected dimension and comparison period(s); decompose by Region → Category → Sub-Category → Product to isolate the largest contributor(s).

**Relevant Business Documents:** `root_cause_analysis_playbook.md` (methodology), `business_kpi_definitions.md` (Sales/Revenue Growth definitions), `pricing_discount_policy.md` (if discount-related).

**Possible Evidence:** A specific Sub-Category or Region accounts for most of the decline; Quantity fell alongside Sales (demand-side) or Quantity held while price/Discount changed (price-side).

**Possible Interpretations:** Seasonal effect (compare to prior year same period); demand softening in a specific Sub-Category; a pricing or discount change reducing effective revenue per unit.

**Unknown Factors:** Competitor activity, marketing campaign timing, macroeconomic conditions, inventory availability — none are recorded in the dataset.

**Recommended Next Investigation:** If Quantity also fell, investigate demand-side factors within available dimensions (Region, Segment); if Quantity held but Sales fell, investigate Discount and pricing changes.

**Example Final Report Structure:** Event validation → baseline comparison (MoM and YoY) → decomposition table by Region/Category → FACT/INFERENCE/UNKNOWN classification → stated limitations → recommended follow-up.

---

## Scenario 2 — Profit Decline Investigation

**Business Question:** "Why did Profit decline even though Sales were stable/growing?"

**Required Data:** Sales, Profit, aggregate Profit Margin (`SUM(Profit)/SUM(Sales)`), Discount, Shipping Cost — all by the same period/dimension cuts.

**SQL Analysis:** Compute aggregate Margin trend; decompose the Profit change into a Discount-driven component and a Shipping-Cost-driven component by comparing average Discount and average Shipping Cost across the two periods.

**Relevant Business Documents:** `business_kpi_definitions.md` (correct margin formula), `pricing_discount_policy.md`, `shipping_fulfillment_policy.md`.

**Possible Evidence:** Rising average Discount in the affected segment; rising Shipping Cost as a % of Sales; a mix shift toward lower-margin Sub-Categories (e.g., more Furniture, less Technology).

**Possible Interpretations:** "Profitless growth" driven by discounting; margin compression from a Category/Sub-Category mix shift; fulfillment cost creep.

**Unknown Factors:** Whether any discount increase was a deliberate strategic decision or unplanned drift; actual vendor cost changes not in this dataset.

**Recommended Next Investigation:** Isolate whether the Margin decline is Discount-driven, Shipping-Cost-driven, or mix-driven using the decomposition in Step 4 of the root-cause playbook; escalate per `pricing_discount_policy.md` if Discount-driven and material.

**Example Final Report Structure:** As Scenario 1, with explicit Margin decomposition table (Discount effect / Shipping effect / mix effect).

---

## Scenario 3 — High-Sales, Low-Profitability Region

**Business Question:** "Which Region has high Sales but poor profitability, and what business factors could explain it?"

**Required Data:** Sales, Profit, aggregate Margin, Discount, Category mix, Shipping Cost — by Region.

**SQL Analysis:** Rank Regions by Sales; separately rank by aggregate Margin; identify Regions that are high on the first ranking and low on the second (this pattern is already observable in Meridian's data — e.g., Southeast Asia and EMEA show relatively higher Sales alongside notably lower aggregate Margin than several smaller Regions).

**Relevant Business Documents:** `pricing_discount_policy.md` (regional discount considerations), `product_category_management.md` (Category mix effects), `shipping_fulfillment_policy.md` (geographic cost considerations).

**Possible Evidence:** Elevated average Discount in the Region; a Category mix skewed toward lower-margin Sub-Categories (e.g., Furniture); higher Shipping Cost as a % of Sales due to geography.

**Possible Interpretations:** The Region's profitability gap is a composition effect (Category/Discount mix) rather than an execution problem; alternatively, it may reflect genuinely higher cost-to-serve geography.

**Unknown Factors:** Local competitive intensity, regional pricing strategy rationale, local logistics infrastructure constraints.

**Recommended Next Investigation:** Decompose the Region's Margin gap into Discount effect vs. Category-mix effect vs. Shipping-Cost effect before concluding the Region is "underperforming" in an execution sense.

**Example Final Report Structure:** Region ranking table (Sales vs. Margin) → decomposition of margin gap → FACT/INFERENCE/UNKNOWN → limitations.

---

## Scenario 4 — High-Discount Investigation

**Business Question:** "Could discounting be contributing to declining margins?"

**Required Data:** Discount distribution (by tier per `pricing_discount_policy.md`), Sales and Profit by Discount tier, trended over time.

**SQL Analysis:** Bucket transactions into Discount tiers (0%, 0–10%, 10–20%, 20–30%, 30–50%, 50%+); compute aggregate Margin per tier and trend the share of Sales occurring in each tier over time.

**Relevant Business Documents:** `pricing_discount_policy.md` (Section 5 documents the tier-margin relationship directly), `business_kpi_definitions.md`.

**Possible Evidence:** In Meridian's actual transaction history, margin declines steadily as Discount tier rises, turning negative above roughly 20–30% Discount and deeply negative above 50% — this is a documented FACT in the dataset, not a hypothesis. The open question in any specific investigation is whether the **mix of transactions shifted toward these higher tiers** during the period under review.

**Possible Interpretations:** If the share of Sales in high-discount tiers increased in the affected period, discounting is a well-supported (INFERENCE-level, evidence-backed) contributor to margin decline; if the tier mix was stable, the margin decline likely stems from another source (Shipping Cost, Category mix).

**Unknown Factors:** Whether high-discount transactions were pre-approved clearance activity (acceptable) or uncontrolled discounting (a governance failure) — not distinguishable from the transaction data alone.

**Recommended Next Investigation:** Trend the high-discount-tier Sales share over the exact period in question and compare to the Margin trend in the same period.

**Example Final Report Structure:** Discount-tier margin table (company-wide, from `pricing_discount_policy.md`) → tier-mix trend for the specific period → correlation statement (FACT: co-movement; INFERENCE: contribution) → limitations.

---

## Scenario 5 — Shipping-Cost Increase

**Business Question:** "Why did Shipping Cost increase in [Region/period]?"

**Required Data:** Shipping Cost, Ship Mode mix, Order Priority mix, Sales, order count — by Region/period.

**SQL Analysis:** Compute Shipping Cost as a % of Sales (not absolute) trended over time; decompose by Ship Mode share and Order Priority share.

**Relevant Business Documents:** `shipping_fulfillment_policy.md` (Sections 5, 8 — cost drivers and the "lower cost ≠ better efficiency" principle applies in reverse here too: higher cost ≠ automatically inefficient).

**Possible Evidence:** A shift toward faster Ship Modes (Same Day/First Class) as a share of orders; a rise in Critical/High Order Priority share; larger average order size (Shipping Cost correlates with Sales).

**Possible Interpretations:** Deliberate service-level improvement (faster shipping to meet rising Critical-priority commitments); alternatively, genuine cost inefficiency (same Ship Mode mix, but rising per-shipment cost).

**Unknown Factors:** Actual carrier rate changes, fuel cost, geographic expansion into higher-cost-to-serve areas — not directly recorded.

**Recommended Next Investigation:** Separate the volume/mix effect (more orders, bigger orders, faster Ship Mode share) from a true cost-per-shipment effect (same mix, higher cost) before concluding inefficiency.

**Example Final Report Structure:** Shipping Cost % of Sales trend → Ship Mode/Priority mix trend → classified conclusion → limitations.

---

## Scenario 6 — Category Underperformance

**Business Question:** "Why is the Furniture Category underperforming relative to Technology and Office Supplies?"

**Required Data:** Sales, Profit, aggregate Margin, Discount, Sub-Category breakdown for Furniture vs. other Categories.

**SQL Analysis:** Compare aggregate Margin across the three Categories; drill into Furniture's Sub-Categories (Tables, Bookcases, Chairs, Furnishings) to isolate the primary contributor.

**Relevant Business Documents:** `product_category_management.md` (Section 3 documents Furniture's Category-level margin weakness and Tables' negative aggregate margin directly).

**Possible Evidence:** Tables shows a negative aggregate Profit Margin and the highest average Discount of any Sub-Category — a documented FACT in Meridian's data.

**Possible Interpretations:** Furniture's weaker performance is substantially attributable to the Tables Sub-Category specifically, not a uniform weakness across all Furniture Sub-Categories.

**Unknown Factors:** Whether Tables' discounting is planned clearance (acceptable, time-bound) or a chronic pricing problem (requires correction) — see `product_category_management.md`, Section 8.

**Recommended Next Investigation:** Trend Tables' Discount and Margin over time to determine whether the negative margin is a persistent structural issue or improving/worsening.

**Example Final Report Structure:** Category comparison table → Sub-Category drill-down → FACT/INFERENCE/UNKNOWN → limitations.

---

## Scenario 7 — Product Concentration Risk

**Business Question:** "Is Meridian overly dependent on a small number of products?"

**Required Data:** Sales and Profit by Product, ranked; total company Sales/Profit.

**SQL Analysis:** Compute the top 10/20/50 products' share of total company Sales and Profit; compare against the total catalog size (Meridian carries over 10,000 distinct products).

**Relevant Business Documents:** `business_kpi_definitions.md` (Product Contribution), `product_category_management.md`.

**Possible Evidence:** Given the very large product catalog, any individual product's share of total company Sales is typically small; concentration risk at the product level is generally low unless a specific product is shown to represent an outsized share.

**Possible Interpretations:** Meridian's revenue base is broadly diversified across products; risk, if any, is more likely to concentrate at the Sub-Category or Category level than the individual product level.

**Unknown Factors:** Supplier-side concentration (whether many top products share a single vendor) is not recorded in this dataset.

**Recommended Next Investigation:** If product-level concentration is low, redirect concentration analysis to Sub-Category or vendor level (outside current dataset scope).

**Example Final Report Structure:** Top-N product share table → comparison to total catalog size → conclusion on concentration risk level → limitations.

---

## Scenario 8 — Customer Concentration Risk

**Business Question:** "Is Meridian overly dependent on a small number of customers?"

**Required Data:** Sales by Customer ID, ranked; total company Sales; customer count.

**SQL Analysis:** Compute the top 10/20/50 customers' share of total company Sales against a customer base of roughly 4,800 distinct customers.

**Relevant Business Documents:** `customer_segmentation_strategy.md` (Section 5 documents this directly: even the top 20 customers represent only a low single-digit share of total Sales).

**Possible Evidence:** Company-wide customer concentration is low, a documented FACT in Meridian's data.

**Possible Interpretations:** Company-level performance swings are unlikely to be explained by any single customer; concentration should instead be assessed within narrower cuts (a specific Region or Category) where it may be materially higher.

**Unknown Factors:** Contractual dependency (e.g., multi-year agreements) with any specific large account is not recorded.

**Recommended Next Investigation:** Re-run the concentration calculation within specific Regions/Markets/Categories rather than company-wide, per `customer_segmentation_strategy.md`, Section 5.

**Example Final Report Structure:** Company-wide concentration statement → narrower-cut concentration check → conclusion → limitations.

---

## Scenario 9 — Regional Performance Anomaly

**Business Question:** "Why did [Region] perform very differently from other Regions in the same Market during [period]?"

**Required Data:** Sales, Profit, Margin, Discount, Category mix, Shipping Cost for the anomalous Region vs. peer Regions in the same Market.

**SQL Analysis:** Compare the anomalous Region against Market-average performance across all core metrics for the same period; check whether the anomaly is new or has existed historically (compare against the Region's own prior-period baseline).

**Relevant Business Documents:** `root_cause_analysis_playbook.md` (full methodology), `company_business_overview.md` (Market/Region hierarchy), `product_category_management.md` (Category mix effects).

**Possible Evidence:** A structural difference (e.g., North Asia and Central Asia show notably higher aggregate Margin than Southeast Asia within the same APAC Market, coinciding with much lower average Discount) or a period-specific deviation.

**Possible Interpretations:** Structural (persistent, driven by Category mix or discount discipline differences) vs. episodic (a one-period anomaly likely tied to a specific event not captured in the dataset).

**Unknown Factors:** Local market conditions, in-country competitive dynamics, currency effects (not separately modeled in this dataset).

**Recommended Next Investigation:** Determine persistence by checking whether the anomaly holds across multiple periods (structural) or appears in only one period (episodic, requiring the "state limitations" step).

**Example Final Report Structure:** Region-vs-peer comparison table → historical persistence check → classified conclusion → limitations.

---

## Scenario 10 — Margin Deterioration (Company-Wide)

**Business Question:** "Why is Meridian's overall Profit Margin trending downward?"

**Required Data:** Company-wide aggregate Margin trend by year/quarter; Discount tier mix trend; Category mix trend; Shipping Cost as % of Sales trend.

**SQL Analysis:** Trend `SUM(Profit)/SUM(Sales)` by year and quarter; overlay Discount-tier mix, Category mix (Sales share by Category), and Shipping Cost % of Sales on the same timeline to identify which moved together with the Margin trend.

**Relevant Business Documents:** All KPI, pricing, shipping, and category documents; `root_cause_analysis_playbook.md` for the full decomposition method.

**Possible Evidence:** A rising share of Sales occurring in higher Discount tiers; a growing Sales share for lower-margin Categories (e.g., Furniture) relative to Technology; rising Shipping Cost as a % of Sales.

**Possible Interpretations:** Margin deterioration is most plausibly explained by whichever of the three candidate drivers shows the clearest co-movement with the Margin trend — this must be tested with actual period-by-period decomposition, not assumed.

**Unknown Factors:** Vendor cost inflation, currency effects, and competitive pricing pressure are not recorded in this dataset.

**Recommended Next Investigation:** Run the three candidate-driver trends (Discount-tier mix, Category mix, Shipping Cost %) side-by-side against the Margin trend and identify the strongest co-movement as the primary INFERENCE-level explanation, explicitly noting it is not proof of causation (`business_analysis_governance.md`, Section 8).

**Example Final Report Structure:** Company-wide Margin trend chart/table → three-driver overlay table → ranked INFERENCE statements → stated limitations → recommended follow-up analysis.

---

### Document Scope

**This document can establish:** how an AI agent should structure the investigation of ten realistic categories of business questions using Meridian's actual data dimensions and documented policies, and which documents and SQL analyses are relevant to each.

**This document cannot establish:** the actual answer to any of these scenarios for a specific real period — each scenario must be executed against the transaction data at query time, following the referenced methodology in `root_cause_analysis_playbook.md`.
