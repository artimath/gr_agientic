# Funnel Economics Calculator

This tool allows you to model and analyze the economics of a sales funnel with the following structure:

**Video Ad → Checkout/Sales Page → Upsell 1 (Community)**

## Key Metrics Modeled

The calculator models all critical funnel metrics including:

- **Traffic Metrics**: Ad spend, CPC, clicks, CTR
- **Conversion Metrics**: Landing page CVR, checkout CVR, upsell take rate
- **Revenue Metrics**: AOV, main offer revenue, upsell revenue
- **Cost Metrics**: CPA, COGS, fulfillment costs
- **Profit Metrics**: ROI, ROAS, profit margin

## Getting Started

### Prerequisites

The tool requires Python 3.6+ and the following packages:
- pandas
- numpy
- matplotlib
- seaborn

Install dependencies with:

```bash
pip install pandas numpy matplotlib seaborn
```

### Running the Calculator

Two ways to use the calculator:

1. **Interactive Mode** (Recommended for first-time users):
   ```bash
   python interactive_funnel.py
   ```
   This will prompt you for inputs and guide you through the analysis.

2. **Direct Script Mode**:
   ```bash
   python funnel_economics.py
   ```
   This runs with default values which you can modify in the script.

## Features

### 1. Basic Funnel Economics

The calculator provides a comprehensive analysis of your funnel including:
- Daily and total metrics across the entire funnel
- Conversion rates between each funnel step
- Revenue, cost, and profit calculations

### 2. Breakeven Analysis

Finds combinations of conversion rates that achieve your target ROI, helping you understand:
- What conversion rates you need to be profitable
- Trade-offs between different metrics (e.g., lower landing page CVR with higher checkout CVR)

### 3. Sensitivity Analysis

Shows how changes in key metrics affect your ROI and profit, helping you:
- Identify which metrics have the biggest impact on profitability
- Determine where to focus optimization efforts
- Understand risks in your funnel model

### 4. Visualization

Generates visualizations including:
- Funnel visualization showing drop-off at each step
- Revenue breakdown between main offer and upsell
- Profit over time projections
- Critical customer metrics (CPA, AOV)

## Modifying Default Values

For the direct script mode, you can modify default parameters in the `funnel_economics.py` file:

```python
funnel_df, summary = calculate_funnel_economics(
    daily_ad_spend=1000,  # Your daily ad budget
    avg_cpc=1.5,          # Average cost per click
    lp_cvr=0.03,          # Landing page conversion rate (3%)
    checkout_cvr=0.20,    # Checkout page conversion rate (20%)
    # ... other parameters
)
```

## Interpreting Results

The most important metrics to focus on:

1. **ROI (Return on Investment)**: Should be positive for a profitable funnel
2. **ROAS (Return on Ad Spend)**: Should be >1 to be profitable 
3. **CPA (Cost Per Acquisition)**: Should be less than your AOV
4. **Breakeven Analysis**: Shows minimum conversion rates needed
5. **Sensitivity Analysis**: Shows which metrics to optimize first

## Example Use Cases

1. **Validating a Funnel Concept**: Test if your pricing and conversion assumptions yield a profitable funnel
2. **Funnel Optimization**: Identify which metrics need improvement to reach target profitability
3. **Budget Planning**: Determine how changes in ad spend affect overall profit
4. **Pricing Strategy**: Test different price points to maximize profit 