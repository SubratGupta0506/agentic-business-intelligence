# Meridian Global Retail Group — Product and Category Management Policy

**Document Type:** Internal Policy — Category Management
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is **fictional internal category-management documentation** created for this AI/ML portfolio project. It is not an official document of the original Global Superstore dataset provider. Product names referenced as examples are drawn directly from the uploaded dataset for realism; commentary about their strategic status is fictional demo content.

---

## 1. Purpose

This policy defines how Meridian manages its product portfolio across Categories and Sub-Categories, and — critically — gives AI analysts a framework for distinguishing between product performance dimensions that are frequently and incorrectly treated as interchangeable.

## 2. Category and Sub-Category Structure

Meridian's catalog is organized into three Categories and seventeen Sub-Categories:

| Category | Sub-Categories |
|---|---|
| **Technology** | Phones, Copiers, Machines, Accessories |
| **Office Supplies** | Paper, Art, Storage, Appliances, Supplies, Envelopes, Fasteners, Labels, Binders |
| **Furniture** | Tables, Bookcases, Chairs, Furnishings |

Each Sub-Category is owned by a Category Manager accountable for assortment, vendor pricing, and Sub-Category-level profitability.

## 3. Category Performance Overview

At the Category level, Meridian's transaction history shows three distinct economic profiles:

- **Technology** — the largest Category by Sales and the strongest by aggregate Profit Margin, led by Copiers (the highest-margin Sub-Category in the portfolio) and Phones (the highest-Sales Sub-Category).
- **Office Supplies** — the highest Category by order/line-item count and Quantity sold (a high-frequency, lower-ticket Category), with solid aggregate Profit Margin.
- **Furniture** — comparable in total Sales to Office Supplies but with by far the weakest aggregate Profit Margin of the three Categories, driven primarily by its Tables Sub-Category.

**Key finding requiring ongoing monitoring:** Tables is Meridian's only Sub-Category with a **negative aggregate Profit Margin** across the full transaction history, coinciding with the highest average Discount of any Sub-Category. This combination — high discount + structurally negative margin — is the clearest portfolio-level margin risk in Meridian's current business and is referenced throughout `pricing_discount_policy.md` and `root_cause_analysis_playbook.md` as a canonical investigation case.

## 4. Distinguishing Product Performance Dimensions

A central principle of Meridian's category management practice is that the following six dimensions are **not the same thing** and must be evaluated independently before drawing conclusions about a product's health:

| Dimension | What it measures | What it does NOT tell you |
|---|---|---|
| **High Sales** | Strong revenue generation | Says nothing about whether the product is profitable |
| **High Profit** | Strong absolute dollar contribution | A high-Sales, thin-margin product can still generate high absolute Profit; doesn't tell you about margin health |
| **High Margin** | Strong Profit relative to Sales (`Profit/Sales`) | A high-margin product with very low Sales may be immaterial to overall business performance |
| **High Quantity** | Large unit volume | High unit volume at low unit price may still generate low total Sales/Profit; common for low-ticket Office Supplies |
| **High Discount** | Heavy promotional/negotiated price reduction | Does not by itself mean a product is unprofitable — depends on the product's baseline margin (Section 3) |
| **High Shipping Cost** | Expensive to fulfill (often due to size/weight) | Does not by itself mean a product is unprofitable if Sales/margin are strong enough to absorb it |

**Analyst rule:** Never describe a product as "underperforming" or "a strong performer" based on only one of these six dimensions. A complete product assessment reports Sales, Profit, Margin, Quantity, average Discount, and average Shipping Cost together.

## 5. Sales Concentration and High-Revenue Products

Meridian's highest-Sales products are concentrated in the Phones and Copiers Sub-Categories (e.g., smartphone product lines from multiple brands, and high-end copier models), alongside premium Furniture items such as executive leather armchairs. Notably:

- Several of Meridian's highest-Sales individual products realize only modest Profit relative to their Sales, and at least one high-Sales phone product realizes a **net negative Profit** — a clear example of "high Sales" not implying "high Profit," reinforcing Section 4.
- High-Sales Furniture items (e.g., premium armchairs) tend to show a smaller Profit-to-Sales ratio than high-Sales Technology items, consistent with the Category-level pattern in Section 3.

## 6. Underperforming and High-Risk Products

