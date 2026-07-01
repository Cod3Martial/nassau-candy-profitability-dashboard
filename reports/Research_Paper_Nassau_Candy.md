# Product Line Profitability & Margin Performance Analysis
## Nassau Candy Distributor — FY 2025

**Prepared by:** Data Science & Analytics Team  
**Submission Date:** 2025  
**Dataset:** Nassau_Candy_Distributor.csv (10,194 order records)  
**Analysis Period:** January 2025 – December 2025  

---

## Abstract

This paper presents a comprehensive product-line profitability analysis for Nassau Candy Distributor, a multi-division candy distribution company operating across the United States. Using a dataset of 10,194 transactions spanning three product divisions (Chocolate, Sugar, and Other), we apply gross margin analysis, Pareto concentration modelling, and cost-structure diagnostics to surface actionable insights about where the company earns money, where it loses efficiency, and which products demand immediate strategic attention. Key findings reveal that the Chocolate division alone generates 95.1% of total gross profit at a 67.5% average margin, while the Other division houses a critical cost-risk product (Kazookles, 92.3% cost ratio) that actively erodes overall profitability. This paper concludes with a prioritised set of strategic recommendations for pricing, product rationalisation, and portfolio management.

---

## 1. Introduction

### 1.1 Background

Nassau Candy Distributor operates across three product divisions — Chocolate, Sugar, and Other — distributing a portfolio of 15 branded candy products manufactured across five US factories. As a distributor operating in a competitive consumer goods market, the company's financial health depends not merely on sales volume, but on the *quality* of that revenue as expressed through gross margin.

Sales volume is frequently a misleading measure of business health. A product can generate significant revenue while contributing negligible — or even negative — profit if its cost structure is misaligned with its pricing. For distributors operating across a broad product portfolio, high-volume products with thin margins can actually weaken overall business performance by consuming operational resources, warehouse capacity, and sales effort that could be redirected to high-margin products.

This study was commissioned to address precisely this risk: to transform raw transaction data into a clear, evidence-based picture of which products drive profitability, which divisions are financially efficient, and where Nassau Candy should focus its pricing, sourcing, and product portfolio strategy.

### 1.2 Problem Statement

Prior to this analysis, Nassau Candy lacked visibility into:

- Which product lines deliver the highest gross margin percentage
- Whether high-sales-volume products are genuinely profitable
- How profitability and cost efficiency vary across product divisions
- Which individual products represent margin risk requiring immediate intervention

Without this intelligence, decisions on pricing adjustments, promotional investment, supplier renegotiation, and product discontinuation were reactive and intuition-based, rather than data-driven.

### 1.3 Objectives

This analysis pursues four primary objectives:

1. Calculate and compare product-level and division-level gross margin performance
2. Identify high-profit, high-margin products and margin-risk products
3. Apply Pareto analysis to quantify profit concentration risk
4. Provide actionable, prioritised recommendations for portfolio optimisation

---

## 2. Dataset Description

### 2.1 Source & Scope

The dataset comprises **10,194 order rows** from Nassau Candy Distributor's internal order management system, covering the full fiscal year 2025 (January 1 – December 31, 2025). Each row represents a single product order-line associated with a customer, geographic location, shipping method, and financial attributes.

### 2.2 Field Definitions

| Field | Type | Description |
|---|---|---|
| Row ID | Integer | Unique row identifier |
| Order ID | String | Unique order identifier |
| Order Date | Date | Date the order was placed |
| Ship Date | Date | Date the order was shipped |
| Ship Mode | Categorical | Shipping method (e.g. Standard Class) |
| Customer ID | Integer | Unique customer identifier |
| Country/Region | String | Country of customer |
| City | String | City of customer |
| State/Province | String | State of customer |
| Postal Code | Integer | Zip code |
| Division | Categorical | Product division (Chocolate / Sugar / Other) |
| Region | Categorical | Sales region (Atlantic / Gulf / Interior / Pacific) |
| Product ID | String | Unique product identifier |
| Product Name | String | Full product name |
| Sales | Float | Total sales value (revenue) |
| Units | Integer | Total units sold |
| Gross Profit | Float | Gross profit (Sales − Cost) |
| Cost | Float | Cost of goods |

### 2.3 Factory & Division Mapping

