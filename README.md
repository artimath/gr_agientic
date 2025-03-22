# Funnel Economics Modeling Suite

A comprehensive suite of tools for modeling and analyzing the economics of a sales funnel with the following structure:

**Video Ad → Checkout/Sales Page → Upsell 1 (Community)**

## Quick Start

1. **Install requirements:**
   ```bash
   pip install -r models/requirements.txt
   ```

2. **Run the main interface:**
   ```bash
   cd models
   python main.py
   ```

## Available Tools

### 1. Quick Breakeven Calculator
Instantly calculate the conversion rates needed to achieve profitability, based on your ad costs, pricing, and target ROI.

```bash
python models/breakeven_calculator.py
```

### 2. Interactive Funnel Calculator
A comprehensive tool that lets you model your entire funnel with customizable parameters.

```bash
python models/interactive_funnel.py
```

### 3. Full Funnel Analysis with Visualizations
Generate detailed visualizations and sensitivity analysis of your funnel performance.

```bash
python models/funnel_economics.py
```

### 4. Example Scenarios
View example funnel scenarios with realistic metrics.

```bash
python models/example_scenario.py
```

## Key Metrics Modeled

The suite models all critical metrics for your funnel:

- **Traffic Metrics**: Ad spend, CPC, CTR, clicks
- **Conversion Metrics**: Landing page CVR, checkout CVR, upsell take rate
- **Revenue Metrics**: AOV, main offer revenue, upsell revenue
- **Cost Metrics**: CPA, COGS, fulfillment costs
- **Profit Metrics**: ROI, ROAS, profit margin

## Understanding Your Funnel Economics

For your Video Ad → Checkout/Sales Page → Upsell funnel, these are the key metrics to focus on:

1. **Ad Metrics:**
   - CPC (Cost Per Click) - Typically $1-3 for video ads
   - CTR (Click-Through Rate) - 1-5% is common for video ads

2. **Conversion Metrics:**
   - Landing Page CVR (Video to Checkout) - 2-5% is typical
   - Checkout CVR (Checkout to Purchase) - 15-30% is a good range
   - Upsell Take Rate - 20-40% is typical for relevant offers

3. **Revenue Metrics:**
   - AOV (Average Order Value) - Main offer + upsell revenue
   - LTV (Lifetime Value) - Consider future purchases

4. **Profitability Metrics:**
   - CPA (Cost Per Acquisition) - Should be less than AOV
   - ROAS (Return on Ad Spend) - Aim for 1.5-3x or higher
   - ROI (Return on Investment) - Should be positive (>0%)

## Example Funnel Calculations

For a profitable funnel:
- $1.20 CPC
- 4% Landing Page CVR
- 25% Checkout CVR
- 35% Upsell Take Rate
- $97 Main Offer + $47 Upsell

Results in:
- $113.87 AOV
- $30.00 CPA
- 3.80x ROAS
- 73.7% Profit Margin

## Credits

This suite was built for analyzing funnel economics and optimizing sales funnels.

For support or questions, please see the documentation in the models directory. 