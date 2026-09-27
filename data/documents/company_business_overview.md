# Meridian Global Retail Group — Company Business Overview

**Document Type:** Internal Corporate Business Overview
**Version:** 1.0
**Status:** Project-specific demo documentation
**Data Source:** Derived from the uploaded Global Superstore-style transaction dataset (`superstore_cleaned.csv`)
**Disclaimer:** Meridian Global Retail Group ("Meridian," "the Company," "MGRG") is a **fictional company** created solely for this AI/ML portfolio project. This document is project-specific business documentation derived from the uploaded Global Superstore-style transaction dataset and is **not an official document from the original dataset provider**. All policies, figures, and business facts described here are demo content designed to be internally consistent with the uploaded transaction data.

---

## 1. Company Identity

Meridian Global Retail Group is a mid-to-large multinational retailer and business-to-business distributor of office supplies, furniture, and technology products. Meridian operates a hybrid catalog / direct-sales / e-commerce model, selling to individual consumers as well as corporate and home-office buyers across a global footprint.

Meridian's positioning is best summarized internally as: *"Everything a workplace needs, delivered anywhere in the world."*

The Company's transaction systems record every order at the line-item level, which is the basis of the `Row ID`-level transaction dataset referenced throughout this documentation set (see `business_data_dictionary.md`).

## 2. Business Model

Meridian generates revenue by selling physical products across three **Categories**:

- **Technology** — phones, copiers, machines, accessories
- **Office Supplies** — paper, art, storage, appliances, supplies, envelopes, fasteners, labels, binders
- **Furniture** — chairs, bookcases, tables, furnishings

