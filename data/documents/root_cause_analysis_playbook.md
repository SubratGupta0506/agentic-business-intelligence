# Meridian Global Retail Group — Business Investigation and Root-Cause Analysis Playbook

**Document Type:** Internal Methodology — Business Intelligence & Analytics
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is **fictional internal methodology documentation** created for this AI/ML portfolio project. It is not an official document of the original Global Superstore dataset provider. This playbook does not itself contain conclusions about any real historical event — it defines the *method* an AI or human analyst should follow when investigating Meridian's transaction data.

---

## Purpose

This is the primary investigative methodology document for Meridian's Business Intelligence function and any AI agent performing business analysis on Meridian's transaction data. It applies to any "why did X happen" question — sales decline, profit decline, margin compression, regional underperformance, category decline, shipping cost increase, quantity decline, or rising discounting.

This document should be treated as **high-priority context** by any retrieval system: nearly every complex business question routes through this methodology.

---

## The Seven-Step Investigation Methodology

### Step 1 — Validate the Event

Before investigating *why* something happened, confirm that it **actually happened** and is not a data artifact.

- Query the exact metric and period cited in the question directly from the transaction data.
- Check for data completeness in that period (e.g., partial-month data, missing days) before concluding a genuine decline or spike occurred.
- Confirm the metric direction (decline vs. spike) and the exact field involved (Sales? Profit? Quantity? Margin?) — these are frequently conflated (see `business_kpi_definitions.md`).

**Output of this step:** A confirmed, quantified statement such as "Sales in [period] were $X, compared to $Y in [comparison period] — a confirmed decline/increase of Z%." If the event cannot be confirmed in the data, stop here and report that the premise is not supported by the data.

### Step 2 — Establish the Baseline

A single number is meaningless without a comparison point. Establish the appropriate baseline(s):

