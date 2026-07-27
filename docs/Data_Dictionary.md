# N100 Financial Intelligence Platform

# Data Dictionary

Version: 1.0.0

---

# Table of Contents

1. Overview
2. Dataset Summary
3. Original Dataset Attributes
4. Engineered Features
5. Financial Health Score Attributes
6. Ranking Attributes
7. Data Types
8. Missing Value Strategy
9. Data Sources
10. Summary

---

# 1. Overview

This document describes the datasets, variables, engineered features, and financial indicators used throughout the **N100 Financial Intelligence Platform**.

The purpose of this data dictionary is to provide a clear understanding of every important field used during:

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Financial Health Score Calculation
- Company Ranking
- Dashboard Visualization

---

# 2. Dataset Summary

| Attribute | Description |
|------------|-------------|
| Dataset Name | N100 Financial Dataset |
| Coverage | Companies listed in the Nifty 100 Index |
| Data Format | CSV |
| Processed Output | `master_features.csv` |
| Database | SQLite |
| Primary Usage | Financial Analytics & Dashboard |

---

# 3. Original Dataset Attributes

## Company Information

| Column | Data Type | Description | Example |
|---------|-----------|-------------|---------|
| Company | String | Name of the company | Reliance Industries Ltd. |
| Symbol | String | Stock ticker symbol | RELIANCE |
| Sector | String | Business sector | Energy |
| Industry | String | Industry classification | Oil & Gas |
| MarketCap | Float | Market capitalization | 2450000 |
| CurrentPrice | Float | Latest market price | 2850.75 |

---

## Profitability Metrics

| Column | Data Type | Description | Example |
|---------|-----------|-------------|---------|
| ROE | Float | Return on Equity (%) | 18.75 |
| ROCE | Float | Return on Capital Employed (%) | 21.60 |
| ProfitMargin | Float | Net Profit Margin (%) | 15.40 |
| OperatingMargin | Float | Operating Margin (%) | 19.10 |
| EPS | Float | Earnings Per Share | 96.42 |

---

## Debt & Stability Metrics

| Column | Data Type | Description | Example |
|---------|-----------|-------------|---------|
| DebtToEquity | Float | Debt to Equity Ratio | 0.42 |
| CurrentRatio | Float | Current Assets / Current Liabilities | 1.85 |
| InterestCoverage | Float | Ability to pay interest obligations | 12.40 |

---

## Cash Flow Metrics

| Column | Data Type | Description | Example |
|---------|-----------|-------------|---------|
| OperatingCashFlow | Float | Cash generated from operations | 52000 |
| FreeCashFlow | Float | Cash available after capital expenditure | 32000 |
| CashFlowGrowth | Float | Growth in cash flow (%) | 9.50 |

---

## Valuation Metrics

| Column | Data Type | Description | Example |
|---------|-----------|-------------|---------|
| PE | Float | Price-to-Earnings Ratio | 24.15 |
| PB | Float | Price-to-Book Ratio | 3.85 |
| EVEBITDA | Float | Enterprise Value / EBITDA | 16.30 |
| DividendYield | Float | Dividend Yield (%) | 1.40 |

---

# 4. Engineered Features

The following variables were created during the Feature Engineering phase.

---

## Profitability Features

| Feature | Description |
|----------|-------------|
| ProfitabilityScore | Composite profitability score |
| ROEScore | Numerical score based on ROE |
| ROEGrade | Grade assigned from ROE performance |
| ProfitMarginCategory | Profitability category |

Example Categories

- Excellent
- Good
- Average
- Weak

---

## Debt Features

| Feature | Description |
|----------|-------------|
| DebtScore | Debt quality score |
| DebtRisk | Debt risk category |
| SafeDebt | Indicates financially safe debt level |

Debt Risk Categories

- Low
- Moderate
- High

---

## Cash Flow Features

| Feature | Description |
|----------|-------------|
| PositiveCashFlow | Indicates positive operating cash flow |
| CashFlowCategory | Cash flow classification |

Categories

- Strong
- Stable
- Weak

---

## Dividend Features

| Feature | Description |
|----------|-------------|
| DividendCompany | Indicates whether company pays dividends |
| DividendCategory | Dividend classification |

Categories

- High Dividend
- Moderate Dividend
- Low Dividend
- No Dividend

---

## Market Features

| Feature | Description |
|----------|-------------|
| ValueScore | Valuation score |
| PECategory | Price-to-Earnings category |
| PBCategory | Price-to-Book category |

PE Categories

- Undervalued
- Fairly Valued
- Overvalued

PB Categories

- Low
- Medium
- High

---

## Financial Strength Features

| Feature | Description |
|----------|-------------|
| FinancialStrengthScore | Composite financial stability score |

---

## Sector Features

| Feature | Description |
|----------|-------------|
| SectorCode | Encoded sector identifier |
| SectorRank | Rank within sector |

---

# 5. Financial Health Score Attributes

The Financial Health Score combines multiple financial dimensions into a single evaluation metric.

| Feature | Description |
|----------|-------------|
| FinancialHealthScore | Overall financial strength score |
| Rating | Company rating |
| OverallRank | Rank among all companies |
| SectorRankFinal | Final rank within sector |

Rating Categories

| Rating | Meaning |
|----------|---------|
| AAA | Exceptional Financial Strength |
| AA | Very Strong |
| A | Strong |
| BBB | Stable |
| BB | Moderate |
| B | Weak |

---

# 6. Ranking Attributes

| Feature | Description |
|----------|-------------|
| OverallRank | Overall ranking among companies |
| SectorRank | Ranking within sector |
| FinancialHealthScore | Basis for ranking |
| Rating | Financial performance grade |

---

# 7. Data Types

| Data Type | Usage |
|------------|------|
| String | Company names, sectors, ratings |
| Integer | Rankings, encoded values |
| Float | Financial ratios, market metrics |
| Boolean | Flags and indicators |
| Category | Performance classifications |

---

# 8. Missing Value Strategy

The following preprocessing techniques were applied:

- Missing value identification
- Missing value treatment
- Duplicate removal
- Data type standardization
- Validation of required columns
- Consistency checks
- Feature validation

The processed dataset used by the dashboard contains validated and cleaned records suitable for analysis.

---

# 9. Data Sources

The platform integrates financial information related to:

- Company Information
- Financial Ratios
- Profitability Metrics
- Cash Flow Metrics
- Valuation Metrics
- Market Capitalization
- Sector Information
- Company Rankings

The processed output is stored as:

```
master_features.csv
```

and is used throughout the analytics pipeline and Streamlit dashboard.

---

# 10. Summary

The N100 Financial Intelligence Platform transforms raw financial information into a comprehensive analytical dataset through data cleaning, preprocessing, and feature engineering.

The resulting dataset combines original financial variables with engineered indicators, Financial Health Scores, company rankings, and sector-based insights. This standardized structure enables efficient financial analysis, investment screening, portfolio evaluation, and interactive business intelligence through the Streamlit dashboard.