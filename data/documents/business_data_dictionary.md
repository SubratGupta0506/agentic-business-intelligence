# Meridian Global Retail Group — Business Glossary and Data Dictionary

**Document Type:** Internal Reference — Data Dictionary
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is **fictional internal data documentation** created for this AI/ML portfolio project. It is not an official document of the original Global Superstore dataset provider. Field names and structure reflect the actual uploaded CSV; no fields beyond what is present in the dataset have been invented.

---

## Purpose

This document defines every field present in Meridian's transaction dataset (`superstore_cleaned.csv`), its business meaning, data type, analytical use, and known pitfalls. It is the authoritative reference for how an AI analyst should interpret each column before writing SQL or drawing conclusions.

## Dataset Overview

- **Grain:** One row = one product line item within a customer order (i.e., Row ID grain, not Order ID grain).
- **Row count:** Approximately 51,290 transaction records.
- **Coverage:** Order dates spanning 2011–2014, across 147 countries, 7 Markets, 13 Regions, 3 Categories, 17 Sub-Categories, and 3 Customer Segments.

## Field-by-Field Reference

### Row ID

- **Business meaning:** A unique technical identifier for a single transaction line item.
- **Data type:** Integer.
- **Analytical meaning:** The correct grain for `COUNT()` when the question is "how many transaction lines" — e.g., line-item volume.
- **Common usage:** Joining, deduplication, and confirming that an aggregation is being performed at the correct grain.
- **Pitfall:** Do not use Row ID count as a proxy for "number of orders" — see Order ID below.

### Order ID

- **Business meaning:** Identifies the customer order (checkout event) that a line item belongs to.
- **Data type:** String/categorical (e.g., `CA-2014-100111`).
- **Analytical meaning:** The correct grain for Order-level metrics such as Average Order Value (`SUM(Sales)/COUNT(DISTINCT Order ID)`) and Order Volume.
- **Common usage:** Grouping line items that were purchased together in a single checkout.
- **Pitfall — IMPORTANT:** **Order ID is not unique per transaction row.** A single Order ID can and does appear across multiple Row IDs, because customers frequently purchase several different products (potentially spanning multiple Categories) in one order. Any query that assumes one row per Order ID will undercount true line-item volume and must instead use `COUNT(DISTINCT Order ID)` when counting orders and `COUNT(Row ID)` (or simple row count) when counting line items.

### Order Date

- **Business meaning:** The date the customer placed the order.
- **Data type:** Date (spans January 2011 through December 2014 in this dataset).
- **Analytical meaning:** The primary field for all time-series, seasonality, and period-over-period analysis (see `root_cause_analysis_playbook.md`).
- **Common usage:** Grouping by year/quarter/month for trend analysis.
- **Pitfall:** Do not confuse Order Date with Ship Date (below) — using the wrong date field will distort both revenue-recognition and fulfillment-lead-time analysis.

### Ship Date