Meridian's transaction history identifies a recurring underperformer profile: **specialty/high-ticket equipment with low unit volume and negative cumulative Profit** — for example, 3D printer product lines and certain large conference/occasional tables show meaningfully negative cumulative Profit despite non-trivial Sales. These products share two characteristics worth flagging in any AI-assisted review:

- Low order/unit count (a handful of transactions), meaning a small number of unusually unprofitable orders can dominate the product's entire performance history — analysts should check whether an "underperforming product" finding is driven by broad-based weakness or by one or two outlier transactions.
- Presence in already-thin-margin Sub-Categories (Furniture, certain Machines), compounding the effect described in Section 3.

## 7. Discount-Heavy Products

Because Discount and Profit Margin are inversely related in Meridian's data (see `pricing_discount_policy.md`, Section 5), products or Sub-Categories with above-average Discount rates deserve routine profitability review, especially:

- **Tables** and other Furniture Sub-Categories (Chairs, Machines) — above-average Discount, below-average margin.
- Category Managers are expected to review any Sub-Category where average Discount exceeds roughly 15–17% (the level at which Meridian's aggregate margin curve begins compressing meaningfully; see `pricing_discount_policy.md`, Section 5) alongside that Sub-Category's Profit Margin trend.

## 8. Product Lifecycle Considerations

Meridian's category managers consider four lifecycle stages when interpreting product-level anomalies:

1. **Introduction** — new SKUs may show low Quantity and inconsistent margin as pricing is calibrated; not a reliable performance signal yet.
2. **Growth** — Quantity and Sales should be rising together; margin should stabilize.
3. **Maturity** — the expected steady state; deviations here (sudden Discount increases, margin compression) are the most meaningful anomalies.
4. **Decline / Clearance** — deliberately discounted to reduce inventory; negative or thin margin here may be an accepted, planned outcome rather than a problem, provided it is time-bound.

**Analyst caution:** the transaction dataset does not record which lifecycle stage a product is in. A negative-margin product could be a planned clearance (acceptable) or a chronic structural problem (requires action) — this distinction is an UNKNOWN that requires category-manager input unless corroborated by a sustained multi-period pattern (see `business_analysis_governance.md`).

## 9. Product-Level and Category-Level Anomaly Investigation

Recommended sequence when a product or Sub-Category is flagged as anomalous:

1. Confirm the anomaly using aggregate Sales, Profit, and Margin (`SUM(Profit)/SUM(Sales)`) — not row-averaged margin.
2. Check order/transaction count — is the finding based on enough transactions to be reliable, or driven by a small number of outliers (Section 6)?
3. Check average Discount trend for the product/Sub-Category.
4. Check Region/Market distribution — is the anomaly global or concentrated in specific geographies?
5. Check Shipping Cost relative to Sales for the product/Sub-Category.
6. Classify findings as FACT / INFERENCE / UNKNOWN per the root-cause playbook.

## 10. Regional Product Differences

Category mix varies by Region and Market — for example, a Region with a Furniture-heavy purchase mix will show a structurally lower blended Profit Margin than a Region skewed toward Technology, independent of any pricing or operational issue. Analysts comparing Regional performance must control for Category mix before concluding that one Region is "less efficient" than another (a composition effect vs. a genuine performance issue — see `root_cause_analysis_playbook.md`).

## 11. Recommended Product/Category KPIs

- Sales, Profit, and aggregate Profit Margin by Category and Sub-Category
- Quantity sold by Category and Sub-Category
- Average Discount by Category and Sub-Category
- Average Shipping Cost by Category and Sub-Category
- Top-N and bottom-N products by Profit (not Sales alone)
- Share of Sub-Category Sales occurring at Discount > 20%

## 12. Escalation Rules

Escalate a product/Category finding when:

- A Sub-Category's aggregate Profit Margin is negative or approaches zero over a sustained period (as is already true for Tables).
- A high-Sales product shows negative cumulative Profit.
- A Sub-Category's average Discount rises materially without a documented clearance/lifecycle rationale.
- A Regional Category mix shift is large enough to materially change that Region's blended margin.

---

### Document Scope

**This document can establish:** Meridian's fictional category-management framework, the documented Category/Sub-Category profitability structure in the transaction dataset (including the Tables margin issue), and the correct analytical distinctions between Sales, Profit, Margin, Quantity, Discount, and Shipping Cost.

**This document cannot establish:** the actual lifecycle stage of any product, real vendor cost structures, inventory levels, or the deliberate intent behind any specific discount or pricing decision. These require information outside the transaction dataset.