| Division | Product | Factory |
|---|---|---|
| Chocolate | Wonka Bar - Nutty Crunch Surprise | Lot's O' Nuts (AZ) |
| Chocolate | Wonka Bar - Fudge Mallows | Lot's O' Nuts (AZ) |
| Chocolate | Wonka Bar - Scrumdiddlyumptious | Lot's O' Nuts (AZ) |
| Chocolate | Wonka Bar - Milk Chocolate | Wicked Choccy's (GA) |
| Chocolate | Wonka Bar - Triple Dazzle Caramel | Wicked Choccy's (GA) |
| Sugar | Laffy Taffy, SweeTARTS, Nerds, Fun Dip | Sugar Shack (MN) |
| Sugar | Everlasting Gobstopper | Secret Factory (IL) |
| Sugar | Hair Toffee | The Other Factory (TN) |
| Other | Fizzy Lifting Drinks | Sugar Shack (MN) |
| Other | Lickable Wallpaper, Wonka Gum | Secret Factory (IL) |
| Other | Kazookles | The Other Factory (TN) |

---

## 3. Methodology

### 3.1 Data Cleaning & Validation

The following preprocessing steps were applied:

**Date parsing:** Order Date and Ship Date were parsed from string format (`DD-MM-YYYY`) to proper datetime objects to enable temporal analysis.

**Whitespace standardisation:** Product names were stripped of leading/trailing whitespace. A typographical error in the original data (`"Wonka Bar -Scrumdiddlyumptious"`) was identified and corrected.

**Financial integrity check:** All rows were validated against the accounting identity: `Sales = Cost + Gross Profit`. Rows deviating by more than $0.01 were flagged for review. No integrity violations were found in the final dataset.

**Zero-sales filtering:** Rows with zero or negative sales values were excluded from analysis. No such rows were present in the dataset.

**Result:** The dataset required minimal cleaning. Zero missing values were detected across all 18 columns, indicating a high-quality, well-maintained source system.

### 3.2 KPI Calculation

The following key performance indicators were computed at the transaction level and then aggregated to product and division levels:

| KPI | Formula |
|---|---|
| Gross Margin (%) | Gross Profit ÷ Sales × 100 |
| Profit per Unit | Gross Profit ÷ Units |
| Revenue per Unit | Sales ÷ Units |
| Cost Ratio (%) | Cost ÷ Sales × 100 |
| Revenue Contribution (%) | Product Sales ÷ Total Sales × 100 |
| Profit Contribution (%) | Product Profit ÷ Total Profit × 100 |
| Cumulative Profit (%) | Running sum of Profit Contribution (%) |

### 3.3 Analytical Framework

The analysis follows five methodological stages:

1. **Descriptive profiling** — Summary statistics across all products and divisions
2. **Ranked product analysis** — League tables by gross profit, gross margin, and profit per unit
3. **Division-level aggregation** — Comparing revenue efficiency across the three divisions
4. **Pareto concentration analysis** — Determining what share of products generates 80% of profits
5. **Cost structure diagnostics** — Identifying products with dangerously high cost-to-revenue ratios

---

## 4. Exploratory Data Analysis & Findings

### 4.1 Overall Business KPIs

| KPI | FY 2025 Value |
|---|---|
| Total Revenue | $141,783.63 |
| Total Gross Profit | $93,442.80 |
| Overall Gross Margin | 66.5% |
| Total Units Sold | 38,654 |
| Total Orders | 8,549 |

The 66.5% overall gross margin is exceptionally strong for a distributor, driven heavily by the Chocolate division's high-margin Wonka Bar product line.

### 4.2 Product-Level Profitability

#### Top Performers by Gross Profit

| Rank | Product | Division | Revenue | Gross Profit | Avg Margin |
|---|---|---|---|---|---|
| 1 | Wonka Bar - Scrumdiddlyumptious | Chocolate | $27,874 | $19,358 | 69.4% |
| 2 | Wonka Bar - Triple Dazzle Caramel | Chocolate | $28,485 | $18,610 | 65.3% |
| 3 | Wonka Bar - Milk Chocolate | Chocolate | $26,868 | $17,443 | 64.9% |
| 4 | Wonka Bar - Nutty Crunch Surprise | Chocolate | $23,575 | $16,820 | 71.3% |
| 5 | Wonka Bar - Fudge Mallows | Chocolate | $24,890 | $16,594 | 66.7% |

All five top-performing products by gross profit are Chocolate division products. Together, they account for **$88,825** in gross profit — **95.1%** of total company profit — from **$131,693** in revenue (92.9% of total revenue).

#### Highest Margin Products

| Product | Division | Avg Gross Margin |
|---|---|---|
| Everlasting Gobstopper | Sugar | 80.0% |
| Hair Toffee | Sugar | 77.8% |
| Wonka Bar - Nutty Crunch Surprise | Chocolate | 71.3% |
| Wonka Bar - Scrumdiddlyumptious | Chocolate | 69.4% |
| Wonka Bar - Fudge Mallows | Chocolate | 66.7% |