- **Business meaning:** The date the order was shipped to the customer.
- **Data type:** Date (extends slightly beyond Order Date's range, into early the following period, since orders placed near period-end may ship shortly after).
- **Analytical meaning:** Used together with Order Date to compute fulfillment lead time (`shipping_fulfillment_policy.md`, Section 10).
- **Common usage:** Operational/logistics analysis, not revenue analysis.
- **Pitfall:** Never use Ship Date for revenue-period reporting — Sales should always be attributed to Order Date.

### Customer ID

- **Business meaning:** A unique identifier for a customer account.
- **Data type:** String/categorical.
- **Analytical meaning:** The correct grain for customer-level aggregation (Customer Value, concentration analysis — see `customer_segmentation_strategy.md`).
- **Common usage:** Grouping all orders belonging to the same customer across time.
- **Pitfall:** Prefer Customer ID over Customer Name for aggregation/joins, since names could theoretically collide across different customer accounts; Customer Name is best used for human-readable reporting only.

### Customer Name

- **Business meaning:** The display name of the customer.
- **Data type:** String.
- **Analytical meaning:** Human-readable label; not the preferred join/grouping key (use Customer ID).
- **Common usage:** Reporting and illustrative examples in business documentation and dashboards.
- **Pitfall:** Do not assume Customer Name uniquely identifies a customer in all edge cases; use Customer ID for authoritative grouping.

### Segment

- **Business meaning:** The customer type: `Consumer`, `Corporate`, or `Home Office` (see `customer_segmentation_strategy.md`).
- **Data type:** Categorical (3 values).
- **Analytical meaning:** Primary customer-strategy dimension.
- **Common usage:** Segment-level Sales/Profit/Discount analysis.
- **Pitfall:** Segment is a customer-level attribute recorded per order; do not assume a customer never changes segment across their history without checking (though in this dataset Segment is generally stable per Customer ID).

### Product ID

- **Business meaning:** A unique identifier for a specific product/SKU.
- **Data type:** String/categorical.
- **Analytical meaning:** The correct grain for product-level aggregation (over 10,000 distinct Product IDs in this dataset).
- **Common usage:** Product Contribution and concentration analysis (`business_kpi_definitions.md`).
- **Pitfall:** Prefer Product ID over Product Name for joins/grouping, for the same reason as Customer ID vs. Customer Name.

### Product Name

- **Business meaning:** The descriptive name of the product.
- **Data type:** String (often includes brand and variant detail, e.g., "Apple Smart Phone, Full Size").
- **Analytical meaning:** Human-readable label for product-level reporting.
- **Common usage:** Top/bottom product reporting in `product_category_management.md`.
- **Pitfall:** Product Name strings can be long and similar across variants (e.g., multiple "Smart Phone" entries from different brands) — always pair with Product ID when precision matters.

### Category

- **Business meaning:** The top-level product grouping: `Technology`, `Office Supplies`, or `Furniture`.
- **Data type:** Categorical (3 values).
- **Analytical meaning:** Primary product-portfolio dimension (see `product_category_management.md`).
- **Common usage:** Category-level Sales/Profit/Margin comparison.
- **Pitfall:** Category-level Margin comparisons can mask very different Sub-Category behavior within the same Category (e.g., Furniture contains both healthy and structurally unprofitable Sub-Categories) — always drill into Sub-Category before concluding.

### Sub-Category

- **Business meaning:** The detailed product grouping within a Category (17 total: Paper, Art, Storage, Appliances, Supplies, Envelopes, Fasteners, Labels, Binders, Accessories, Phones, Copiers, Machines, Tables, Bookcases, Chairs, Furnishings).
- **Data type:** Categorical (17 values).
- **Analytical meaning:** The primary level at which Meridian evaluates product profitability (see `product_category_management.md`).
- **Common usage:** Identifying specific profitability issues (e.g., Tables).
- **Pitfall:** Do not assume Sub-Category names are self-explanatory of margin profile — margin must always be computed, not assumed, from Sales and Profit.

### Country

- **Business meaning:** The country associated with the order (typically ship-to country).
- **Data type:** Categorical (147 distinct values in this dataset).
- **Analytical meaning:** The most granular standard geography for cross-border analysis.
- **Common usage:** Country-level Sales/Margin ranking (e.g., United States as the single largest country by Sales).
- **Pitfall:** With 147 countries, many will have very low transaction counts — apply the same small-sample caution as in `product_category_management.md`, Section 6, before drawing conclusions about any single low-volume country.

### State / City

- **Business meaning:** Sub-national and city-level geography associated with the order.
- **Data type:** Categorical (State: many distinct values; City: 3,600+ distinct values).
- **Analytical meaning:** The finest-grained standard geography available; useful for logistics and last-mile analysis.
- **Common usage:** Deep-dive geographic investigation, typically only after Region/Country-level analysis has narrowed the scope.
- **Pitfall:** City-level analysis will almost always suffer from very low transaction counts per city; avoid drawing company-level conclusions from city-level data alone.

### Market

- **Business meaning:** Meridian's top-level commercial geography grouping used in executive reporting: `US`, `EU`, `LATAM`, `Africa`, `APAC`, `EMEA`, `Canada`.
- **Data type:** Categorical (7 values).
- **Analytical meaning:** The primary geography for Market-level executive reporting (see `company_business_overview.md`, Section 3).
- **Common usage:** Market-level Sales/Margin comparison.
- **Pitfall:** `US` and `Canada` are separate Markets in this hierarchy but roll up together under `Market 2` = `North America` — do not conflate the two hierarchies when reporting.

### Market 2

- **Business meaning:** A consolidated regional grouping used in finance/supply-chain reporting: `North America`, `EU`, `LATAM`, `Africa`, `APAC`, `EMEA`.
- **Data type:** Categorical (6 values).
- **Analytical meaning:** Use when a finance-style consolidated geography is needed (e.g., combining US and Canada).
- **Common usage:** Cross-referencing Market-level figures against finance reporting conventions.
- **Pitfall:** Do not assume Market and Market 2 are interchangeable labels for the same 7-vs-6 category system — always check which hierarchy a question or report is using.

### Region

- **Business meaning:** A finer-grained operational geography than Market, used by sales/fulfillment operations (13 values: West, East, South, Central, North, Canada, EMEA, Africa, Oceania, Southeast Asia, North Asia, Central Asia, Caribbean).
- **Data type:** Categorical (13 values).
- **Analytical meaning:** The preferred level for operational and fulfillment analysis; more granular than Market but less granular than Country.
- **Common usage:** Regional Sales/Margin/Discount comparison (see all four policy documents).
- **Pitfall:** Region names can be easy to confuse across hierarchies (e.g., "Central" as a Region within North America is distinct from "Central Asia" as a Region within APAC) — always confirm which Market a Region belongs to before interpreting.

### Sales

- **Business meaning:** Invoiced revenue for the line item.
- **Data type:** Numeric (integer in this dataset).
- **Analytical meaning:** Top-line revenue metric; see `business_kpi_definitions.md`.
- **Common usage:** Nearly every business question involves Sales at some level of aggregation.
- **Pitfall:** Never interpret Sales alone as a profitability signal.

### Profit

- **Business meaning:** Net financial contribution of the line item after cost of goods, discount, and associated costs.
- **Data type:** Numeric (float; can be negative — roughly a quarter of all transaction lines carry negative Profit in this dataset).
- **Analytical meaning:** The company's primary bottom-line metric; see `business_kpi_definitions.md`.
- **Common usage:** Profitability analysis at every level of aggregation.
- **Pitfall:** Must always be summed, never row-averaged, when computing group-level profitability alongside Sales (see Profit Margin below).

### Quantity

- **Business meaning:** Number of units sold in the line item.
- **Data type:** Integer.
- **Analytical meaning:** Volume metric, independent of price.
- **Common usage:** Demand and logistics analysis; distinguishing volume effects from price/discount effects (root-cause playbook, Step 5).
- **Pitfall:** High Quantity does not imply high Sales or Profit.

### Discount

- **Business meaning:** The proportion of list price removed as a promotional or negotiated reduction.
- **Data type:** Numeric, float, range 0.00–0.85 in this dataset (proportion, not percentage — e.g., 0.20 means 20%).
- **Analytical meaning:** Central variable in pricing and margin analysis (see `pricing_discount_policy.md`).
- **Common usage:** Discount-tier analysis, margin decomposition.
- **Pitfall:** Confirm whether a given report expects a proportion (0–1) or a percentage (0–100) representation before combining Discount with other percentage-based metrics.

### Shipping Cost

- **Business meaning:** The logistics cost incurred to fulfill the line item.
- **Data type:** Numeric (float).
- **Analytical meaning:** Direct cost deduction affecting Profit; see `shipping_fulfillment_policy.md`.
- **Common usage:** Fulfillment cost analysis, Shipping-Cost-as-%-of-Sales calculations.
- **Pitfall:** Positively correlated with Sales/order size — always normalize before cross-group comparison.

### Ship Mode

- **Business meaning:** The carrier service level used to fulfill the order line: `Same Day`, `First Class`, `Second Class`, `Standard Class`.
- **Data type:** Categorical (4 values).
- **Analytical meaning:** Primary driver of Shipping Cost variation (see `shipping_fulfillment_policy.md`).
- **Common usage:** Ship Mode mix analysis, cost-efficiency investigation.
- **Pitfall:** Do not assume a strict one-to-one mapping between Ship Mode and Order Priority — they are related but distinct fields.

### Order Priority

- **Business meaning:** The customer service commitment level assigned to the order: `Critical`, `High`, `Medium`, `Low`.
- **Data type:** Categorical (4 values).
- **Analytical meaning:** Reflects customer/account commitment, not the fulfillment method itself.
- **Common usage:** Service-level analysis, escalation criteria in `shipping_fulfillment_policy.md`.
- **Pitfall:** Higher Order Priority correlates with higher average Shipping Cost but is not identical to Ship Mode — analyze both fields together, not interchangeably.

### Profit Margin (row-level field)

- **Business meaning:** The Profit-to-Sales ratio recorded for that individual transaction line.
- **Data type:** Numeric (float; percentage or ratio depending on dataset scaling).
- **Analytical meaning:** Useful for row-level or transaction-level inspection only.
- **Common usage:** Identifying individual outlier transactions with extreme margin.
- **Pitfall — CRITICAL:** **Profit Margin should be interpreted carefully when Sales is zero or very small.** A near-zero Sales denominator can produce an extreme or undefined row-level margin percentage that does not reflect the transaction's true business significance. Furthermore, **this row-level field must never be simply averaged (`AVG`) to represent a group's aggregate margin** — the correct aggregate calculation is always `SUM(Profit) / SUM(Sales) × 100`, as detailed in `business_kpi_definitions.md`. Averaging row-level margins gives disproportionate weight to small transactions and will produce a materially incorrect picture of group profitability.

---

## Summary Table: Grain and Correct Aggregation Key

| Question Type | Correct Grouping Key |
|---|---|
| "How many line items?" | `COUNT(Row ID)` |
| "How many orders?" | `COUNT(DISTINCT Order ID)` |
| "How many customers?" | `COUNT(DISTINCT Customer ID)` |
| "How many products?" | `COUNT(DISTINCT Product ID)` |
| "What is aggregate Profit Margin?" | `SUM(Profit) / SUM(Sales) × 100` — never `AVG(profit_margin)` |
| "What is Average Order Value?" | `SUM(Sales) / COUNT(DISTINCT Order ID)` |

---

### Document Scope

**This document can establish:** the precise business and technical meaning of every field in Meridian's transaction dataset, the correct grain for each type of aggregation, and the known pitfalls an analyst must avoid.

**This document cannot establish:** the actual values, distributions, or trends of any field for a specific query — those must be computed directly from the transaction dataset using the grain and aggregation rules defined here.