- **Previous month** — for short-term operational movements.
- **Previous quarter** — for seasonal or campaign-driven effects.
- **Previous year (same period)** — for the most reliable comparison, since it controls for seasonality (Meridian's Sales data shows a clear seasonal pattern, generally rising through the second half of the calendar year toward Q4).
- **Multi-year trend** — for structural (multi-year) shifts versus one-off fluctuations.

**Rule:** Never judge a monthly movement using only month-over-month comparison if seasonality is plausible — always cross-check against the same month in the prior year.

### Step 3 — Identify Magnitude

Quantify the change precisely:

- **Absolute change:** `Value_current − Value_baseline`
- **Percentage change:** `(Value_current − Value_baseline) / Value_baseline × 100`

Report both. A large percentage change on a small absolute base (or vice versa) should be flagged explicitly — e.g., "Sales in [Region] fell 40%, but this represents only $12,000 of the company's $12.6M total Sales" versus "Sales fell 5%, representing $600,000."

### Step 4 — Decompose the Change

This is the most important step. Break the aggregate change down along every relevant business dimension available in the dataset:

- **Region / Country** — is the change broad-based (every Region) or concentrated (one Region driving it)?
- **Category / Sub-Category** — is one product area responsible, or is it uniform across the portfolio?
- **Product** — is a small number of specific products (or even a small number of individual transactions) responsible?
- **Customer Segment** — Consumer, Corporate, or Home Office?
- **Quantity vs. Price/Discount** — did fewer units sell, or did the same units sell at a lower effective price (higher Discount)?
- **Shipping Cost** — did fulfillment cost changes contribute to a Profit or Margin movement, independent of Sales?

**Rule:** A company-wide movement should always be decomposed until you can state which specific dimension(s) account for the majority of the change. "Sales declined" is an incomplete finding; "Sales declined, driven primarily by a decline in the [Region] Region's [Category] Category, with [Sub-Category] the largest single contributor" is a complete finding.

### Step 5 — Identify Correlated Drivers

Once the change is decomposed, examine which other metrics moved *at the same time and in the same segment*:

- Did average Discount rise or fall in the affected segment during the same period?
- Did Quantity move in the same direction as Sales (implying a genuine demand change) or the opposite direction (implying a price/discount effect)?
- Did Shipping Cost or Ship Mode mix shift in the affected segment?
- Did Order Priority mix shift?

**Rule:** A correlated driver is evidence, not proof. Two metrics moving together in the same period and segment is a **FACT** about co-occurrence; the claim that one *caused* the other is, at best, an **INFERENCE** (Step 6).

### Step 6 — Separate Evidence From Hypothesis

Every conclusion in a Meridian business analysis report must be explicitly classified into one of three categories:

| Classification | Definition | Example |
|---|---|---|
| **FACT** | Directly supported by the transaction data, verifiable via SQL | "Furniture Sales in the Central Region fell 18% in Q3 2014 vs. Q3 2013." |
| **INFERENCE** | A reasonable interpretation supported by correlated evidence in the data, but not proven | "The decline appears associated with a rise in average Discount in the same Region and Category, consistent with the margin-compression pattern documented in `pricing_discount_policy.md`." |
| **UNKNOWN** | Cannot be determined from the available transaction data | "Whether a competitor promotion or a change in account management strategy contributed to this decline cannot be determined from the transaction data alone." |

**Rule:** Never present an INFERENCE using FACT-level language (e.g., avoid "discounting caused the decline" — prefer "the decline is consistent with / coincides with a rise in discounting"). Never omit the UNKNOWN category when relevant external factors plausibly apply.

### Step 7 — State Limitations

Every investigation report must explicitly state what the transaction dataset **cannot** establish. Common limitations relevant to Meridian's data include:

- **Competitor activity** — pricing, promotions, or market entry by competitors is not recorded.
- **Economic conditions** — macroeconomic shifts affecting customer demand are not recorded.
- **Management intent** — whether a discount, pricing change, or Ship Mode shift was a deliberate strategic decision or an operational drift is not recorded.
- **Marketing campaigns** — campaign timing, spend, or targeting not reflected in Order-level data cannot be linked to Sales movements with certainty.
- **External market events** — regulatory changes, supply disruptions, or geopolitical events are not recorded.
- **Inventory availability** — stockouts or supply constraints are not recorded in this dataset; a Quantity decline could reflect either falling demand or unavailable stock, and the two cannot be distinguished from Sales data alone.
- **Customer satisfaction / churn** — actual customer sentiment, complaints, or churn reasons are not recorded; only purchasing behavior is observable.

---

## Worked Example Structure (Template)

When responding to a "why" question, an AI agent should structure its answer as follows:

1. **Event validation** (Step 1) — confirmed magnitude and direction.
2. **Baseline comparison** (Step 2) — which comparison period(s) were used and why.
3. **Decomposition findings** (Steps 3–4) — a ranked breakdown of which dimensions explain the majority of the change.
4. **Correlated drivers** (Step 5) — what else moved alongside the primary change.
5. **Classified conclusions** (Step 6) — explicit FACT / INFERENCE / UNKNOWN statements.
6. **Stated limitations** (Step 7) — what cannot be determined from this dataset.
7. **Recommended next step** — what additional data (internal system, campaign calendar, competitive intelligence) would be needed to move an INFERENCE toward a FACT.

## Applying the Methodology to Common Question Types

| Question Type | Primary Decomposition Axes (Step 4) | Likely Correlated Drivers to Check (Step 5) |
|---|---|---|
| Why did Sales decline/spike? | Region, Category, Segment, Quantity | Discount, seasonality, Order Volume |
| Why did Profit decline? | Region, Category, Sub-Category | Discount, Shipping Cost, Sales mix |
| Why did Margin decrease? | Category, Sub-Category, Segment | Discount tier mix (`pricing_discount_policy.md`) |
| Why did a Region underperform? | Category mix within Region, Country/City | Discount, Shipping Cost, Segment mix |
| Why did a Category decline? | Sub-Category, Region, Product | Discount, Quantity, competing Sub-Categories |
| Why did Shipping Cost increase? | Ship Mode mix, Order Priority mix, Region | Order volume/size, geography (`shipping_fulfillment_policy.md`) |
| Why did Quantity decline? | Product, Sub-Category, Region | Price/Discount changes, Order count |
| Why did Discounting increase? | Segment, Category, Region | Approval-tier mix shift (`pricing_discount_policy.md`) |

## Cross-References

This playbook should always be used together with:

- `business_kpi_definitions.md` — for correct metric calculation (especially aggregate Profit Margin).
- `pricing_discount_policy.md` — for interpreting Discount-related findings.
- `shipping_fulfillment_policy.md` — for interpreting Shipping Cost and Ship Mode findings.
- `customer_segmentation_strategy.md` and `product_category_management.md` — for customer- and product-level decomposition.
- `business_analysis_governance.md` — for the formal rules governing evidence classification and causal claims.

---

### Document Scope

**This document can establish:** the correct, repeatable methodology for investigating any performance change in Meridian's transaction data, and the discipline required to separate confirmed facts from reasonable inferences and genuine unknowns.

**This document cannot establish:** the actual answer to any specific "why did X happen" question — that requires applying this methodology to the transaction data for the specific period and dimension in question, and explicitly acknowledging where the data's explanatory power ends.