Notably, Everlasting Gobstopper and Hair Toffee (Sugar division) post the highest margin percentages but extremely low total sales volumes ($130 and $76.50 respectively), indicating they are high-quality niche products with negligible scale.

#### Margin Risk Products (Cost Ratio > 60%)

| Product | Division | Cost Ratio | Avg Margin | Revenue |
|---|---|---|---|---|
| Kazookles | Other | **92.3%** | **7.7%** | $1,206 |
| Fun Dip | Sugar | 60.0% | 40.0% | $12 |
| SweeTARTS | Sugar | 53.3% | 46.7% | $62 |
| Nerds | Sugar | 53.3% | 46.7% | $15 |

**Kazookles** is the most critical margin risk in the portfolio. At a 92.3% cost ratio, it generates only $0.077 profit for every dollar of revenue — a near-zero margin product that nonetheless consumes distribution, storage, and sales resources.

### 4.3 Division Performance

| Division | Revenue | Gross Profit | Rev Share | Profit Share | Avg Margin |
|---|---|---|---|---|---|
| Chocolate | $131,693 | $88,825 | 92.9% | 95.1% | 67.5% |
| Other | $9,663 | $4,333 | 6.8% | 4.6% | 37.7% |
| Sugar | $427 | $285 | 0.3% | 0.3% | 57.7% |

**Key insight:** The Chocolate division dominates by every metric. The Other division contributes 6.8% of revenue but only 4.6% of profit — a sign of margin inefficiency. The Sugar division is commercially negligible at this time, contributing just $427 in revenue across the full year.

### 4.4 Pareto Analysis — Profit Concentration

| Products | % of SKUs | Cumulative Profit % |
|---|---|---|
| Top 1 (Scrumdiddlyumptious) | 6.7% | 20.7% |
| Top 2 | 13.3% | 40.6% |
| Top 3 | 20.0% | 59.3% |
| Top 4 | 26.7% | 77.3% |
| Top 5 | 33.3% | **95.1%** |

The Pareto analysis reveals a highly concentrated profit structure. Just **5 products** (33% of SKUs) generate **95.1% of total gross profit**. This exceeds the classic 80/20 rule — it is effectively a 95/33 concentration. This extreme concentration carries significant business risk: disruption to any one Chocolate product (supply chain, regulatory, or demand shock) would have a disproportionate impact on profitability.

### 4.5 Regional Analysis

| Region | Revenue | Gross Profit | Avg Margin |
|---|---|---|---|
| Pacific | $46,302 | $30,486 | 65.8% |
| Atlantic | $41,197 | $26,974 | 65.5% |
| Interior | $32,038 | $21,282 | 66.4% |
| Gulf | $22,247 | $14,701 | 66.1% |

Regional margins are remarkably consistent (65.5%–66.4%), suggesting that pricing and product mix are stable across geographies. The Pacific region leads in absolute revenue and profit, while the Gulf region is the smallest. No region shows signs of structural underperformance.

### 4.6 Temporal Trends

Monthly analysis shows that Chocolate division margins are highly stable throughout 2025 (~66–68% each month), confirming the reliability and predictability of that product line's financial performance. The Other division shows higher volatility month-to-month (26%–42%), indicating inconsistent demand or pricing for products like Kazookles, Wonka Gum, and Lickable Wallpaper.

---

## 5. Strategic Recommendations

### Recommendation 1 — Protect & Invest in the Chocolate Division (PRIORITY: HIGH)

The Chocolate division is Nassau Candy's financial engine. All five Wonka Bar variants deliver 65%+ margins and together represent $88,825 in annual profit. The company should:

- Prioritise Chocolate inventory availability and supply chain reliability above all other divisions
- Explore volume expansion opportunities (new customers, new regions) for Wonka Bar variants
- Consider negotiating volume-based discounts with Lot's O' Nuts and Wicked Choccy's factories to further reduce cost ratios

### Recommendation 2 — Discontinue or Reprice Kazookles (PRIORITY: CRITICAL)

Kazookles (Other division, manufactured by The Other Factory) is generating a 92.3% cost ratio and 7.7% gross margin. At $1,206 annual revenue, this product is not commercially viable in its current form. Recommended actions:

- **Option A:** Discontinue Kazookles from the portfolio immediately. The freed operational capacity can be redirected to Chocolate products.
- **Option B:** Renegotiate sourcing costs with The Other Factory to achieve at minimum a 50% cost ratio (doubling current margin to ~15%+), with a target of 40% cost ratio.
- **Option C:** Increase retail price by 50–80% to achieve a commercially acceptable margin, with customer retention impact analysis.

