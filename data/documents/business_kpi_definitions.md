# Meridian Global Retail Group — Business KPI and Metrics Definitions

**Document Type:** Internal Reference — KPI Dictionary
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is **fictional internal KPI documentation** created for this AI/ML portfolio project. It is not an official document of the original Global Superstore dataset provider. Calculation logic reflects the actual fields present in the uploaded dataset (Sales, Profit, Quantity, Discount, Shipping Cost, Profit Margin) and standard business-analytics practice.

---

## Purpose

This document is the canonical reference for how Meridian defines, calculates, and interprets its core business metrics. Any AI agent performing business analysis on Meridian's transaction data should use these definitions consistently, especially the **aggregate Profit Margin calculation rule** in Section on Profit Margin, which is the single most common source of analytical error in this dataset.

---

## Sales

1. **Definition:** The invoiced revenue recorded for a transaction line item, before subtracting cost of goods, discount already applied, or shipping cost.
2. **Business meaning:** Represents top-line revenue generation; the starting point for all downstream profitability calculation.
3. **Calculation logic:** Recorded directly per Row ID; aggregate Sales for any group = `SUM(Sales)` across the relevant rows.
4. **Interpretation:** High Sales indicates strong revenue generation but says nothing about profitability (see `product_category_management.md`, Section 4).
5. **Common mistakes:** Treating Sales growth as inherently positive without checking Profit and Margin in the same period; comparing Sales across Order IDs without recognizing an Order may contain multiple Row ID line items.
6. **Example business question:** "Which Region generated the most Sales in 2014?"
7. **When misleading:** When driven by heavy discounting or a shift toward high-volume, low-margin products — Sales growth can mask deteriorating profitability ("profitless growth").

## Profit

