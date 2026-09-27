# Meridian Global Retail Group — Pricing and Discount Management Policy

**Document Type:** Internal Policy — Pricing & Revenue Management
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** This is a **fictional internal policy** created for this AI/ML portfolio project. It does not represent, and should never be cited as, an actual policy of the original Global Superstore dataset provider. The discount thresholds, approval levels, and escalation rules below are demo content designed to be realistic and internally consistent with the uploaded transaction data — they are not historical facts about how any discount was actually approved.

---

## 1. Purpose

This policy defines how Meridian Global Retail Group sets prices, applies discounts, and governs discounting activity across all Categories, Segments, and Markets. It exists so that revenue growth from discounting never comes at the expense of uncontrolled Profit Margin erosion, and so that an AI business analyst reviewing transaction-level Discount data has a consistent framework for interpreting what it sees.

## 2. Pricing Principles

1. **List price is the baseline.** Every product carries a standard list price from which the recorded `Sales` value and `Discount` are derived on a per-line basis.
2. **Discount is proportional, not absolute.** The `Discount` field is recorded as a proportion (0.00–1.00) of list price removed from the transaction, not a flat currency amount.
3. **Margin protection outranks volume growth.** Discounting exists to grow volume or clear inventory, but never at the cost of turning a Category structurally unprofitable.
4. **Pricing authority is tiered.** Front-line sales staff, account managers, and regional pricing directors hold different discount authority levels (Section 4).
5. **Category economics differ.** Technology, Office Supplies, and Furniture carry different baseline margins and therefore different discount tolerances (Section 6).

## 3. Standard and Promotional Pricing

- **Standard pricing** applies to the majority of transactions. Based on the transaction dataset, more than half of all order lines (roughly 57%) carry **zero discount**, representing full-price, standard-pricing transactions.
- **Promotional pricing** covers everything else: seasonal campaigns, clearance activity, negotiated Corporate/Home Office account discounts, and competitive price-matching. The dataset shows Discount values ranging from 0.00 up to a maximum of **0.85** (an 85% reduction from list price), which Meridian treats as the extreme tail of promotional/clearance activity rather than routine pricing.

## 4. Discount Tiers and Approval Rules

Meridian defines four internal discount tiers, mapped to the Discount field an analyst will see in transaction data:

| Tier | Discount Range | Approval Authority | Business Interpretation |
|---|---|---|---|
| **Tier 0 — Standard** | 0% | No approval needed (list price) | Baseline, healthy margin transaction |
| **Tier 1 — Routine Promotional** | 0–10% | Sales representative / account manager | Normal competitive or loyalty discount |
| **Tier 2 — Elevated** | 10–20% | Regional sales manager | Requires business justification (volume commitment, account tier) |
| **Tier 3 — High-Risk** | 20–30% | Regional pricing director | Requires written justification; margin impact must be modeled before approval |
| **Tier 4 — Severe / Clearance** | Above 30% | VP of Pricing & Revenue Management | Reserved for inventory clearance, end-of-life products, or contractual exceptions; requires post-hoc profitability review |

**Governance rule:** Any transaction with Discount above 30% should be treated by an AI analyst as a candidate for the "Severe / Clearance" tier and cross-checked against Sub-Category and product context (e.g., is this a known clearance Sub-Category, or an isolated anomaly?).

## 5. Margin Protection and the Discount–Profit Relationship

Aggregate analysis of Meridian's transaction history shows a strong, consistent relationship between discount depth and realized Profit Margin (`SUM(Profit) / SUM(Sales)`):

| Discount Band | Approx. Share of Sales | Realized Margin |
|---|---|---|
| 0% (no discount) | Largest share of total Sales | Strongly positive, highest margin band |
| 0–10% | Meaningful share | Positive but reduced margin |
| 10–20% | Meaningful share | Materially thinner margin |
| 20–30% | Small share | Margin approaches breakeven / can turn slightly negative |
| 30–50% | Notable share | Margin is **negative** — these transactions lose money on average |
| Above 50% | Smaller share | Margin is **deeply negative** — these transactions lose substantially more than their Sales value |

**Policy implication:** Discounts above roughly 20–30% are not merely "less profitable" — in Meridian's actual transaction history, the 30%+ discount bands are **net loss-making in aggregate**, meaning that in many cases the cost of goods and fulfillment exceeds what the discounted Sales price recovers. This is why Tiers 3 and 4 require pricing-director or VP sign-off: uncontrolled deep discounting is not a margin-thinning risk, it is a margin-destroying risk.

An AI analyst reviewing a period of margin decline should always check whether the **mix of Discount tiers shifted toward Tier 3/4** before concluding that "discounting is hurting profitability" — the relationship is directional in Meridian's data, but the magnitude of the shift must be measured, not assumed.

## 6. Category-Specific Discount Considerations