### Recommendation 3 — Develop the Sugar Division (PRIORITY: MEDIUM)

Several Sugar products (Everlasting Gobstopper at 80%, Hair Toffee at 77.8%) have outstanding margin profiles but negligible sales volumes. The company should investigate why these products are underperforming commercially despite their attractive unit economics:

- Are these products actively marketed and available to all customers?
- Is distribution coverage adequate for Sugar SKUs?
- Could promotional bundles with Chocolate products drive Sugar volume?

### Recommendation 4 — Reduce Portfolio Concentration Risk (PRIORITY: MEDIUM)

The 95/33 profit concentration is a strategic vulnerability. If any Wonka Bar variant encounters supply disruption, demand decline, or regulatory challenge, the company faces a material profit reduction. Recommended mitigations:

- Actively grow Lickable Wallpaper (Other division, 50% margin, $3,930 profit) — the best-performing non-Chocolate product
- Set a 5-year target to reduce the top-5-product profit concentration from 95% to below 80%
- Consider introducing new product lines or brands in the Sugar and Other divisions

### Recommendation 5 — Standardise Pricing in the Other Division (PRIORITY: MEDIUM)

The Other division's high margin volatility (26%–42% monthly swings) suggests ad hoc or inconsistent pricing practices. A structured pricing review should establish minimum gross margin floors:

- Floor: 40% gross margin for all active products
- Review and reprice any SKU falling below this threshold in two consecutive quarters

---

## 6. Conclusion

This analysis establishes a clear, quantitative view of profitability across Nassau Candy Distributor's product portfolio. The central finding is that the business is extremely profitable where it focuses — the Chocolate division's Wonka Bar range delivers a 67.5% average gross margin and drives 95.1% of total profit — but carries meaningful risk due to this concentration, and is burdened by a critically underperforming product (Kazookles) that should be prioritised for immediate remediation.

The data supports three key strategic conclusions:

1. **Double down on Chocolate.** It is the company's structural advantage and must be protected and grown.
2. **Cut Kazookles.** A 7.7% margin product has no place in a portfolio averaging 66.5%.
3. **Build Sugar.** The margin potential is proven; the commercial execution is not yet there.

By acting on these recommendations, Nassau Candy Distributor can improve its already strong gross margins, reduce concentration risk, and build a more resilient, diversified revenue base.

---

## Appendix A — Gross Margin by Product (Full Table)

| Product | Division | Revenue | Gross Profit | Avg Margin | Cost Ratio |
|---|---|---|---|---|---|
| Wonka Bar - Scrumdiddlyumptious | Chocolate | $27,875 | $19,358 | 69.4% | 30.6% |
| Wonka Bar - Triple Dazzle Caramel | Chocolate | $28,485 | $18,610 | 65.3% | 34.7% |
| Wonka Bar - Milk Chocolate | Chocolate | $26,868 | $17,443 | 64.9% | 35.1% |
| Wonka Bar - Nutty Crunch Surprise | Chocolate | $23,575 | $16,820 | 71.3% | 28.7% |
| Wonka Bar - Fudge Mallows | Chocolate | $24,890 | $16,594 | 66.7% | 33.3% |
| Lickable Wallpaper | Other | $7,860 | $3,930 | 50.0% | 50.0% |
| Wonka Gum | Other | $598 | $311 | 52.0% | 48.0% |
| Everlasting Gobstopper | Sugar | $130 | $104 | 80.0% | 20.0% |
| Kazookles | Other | $1,206 | $93 | 7.7% | 92.3% |
| Hair Toffee | Sugar | $77 | $60 | 77.8% | 22.2% |
| Fizzy Lifting Drinks | Sugar | $79 | $47 | 60.0% | 40.0% |
| Laffy Taffy | Sugar | $54 | $33 | 62.3% | 37.7% |
| SweeTARTS | Sugar | $62 | $29 | 46.7% | 53.3% |
| Nerds | Sugar | $15 | $7 | 46.7% | 53.3% |
| Fun Dip | Sugar | $12 | $5 | 40.0% | 60.0% |

---

## Appendix B — Factory Location Reference

| Factory | State | Latitude | Longitude |
|---|---|---|---|
| Lot's O' Nuts | Arizona | 32.882 | -111.768 |
| Wicked Choccy's | Georgia | 32.076 | -81.088 |
| Sugar Shack | Minnesota | 48.119 | -96.181 |
| Secret Factory | Illinois | 41.446 | -90.565 |
| The Other Factory | Tennessee | 35.118 | -89.971 |

---

*Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis | FY 2025*  
*Prepared by: Data Science & Analytics Team*