These three Categories are subdivided into **Sub-Categories** (17 in total across the Company's catalog: Paper, Art, Storage, Appliances, Supplies, Envelopes, Fasteners, Labels, Binders, Accessories, Phones, Copiers, Machines, Tables, Bookcases, Chairs, Furnishings). Each Sub-Category is managed by a dedicated Category Manager who owns pricing, vendor relationships, and Sub-Category-level profitability.

Meridian's revenue model is transaction-based: revenue ("Sales") is recognized per order line at the point of sale, and Cost of Goods, fulfillment cost, and applied discount jointly determine the "Profit" realized on that line. This is why Sales and Profit must always be analyzed together rather than in isolation — a topic developed further in `business_kpi_definitions.md`.

## 3. Geographic Footprint

Meridian organizes its commercial footprint using two complementary geographic hierarchies:

- **Market** — the top-level commercial grouping used for executive reporting: `US`, `EU`, `LATAM`, `Africa`, `APAC`, `EMEA`, `Canada`.
- **Market 2** — a consolidated regional grouping used for finance and supply-chain reporting: `North America`, `EU`, `LATAM`, `Africa`, `APAC`, `EMEA`. (Note: in the Market 2 hierarchy, the `US` and `Canada` Markets both roll up into `North America`.)
- **Region** — a finer-grained operational grouping used by fulfillment and sales operations: `West`, `East`, `South`, `Central`, `North`, `Canada` (North America); `EMEA`; `Africa`; `Oceania`, `Southeast Asia`, `North Asia`, `Central Asia` (APAC); and `Caribbean` (LATAM).
- **Country / State / City** — the granular geography used for shipping, tax, and last-mile logistics. Meridian ships to 147 distinct countries recorded in the transaction system, with the United States representing the single largest country by transaction volume.

This multi-level geography allows the same transaction to be rolled up ("Which Market performed best?") or drilled down ("Which city in Southeast Asia drove the decline?") depending on the audience.

## 4. Customer Segments

Meridian sells into three customer **Segments**, each with a distinct purchasing profile:

| Segment | Description | Typical Purchasing Pattern |
|---|---|---|
| **Consumer** | Individual buyers purchasing for personal or home use | Highest order count, smaller basket sizes, price-sensitive |
| **Corporate** | Registered business accounts, mid-size and large companies | Recurring bulk orders, negotiated account terms |
| **Home Office** | Small-business and remote-worker buyers | Blend of Consumer and Corporate behavior; smaller but more frequent Technology purchases |

Consumer is Meridian's largest Segment by both order volume and total Sales, followed by Corporate and then Home Office. Segment-specific strategy, retention, and discount-behavior guidance is detailed in `customer_segmentation_strategy.md`.

## 5. Sales Channels and Order Structure

Meridian records each customer purchase as an **Order** (`Order ID`), which may contain one or more **line items** (`Row ID`). A single Order can therefore span multiple products, Categories, and even different discount levels, because customers frequently combine, for example, a Technology purchase with Office Supplies in the same checkout. Analysts must never assume that `Order ID` uniquely identifies one product line — see `business_data_dictionary.md` for the precise distinction between `Order ID` and `Row ID`.

Meridian does not currently distinguish between "online" and "in-store" channel in the transaction data; the dataset represents Meridian's consolidated direct-sales and e-commerce order stream, which analysts should treat as the single system of record for revenue and fulfillment.

## 6. Operational and Shipping Model

Meridian fulfills orders through a global logistics network using four **Ship Modes**:

- **Same Day**
- **First Class**
- **Second Class**
- **Standard Class**

Each Order also carries an **Order Priority** flag — `Critical`, `High`, `Medium`, or `Low` — set by the fulfillment and customer-service teams based on customer commitments and account tier. Ship Mode and Order Priority are related but distinct concepts: Order Priority reflects the customer's service commitment, while Ship Mode reflects the actual carrier service selected to fulfill that commitment. Full operational detail is in `shipping_fulfillment_policy.md`.

## 7. Revenue, Discounting, and Profitability Interaction

Four transaction-level fields drive Meridian's economics on every order line:

1. **Sales** — the invoiced revenue for the line item.
2. **Discount** — the proportion of list price removed as a promotional or negotiated reduction.
3. **Shipping Cost** — the logistics cost incurred to fulfill the line item.
4. **Profit** — the net financial contribution after cost of goods, discount, and associated costs.

These four fields interact continuously: a higher Discount reduces effective revenue per unit, which — if not offset by higher Quantity or lower cost — reduces Profit and compresses Profit Margin. Elevated Shipping Cost (driven by faster Ship Modes, longer distances, or heavier/bulkier Categories such as Furniture) further reduces the Profit retained from a given Sales amount. Meridian's finance and commercial teams treat Sales, Discount, Shipping Cost, and Profit as **jointly determined outcomes** of a single order decision, not as independent metrics — a principle used throughout the diagnostic playbooks in `root_cause_analysis_playbook.md`.

## 8. High-Level Business Objectives

Meridian's stated internal objectives, used to frame quarterly business reviews, are:

- **Grow Sales** across all Markets while protecting overall Profit Margin.
- **Maintain a healthy discounting discipline** so that promotional activity does not erode Category-level profitability (see `pricing_discount_policy.md`).
- **Optimize the Ship Mode mix** to balance customer service commitments (Order Priority) against Shipping Cost (see `shipping_fulfillment_policy.md`).
- **Grow high-value customer relationships** in the Corporate and Home Office Segments while monitoring customer concentration risk (see `customer_segmentation_strategy.md`).
- **Manage the product portfolio** so that high-Sales products are also acceptable-Profit products, retiring or repricing chronic underperformers (see `product_category_management.md`).

## 9. Major Business Functions

- **Commercial / Sales** — owns Segment strategy, account management, and discount negotiation.
- **Category Management** — owns Category and Sub-Category assortment, vendor pricing, and product-level profitability.
- **Pricing & Revenue Management** — owns discount governance and margin protection (see `pricing_discount_policy.md`).
- **Logistics & Fulfillment** — owns Ship Mode selection, carrier relationships, and Shipping Cost management.
- **Finance / FP&A** — owns KPI definitions, Profit Margin reporting, and quarterly business review analysis.
- **Business Intelligence / Data & Analytics** — owns the transaction data warehouse (the system that produces the dataset referenced throughout this documentation set) and increasingly, the AI-assisted business analysis system this documentation set supports.

## 10. Organizational Terminology Glossary (Quick Reference)

| Term | Meaning at Meridian |
|---|---|
| Market | Top-level commercial geography (US, EU, LATAM, Africa, APAC, EMEA, Canada) |
| Market 2 | Consolidated regional geography used in finance reporting |
| Region | Operational sales/fulfillment geography, finer than Market |
| Segment | Customer type: Consumer, Corporate, Home Office |
| Category | Top-level product grouping: Technology, Office Supplies, Furniture |
| Sub-Category | Detailed product grouping within a Category |
| Ship Mode | Carrier service level used to fulfill an order line |
| Order Priority | Customer service commitment level assigned to an order |
| Line item | A single product row within an Order, identified by Row ID |

This glossary is expanded with full field-level detail in `business_data_dictionary.md`.

---

### Document Scope

**This document can establish:** Meridian's fictional business model, organizational structure, terminology, geographic and product hierarchies, and how core business fields conceptually relate to one another, consistent with the structure of the uploaded transaction dataset.

**This document cannot establish:** actual historical performance figures, the cause of any specific sales or profit movement, competitor behavior, marketing activity, or any fact not derivable from the transaction dataset. Quantitative claims about specific periods, regions, or products must be validated against SQL analysis of the transaction data, not inferred from this document alone.