- **Furniture** carries Meridian's thinnest baseline margins of the three Categories and includes Meridian's only Sub-Category (Tables) that is **net unprofitable in aggregate** across the transaction history, coinciding with Tables also carrying the highest average discount of any Sub-Category. Furniture discounting therefore requires the tightest governance.
- **Technology** carries Meridian's strongest baseline margins (led by Copiers and Accessories) and can typically absorb moderate discounting (Tier 1–2) without turning unprofitable, though high-ticket items (e.g., Copiers, Machines) should be reviewed individually given their outsized revenue-per-unit.
- **Office Supplies** is a high-volume, generally healthy-margin Category; discount governance here focuses more on Sub-Category mix (e.g., Binders and Storage carry above-average discount rates) than on absolute risk.

Analysts should always evaluate discount policy compliance **at the Sub-Category level**, not just the Category level, because Sub-Category economics vary widely within the same Category (see `product_category_management.md`).

## 7. Regional Considerations

Discount authority and typical discount depth vary by Market because of differing competitive intensity and account structures:

- Markets with historically higher average Discount (e.g., EMEA) should be monitored for margin compression relative to Markets with lower average Discount (e.g., North Asia, Central Asia).
- Canada shows a distinct pattern in Meridian's data: zero recorded discounting combined with the highest realized Profit Margin of any Market — useful as an internal benchmark for "what full-price selling looks like," though its small transaction volume means it should not be over-generalized to larger Markets.
- Regional pricing directors are expected to benchmark their Region's discount mix against the company-wide distribution in Section 5 during quarterly reviews.

## 8. Customer-Segment Considerations

- **Corporate** and **Home Office** accounts are more likely to carry negotiated, recurring discount arrangements tied to account tier or purchase volume commitments; these should be reviewed against the *account's* cumulative profitability, not judged line-by-line.
- **Consumer** discounting is typically promotional/seasonal rather than negotiated and should be evaluated in the context of campaign timing.
- A Segment showing rising average Discount without a corresponding rise in Quantity or order count is a signal worth escalating (see Section 10).

## 9. Monitoring KPIs

Pricing & Revenue Management tracks the following on a monthly and quarterly basis:

- Average Discount, overall and by Category / Sub-Category / Market / Segment
- Share of Sales in each Discount Tier (Section 4)
- Aggregate Profit Margin (`SUM(Profit)/SUM(Sales)`) trended over time
- Share of transactions with Discount > 20% ("high-discount share")
- Correlation trend between Discount and Profit Margin within each Category

## 10. Escalation Conditions

An AI analyst or human reviewer should flag a discount-related finding for escalation when:

- The share of Sales in Tier 3/4 (>20% discount) **rises materially** period-over-period.
- A Category or Sub-Category's aggregate Profit Margin turns **negative** or declines sharply while its average Discount has also risen.
- A single Region or Market's average Discount diverges significantly from the company-wide average without a known promotional campaign context.
- A high-Sales product or customer account shows a persistently high Discount alongside low or negative Profit (see `product_category_management.md` and `customer_segmentation_strategy.md`).

## 11. Examples: Acceptable vs. Risky Discount Patterns

**Acceptable pattern:** A Technology Sub-Category with strong baseline margin shows a moderate rise in average Discount (e.g., from 10% to 14%) during a defined promotional period, with a proportional rise in Quantity sold and Profit Margin remaining positive, even if compressed.

**Risky pattern:** A Furniture Sub-Category shows average Discount climbing above 25–30%, Quantity growth that does not offset the margin compression, and aggregate Profit Margin moving toward or below zero. This matches the profile Meridian's Tables Sub-Category already exhibits in the transaction history and is the canonical "investigate immediately" pattern referenced in `root_cause_analysis_playbook.md`.

## 12. Guidance for AI Business Analysts

When interpreting transaction-level Discount data, an AI analyst should:

1. Always compute **aggregate** Profit Margin as `SUM(Profit)/SUM(Sales)` for the group under review — never average the row-level `profit_margin` field to represent a group (see `business_kpi_definitions.md`).
2. Segment any discount analysis by Category/Sub-Category before drawing conclusions, since Furniture, Technology, and Office Supplies behave very differently.
3. Treat a high Discount value on its own as a **fact**, but treat "this discount was a deliberate strategic decision" as an **inference** unless corroborated by other evidence (see `business_analysis_governance.md`).
4. Never assume a causal link between rising Discount and rising Sales without checking whether Quantity or order count actually moved with it.

---

### Document Scope

**This document can establish:** Meridian's fictional discount governance framework, discount tiers and approval authority, and the general (data-supported) relationship between discount depth and realized Profit Margin observed in the transaction dataset.

**This document cannot establish:** why any specific discount was actually granted, whether a specific discounting decision was strategic or erroneous, or competitive/market conditions that may have motivated real-world discounting. These require either additional business context outside the dataset or explicit human confirmation.
