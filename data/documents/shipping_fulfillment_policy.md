# Meridian Global Retail Group — Shipping and Fulfillment Operations Policy

**Document Type:** Internal Policy — Logistics & Fulfillment Operations
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is **fictional internal operational documentation** created for this AI/ML portfolio project. It is not an official document of the original Global Superstore dataset provider. Operational thresholds, KPIs, and escalation rules are demo content, designed to be realistic and internally consistent with the uploaded transaction data.

---

## 1. Purpose

This policy governs how Meridian fulfills customer orders across its global logistics network, defines the relationship between Ship Mode, Order Priority, and Shipping Cost, and gives AI analysts a framework for interpreting shipping-related transaction data correctly.

## 2. Ship Modes

Meridian offers four Ship Modes, used consistently across every Market:

| Ship Mode | Description | Typical Use Case |
|---|---|---|
| **Same Day** | Fastest fulfillment; highest cost per shipment | Critical-priority orders, urgent replacements |
| **First Class** | Expedited multi-day delivery | High-priority orders, premium accounts |
| **Second Class** | Standard-expedited delivery | Medium-priority orders |
| **Standard Class** | Most economical, longest transit time | Default for Low/Medium-priority orders; majority of order volume |

In Meridian's transaction history, **Standard Class** accounts for the clear majority of order lines and Sales volume, followed by Second Class, First Class, and then Same Day, which is the smallest but most expensive-per-unit Ship Mode.

## 3. Order Priority

Every order carries an **Order Priority** value — `Critical`, `High`, `Medium`, or `Low` — reflecting the customer service commitment associated with that order (driven by account tier, contractual SLA, or customer request), which is a **separate concept from Ship Mode**:

- Order Priority = the commitment made to the customer.
- Ship Mode = the carrier service actually used to try to meet that commitment.

A `Critical` priority order is not required to always use `Same Day` shipping — fulfillment operations selects the Ship Mode expected to satisfy the priority commitment given origin, destination, and carrier availability. This means the same Order Priority can appear across multiple Ship Modes in the data, and vice versa. Meridian's data confirms this: average Shipping Cost rises with Order Priority (`Critical` orders carry substantially higher average Shipping Cost than `Medium` or `Low` orders), but the two fields are not a strict one-to-one mapping.

## 4. Fulfillment Process (Order Date to Ship Date)

1. Order is placed and recorded with an `Order Date`.
2. Fulfillment operations assigns/validates Order Priority based on account and product context.
3. A Ship Mode is selected to meet the priority commitment at the lowest reasonable Shipping Cost.
4. The order is picked, packed, and handed to carrier; `Ship Date` is recorded.
5. The gap between `Order Date` and `Ship Date` is Meridian's internal **fulfillment lead time**, monitored as an operational KPI (Section 8).

## 5. Shipping Cost Drivers

Shipping Cost per line item is driven by a combination of factors observable (directly or by proxy) in the transaction dataset:

- **Ship Mode** — the single largest driver; Same Day and First Class carry substantially higher average Shipping Cost than Second Class and Standard Class.
- **Order Priority** — Critical and High priority orders carry materially higher average Shipping Cost than Medium/Low, consistent with faster, more expensive fulfillment paths.
- **Geography** — cross-border and long-haul shipments (e.g., into smaller or more remote Markets) tend to carry higher per-unit Shipping Cost than domestic, high-density Markets.
- **Product characteristics (by proxy of Category/Sub-Category)** — bulkier, heavier Categories such as Furniture typically carry higher Shipping Cost per unit than compact Office Supplies items.
- **Order size** — Shipping Cost and Sales are positively correlated in Meridian's data (larger orders tend to cost more to ship in absolute terms), which analysts must account for before comparing raw Shipping Cost across orders of very different size.

## 6. Geographic Considerations

Because Meridian ships to 147 countries, fulfillment operations maintains differentiated logistics strategies:

- **High-density Markets** (e.g., US, EU) benefit from established carrier networks and lower marginal Shipping Cost per shipment.
- **Lower-density or remote Regions** (e.g., Oceania, Central Asia, Caribbean, Africa) typically carry higher per-shipment logistics cost due to longer transit distances and thinner carrier infrastructure.
- Regional fulfillment managers are expected to periodically reassess Ship Mode availability and cost in lower-density Regions rather than assuming a uniform global cost structure.

## 7. Ship Mode Selection Logic

Fulfillment operations selects Ship Mode using this decision hierarchy:

1. Does the Order Priority contractually require expedited handling? → prefer Same Day / First Class.
2. Is the destination Region served efficiently by an expedited carrier? → confirm feasibility before commit.
3. If no urgency is indicated (`Medium`/`Low` priority), default to **Standard Class** to protect Shipping Cost efficiency.
4. Route optimization and carrier consolidation are applied wherever multiple orders share destination and timing.

## 8. Relationship Between Shipping Cost, Order Volume, and Profitability