1. **Definition:** The net financial contribution of a transaction line item after cost of goods, discount, and associated costs are accounted for.
2. **Business meaning:** The true economic value generated; the metric Meridian ultimately optimizes for, subject to acceptable Sales growth.
3. **Calculation logic:** Recorded directly per Row ID; aggregate Profit for any group = `SUM(Profit)`. Profit can be negative at the row level (Meridian's data shows roughly a quarter of all transaction lines carry negative Profit).
4. **Interpretation:** Profit must always be read alongside Sales — a Region or product with modest Sales but healthy Profit may be a better business outcome than one with high Sales and thin Profit.
5. **Common mistakes:** Averaging row-level Profit instead of summing it when reporting a group total; ignoring negative-Profit transactions when they are a meaningful share of volume.
6. **Example business question:** "Which Sub-Category contributes the most Profit to the company?"
7. **When misleading:** A single very large or very negative transaction can distort a small group's total Profit — always check transaction count alongside Profit totals.

## Quantity

1. **Definition:** The number of units sold in a transaction line item.
2. **Business meaning:** A volume metric, independent of price; used for demand and logistics planning.
3. **Calculation logic:** `SUM(Quantity)` for aggregate unit volume.
4. **Interpretation:** High Quantity does not imply high Sales or Profit — low-ticket Office Supplies items often carry the highest Quantity in the portfolio while contributing modestly to total Sales.
5. **Common mistakes:** Conflating "best-selling" (highest Quantity) with "highest-Sales" or "most profitable" — these are frequently different products.
6. **Example business question:** "Which Sub-Category sells the most units?"
7. **When misleading:** When used alone to judge product importance without Sales/Profit context.

## Discount

1. **Definition:** The proportion (0.00–1.00) of list price removed from a transaction as a promotional or negotiated reduction.
2. **Business meaning:** A lever for driving volume, clearing inventory, or rewarding account relationships — but a direct cost to margin.
3. **Calculation logic:** Recorded per Row ID; average Discount for a group = `AVG(Discount)`, or better, Sales-weighted average discount where relevant. Total discount "cost" is implicit in the gap between list price and recorded Sales/Profit.
4. **Interpretation:** See `pricing_discount_policy.md` for the detailed Discount-to-Margin relationship documented in Meridian's data (margin compresses steadily as Discount rises, turning negative above roughly 20–30%).
5. **Common mistakes:** Assuming Discount level alone determines Profit outcome without considering baseline Category/Sub-Category margin.
6. **Example business question:** "Did average Discount rise in the Furniture Category last quarter?"
7. **When misleading:** A rising average Discount in a naturally high-margin Category (e.g., Technology) may be far less concerning than the same rise in an already-thin-margin Category (e.g., Furniture).

## Shipping Cost

1. **Definition:** The logistics cost incurred by Meridian to fulfill a transaction line item.
2. **Business meaning:** A direct cost that reduces Profit; driven by Ship Mode, Order Priority, geography, and product characteristics (see `shipping_fulfillment_policy.md`).
3. **Calculation logic:** Recorded per Row ID; aggregate Shipping Cost = `SUM(Shipping Cost)`. Should typically be evaluated as a % of Sales for comparability across groups of different size.
4. **Interpretation:** Positively correlated with Sales (larger orders cost more to ship) — raw Shipping Cost comparisons across differently sized groups are misleading without normalization.
5. **Common mistakes:** Treating a fall in total Shipping Cost as automatically positive without checking whether it reflects genuine efficiency or a mix/volume shift (see `shipping_fulfillment_policy.md`, Section 8).
6. **Example business question:** "What is Shipping Cost as a percentage of Sales, by Region?"
7. **When misleading:** When compared in absolute terms across Regions or time periods of very different order volume.

## Profit Margin

1. **Definition:** Profit expressed as a percentage of Sales, indicating how much of each revenue dollar is retained as profit.
2. **Business meaning:** Meridian's primary profitability-efficiency metric — the metric of choice when comparing groups of different size (Regions, Categories, customers).
3. **Calculation logic — CRITICAL RULE:**

   **Aggregate Profit Margin must be calculated as:**

   ```
   Profit Margin (%) = SUM(Profit) / SUM(Sales) × 100
   ```

   **It must NOT be calculated by averaging the row-level `profit_margin` field** (i.e., `AVG(profit_margin)` across transactions). The uploaded dataset includes both a row-level `profit_margin` field (the margin of that individual transaction) and the underlying `Sales`/`Profit` fields needed to compute the correct aggregate margin. These two approaches give materially different — and for aggregate reporting, the row-average approach is **wrong** — results, because row-level averaging gives equal weight to a $10 transaction and a $10,000 transaction, distorting the true blended margin. Meridian's own data illustrates this clearly: the correctly weighted aggregate company-wide margin (`SUM(Profit)/SUM(Sales)`) is meaningfully different from the simple average of row-level margins, precisely because small, high-margin transactions and large, low-margin (or loss-making) transactions do not offset proportionally under simple averaging.

4. **Interpretation:** Always compute Profit Margin at the level of aggregation relevant to the question (Category, Region, customer, time period) using the `SUM(Profit)/SUM(Sales)` formula for that specific group.
5. **Common mistakes:** Using `AVG(profit_margin)`; comparing Profit Margin across groups without controlling for Category/Segment/Region mix (a composition effect, not a true efficiency difference).
6. **Example business question:** "What is the aggregate Profit Margin for the Furniture Category in 2014?"
7. **When misleading:** When Sales in the denominator are very small (near zero), Profit Margin can swing to extreme percentage values that overstate the practical significance of the finding — always check the underlying Sales magnitude alongside any extreme margin figure.

## Average Order Value (AOV)

1. **Definition:** The average Sales value per Order.
2. **Business meaning:** Indicates typical basket size; useful for tracking upsell/cross-sell effectiveness.
3. **Calculation logic:** `SUM(Sales) / COUNT(DISTINCT Order ID)` for the relevant group. Must use distinct Order ID, not Row ID, since an Order can contain multiple line items.
4. **Interpretation:** Rising AOV with flat order count can offset a decline in new customer acquisition; falling AOV with rising order count may indicate more, smaller purchases.
5. **Common mistakes:** Dividing Sales by Row ID count instead of distinct Order ID count, which understates true AOV.
6. **Example business question:** "Has average order value increased in the Corporate Segment?"
7. **When misleading:** A single very large Order can distort AOV for a small group.

## Revenue Growth

1. **Definition:** The percentage change in Sales between two comparable periods.
2. **Business meaning:** The headline top-line trend indicator.
3. **Calculation logic:** `(Sales_current − Sales_prior) / Sales_prior × 100`, always compared over equivalent period lengths (month-over-month, year-over-year).
4. **Interpretation:** Must be paired with Profit Growth to assess whether growth is healthy or "profitless."
5. **Common mistakes:** Comparing non-equivalent periods (e.g., a 31-day month vs. a 28-day month without normalization) or ignoring seasonality.
6. **Example business question:** "What was year-over-year Revenue Growth in APAC?"
7. **When misleading:** Driven entirely by discounting or a one-off large order rather than sustainable demand growth.

## Profit Growth

1. **Definition:** The percentage change in Profit between two comparable periods.
2. **Business meaning:** Indicates whether the business is becoming more or less profitable in absolute terms.
3. **Calculation logic:** `(Profit_current − Profit_prior) / Profit_prior × 100`, with care taken when Profit_prior is negative or near zero (percentage change becomes unstable/misleading).
4. **Interpretation:** Should always be compared against Revenue Growth in the same period to distinguish genuine profitability improvement from simple volume growth.
5. **Common mistakes:** Computing percentage growth when the prior-period base is negative or near zero, producing a nonsensical or exaggerated percentage.
6. **Example business question:** "Did Profit Growth keep pace with Revenue Growth in Q3 2014?"
7. **When misleading:** When baseline Profit is small, minor absolute changes produce large, misleading percentage swings.

## Profit Margin Change

1. **Definition:** The change (in percentage points, not percent-of-percent) in aggregate Profit Margin between two periods.
2. **Business meaning:** Isolates whether profitability *efficiency* improved or worsened, independent of volume growth.
3. **Calculation logic:** `Margin_current − Margin_prior`, both computed using `SUM(Profit)/SUM(Sales)`.
4. **Interpretation:** A negative Profit Margin Change alongside positive Revenue Growth is the definitive signature of "profitless growth," warranting a full root-cause investigation (see `root_cause_analysis_playbook.md`).
5. **Common mistakes:** Reporting Margin Change as a percentage of the prior margin rather than a simple percentage-point difference, which confuses stakeholders.
6. **Example business question:** "Did Profit Margin improve or decline in Furniture year-over-year?"
7. **When misleading:** Rarely misleading on its own, but must be decomposed by Category/Region/Discount to explain *why* it moved.

## Order Volume

1. **Definition:** The count of distinct Orders (or, secondarily, line items) placed in a period.
2. **Business meaning:** A demand and operational-load indicator.
3. **Calculation logic:** `COUNT(DISTINCT Order ID)` for Order Volume; `COUNT(Row ID)` for line-item volume — these are different numbers and must be labeled accordingly.
4. **Interpretation:** Order Volume growth without AOV or Sales growth suggests more, smaller transactions.
5. **Common mistakes:** Using Row ID count when Order Volume (distinct orders) is what's being asked for.
6. **Example business question:** "How many distinct orders did the Consumer Segment place in 2014?"
7. **When misleading:** Can rise even while total Sales falls, if average order size shrinks faster than order count grows.

## Customer Value

1. **Definition:** A composite view of a customer's Sales, Profit, and order frequency over their relationship with Meridian.
2. **Business meaning:** Drives account prioritization and retention investment decisions (see `customer_segmentation_strategy.md`).
3. **Calculation logic:** Aggregate Sales, aggregate Profit, and order count per Customer ID; should never be reduced to Sales alone.
4. **Interpretation:** A customer must be assessed on Sales AND Profit together — Meridian's data contains high-Sales customers with thin or negative aggregate Profit.
5. **Common mistakes:** Ranking "best customers" by Sales alone.
6. **Example business question:** "Who are Meridian's most profitable customers, not just highest-Sales customers?"
7. **When misleading:** A customer with few but very large orders can appear high-value on a short window but be volatile over time.

## Category Contribution

1. **Definition:** The share of total company Sales or Profit attributable to a given Category.
2. **Business meaning:** Used for portfolio balance and investment prioritization.
3. **Calculation logic:** `SUM(Sales or Profit for Category) / SUM(Sales or Profit company-wide) × 100`.
4. **Interpretation:** Sales contribution and Profit contribution can differ substantially by Category (e.g., Furniture's Sales contribution is much larger than its Profit contribution, reflecting its thin margin).
5. **Common mistakes:** Reporting only Sales contribution and implying it reflects profitability contribution.
6. **Example business question:** "What share of total company Profit comes from Technology vs. Furniture?"
7. **When misleading:** When a Category's Sales share and Profit share diverge sharply, citing only one paints an incomplete picture.

## Regional Contribution

1. **Definition:** The share of total company Sales or Profit attributable to a given Region or Market.
2. **Business meaning:** Used for resource allocation and regional strategy.
3. **Calculation logic:** Analogous to Category Contribution, computed by Region or Market.
4. **Interpretation:** Should be reviewed alongside Regional Profit Margin, since high Sales contribution does not imply high Profit contribution (see `root_cause_analysis_playbook.md` for the "high-Sales, poor-profitability region" scenario).
5. **Common mistakes:** Equating Sales contribution rank with overall regional importance without checking Profit.
6. **Example business question:** "Which Region contributes the most to company Profit?"
7. **When misleading:** A Region can rank high on Sales contribution and low on Profit contribution simultaneously — both figures should always be reported together.

## Product Contribution

1. **Definition:** The share of total company Sales or Profit attributable to an individual product.
2. **Business meaning:** Identifies portfolio concentration and dependency risk at the SKU level.
3. **Calculation logic:** `SUM(Sales or Profit for Product) / SUM(Sales or Profit company-wide) × 100`.
4. **Interpretation:** Meridian's product base (over 10,000 distinct products) is broad, so any single product's Sales/Profit contribution is typically small — high concentration in a single product would be an unusual and noteworthy finding.
5. **Common mistakes:** Treating a "top 10 products by Sales" list as evidence of overall product concentration risk without measuring their actual share of total Sales.
6. **Example business question:** "Does any single product represent an outsized share of Category Profit?"
7. **When misleading:** Rare individual high-Sales transactions can make a product appear more significant than its sustained contribution over time.

---

### Document Scope

**This document can establish:** the precise definition, calculation method, and correct interpretation of every core KPI used across Meridian's business documentation and analysis, including the mandatory `SUM(Profit)/SUM(Sales)` rule for aggregate Profit Margin.

**This document cannot establish:** the actual value of any KPI for a specific period, Region, Category, or customer — those values must always be computed directly from the transaction dataset via SQL, using the definitions provided here.