Three relationships are important for correct interpretation of shipping data:

1. **Shipping Cost scales with order volume/size**, so total Shipping Cost naturally rises during high-volume periods (e.g., seasonal peaks). A rise in total Shipping Cost is not automatically a red flag — it must be evaluated relative to Sales volume in the same period.
2. **Shipping Cost is a direct deduction from Profit.** Holding Sales and Discount constant, higher Shipping Cost mechanically reduces Profit and compresses Profit Margin. This makes Shipping Cost one of the first variables to check when investigating unexplained margin compression.
3. **Ship Mode mix shifts affect average Shipping Cost independently of volume.** If a Region shifts toward faster Ship Modes (e.g., more First Class / Same Day as a share of orders) without a change in customer commitments, average Shipping Cost per order will rise even if total order volume is flat — an efficiency issue, not a demand issue.

### Why lower shipping cost does not automatically mean better operational efficiency

A period or Region with **lower total or average Shipping Cost** could reflect any of the following, each with very different operational implications:

- **Genuine efficiency improvement** — better carrier rates, smarter consolidation, optimized routing. *(Desirable)*
- **A shift toward slower Ship Modes** (e.g., more Standard Class, less Same Day) — which may reduce cost but also mean Meridian is **failing to meet Order Priority commitments**, risking customer satisfaction. *(Undesirable, hidden risk)*
- **A shift in order mix toward smaller, lighter, or lower-value orders** — lower Shipping Cost simply reflects smaller shipments, not better logistics execution. *(Neutral — a composition effect, not an efficiency effect)*
- **A shift in geographic mix toward lower-cost-to-serve Regions** — again a composition effect rather than a true efficiency gain.

**Policy conclusion:** Analysts must never interpret "Shipping Cost went down" as inherently positive without decomposing whether the change is driven by (a) genuine cost efficiency, (b) a Ship Mode/service-level shift, or (c) an order-mix/geography shift. This decomposition step is mandatory before any efficiency claim is made — see `root_cause_analysis_playbook.md`, Step 4 (Decompose the Change).

## 9. Delivery Expectations

While the dataset does not record actual delivery confirmation, the `Order Date`-to-`Ship Date` gap is used as a proxy for fulfillment responsiveness. Internal service expectations (targets, not guarantees) are:

| Order Priority | Internal Fulfillment Target |
|---|---|
| Critical | Same-day to next-day ship |
| High | 1–2 day ship |
| Medium | 2–4 day ship |
| Low | Up to 5–7 day ship (batched with Standard Class) |

## 10. Operational KPIs

- Average Shipping Cost, overall and by Ship Mode / Order Priority / Region / Market
- Ship Mode mix (% share of orders by Ship Mode), trended over time
- Order Priority fulfilled-as-expected rate (Ship Mode consistent with priority target)
- Shipping Cost as a % of Sales, by Region and Category
- Average `Order Date`-to-`Ship Date` gap, by Order Priority

## 11. Escalation Rules

Escalate to Regional Logistics Manager / VP of Fulfillment when:

- Average Shipping Cost as a % of Sales rises materially in a Region without a corresponding shift toward faster Ship Modes (suggesting a genuine cost problem rather than a deliberate service upgrade).
- Ship Mode mix shifts toward slower classes for `Critical`/`High` priority orders (a service-level failure risk).
- A Region's Shipping Cost profile diverges sharply from comparable Regions in the same Market without an identified geographic or carrier cause.

## 12. Shipping Anomalies to Investigate

- A Category/Sub-Category with unusually high Shipping Cost relative to its Sales value (potential packaging, weight, or routing inefficiency — Furniture Sub-Categories such as Tables and Bookcases are natural candidates given product bulk).
- Orders where Shipping Cost is disproportionately large relative to Sales (a "shipping cost outlier" that can turn an otherwise-profitable line item into a loss).
- Sudden Ship Mode mix changes in a single Region that are not mirrored elsewhere.

## 13. Interpretation Guidelines for Analysts

1. Always normalize Shipping Cost by Sales or by order count before comparing across time periods or geographies.
2. Separate "cost went down because of efficiency" from "cost went down because volume/mix changed" — see Section 8.
3. Cross-reference Shipping Cost findings with Order Priority mix before concluding a service-level problem.
4. Treat any Shipping-Cost-driven margin conclusion as an **inference** unless corroborated by an explicit Ship Mode or Order Priority mix shift in the same period.

---

### Document Scope

**This document can establish:** Meridian's fictional shipping/fulfillment operating model, the defined relationship between Ship Mode, Order Priority, and Shipping Cost, and the correct analytical framework for interpreting Shipping Cost changes.

**This document cannot establish:** actual carrier contracts, real-world logistics costs, delivery confirmation or customer satisfaction outcomes (not present in the dataset), or the specific operational cause of any single shipping cost anomaly without further transaction-level investigation.
