import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_funnel_economics(
    # Traffic metrics
    daily_ad_spend=1000,               # Daily ad spend in dollars
    avg_cpc=1.5,                       # Average cost per click in dollars
    
    # Conversion metrics
    lp_cvr=0.03,                       # Landing page conversion rate (video ad to checkout)
    checkout_cvr=0.20,                 # Checkout conversion rate (checkout page to purchase)
    upsell_take_rate=0.30,             # Upsell acceptance rate
    
    # Revenue metrics
    main_offer_price=97,               # Price of main offer in dollars
    upsell_price=47,                   # Price of upsell (community) in dollars
    
    # Cost metrics
    cogs_percent=0.20,                 # Cost of goods sold as percentage of revenue
    fulfillment_cost=5,                # Per-order fulfillment cost in dollars
    
    # Refund metrics
    main_offer_refund_rate=0.10,       # Refund rate for main offer
    upsell_refund_rate=0.05,           # Refund rate for upsell
    
    # Time period
    days=30                            # Number of days to model
):
    """
    Calculate the economics of a funnel with:
    Video Ad -> Checkout/Sales Page -> Upsell 1 (Community)
    """
    
    # Initialize the funnel DataFrame
    funnel_df = pd.DataFrame(index=range(days))
    
    # Traffic metrics
    funnel_df['ad_spend'] = daily_ad_spend
    funnel_df['clicks'] = funnel_df['ad_spend'] / avg_cpc
    funnel_df['cpc'] = avg_cpc
    funnel_df['ctr'] = None  # Would need impressions data to calculate CTR
    
    # Conversion metrics
    funnel_df['checkouts'] = funnel_df['clicks'] * lp_cvr
    funnel_df['sales'] = funnel_df['checkouts'] * checkout_cvr
    funnel_df['upsells'] = funnel_df['sales'] * upsell_take_rate
    
    # Revenue metrics
    funnel_df['main_offer_revenue'] = funnel_df['sales'] * main_offer_price * (1 - main_offer_refund_rate)
    funnel_df['upsell_revenue'] = funnel_df['upsells'] * upsell_price * (1 - upsell_refund_rate)
    funnel_df['total_revenue'] = funnel_df['main_offer_revenue'] + funnel_df['upsell_revenue']
    
    # Cost metrics
    funnel_df['cogs'] = funnel_df['total_revenue'] * cogs_percent
    funnel_df['fulfillment_costs'] = funnel_df['sales'] * fulfillment_cost
    funnel_df['total_costs'] = funnel_df['ad_spend'] + funnel_df['cogs'] + funnel_df['fulfillment_costs']
    
    # Profit metrics
    funnel_df['profit'] = funnel_df['total_revenue'] - funnel_df['total_costs']
    funnel_df['roi'] = funnel_df['profit'] / funnel_df['ad_spend']
    funnel_df['roas'] = funnel_df['total_revenue'] / funnel_df['ad_spend']
    
    # Customer metrics
    funnel_df['cpa'] = funnel_df['ad_spend'] / funnel_df['sales']  # Cost per acquisition
    funnel_df['aov'] = funnel_df['total_revenue'] / funnel_df['sales']  # Average order value
    funnel_df['clv'] = funnel_df['aov']  # Customer lifetime value (simplified)
    
    # Calculate totals and averages
    totals = funnel_df.sum()
    averages = funnel_df.mean()
    
    summary = {
        'total_ad_spend': totals['ad_spend'],
        'total_clicks': totals['clicks'],
        'total_sales': totals['sales'],
        'total_revenue': totals['total_revenue'],
        'total_profit': totals['profit'],
        'avg_cpa': averages['cpa'],
        'avg_aov': averages['aov'],
        'avg_roi': averages['roi'],
        'avg_roas': averages['roas'],
        'lp_cvr': lp_cvr,
        'checkout_cvr': checkout_cvr,
        'upsell_take_rate': upsell_take_rate,
        'profit_margin': totals['profit'] / totals['total_revenue']
    }
    
    return funnel_df, summary

def find_breakeven_metrics(
    target_roi=0.5,  # Target ROI (e.g., 0.5 = 50% ROI)
    main_offer_price=97,
    upsell_price=47,
    base_metrics=None  # Default metrics to start with
):
    """
    Find combinations of conversion rates that achieve the target ROI.
    """
    if base_metrics is None:
        base_metrics = {
            'daily_ad_spend': 1000,
            'avg_cpc': 1.5,
            'lp_cvr': 0.03,
            'checkout_cvr': 0.20,
            'upsell_take_rate': 0.30,
            'main_offer_price': main_offer_price,
            'upsell_price': upsell_price,
            'cogs_percent': 0.20,
            'fulfillment_cost': 5,
            'main_offer_refund_rate': 0.10,
            'upsell_refund_rate': 0.05,
            'days': 1
        }
    
    # Ranges to test
    lp_cvr_range = np.linspace(0.01, 0.1, 10)
    checkout_cvr_range = np.linspace(0.1, 0.4, 10)
    upsell_rate_range = np.linspace(0.1, 0.6, 10)
    
    results = []
    
    # Test different combinations
    for lp_cvr in lp_cvr_range:
        for checkout_cvr in checkout_cvr_range:
            for upsell_rate in upsell_rate_range:
                metrics = base_metrics.copy()
                metrics.update({
                    'lp_cvr': lp_cvr,
                    'checkout_cvr': checkout_cvr,
                    'upsell_take_rate': upsell_rate
                })
                
                _, summary = calculate_funnel_economics(**metrics)
                
                if summary['avg_roi'] >= target_roi:
                    results.append({
                        'lp_cvr': lp_cvr,
                        'checkout_cvr': checkout_cvr,
                        'upsell_take_rate': upsell_rate,
                        'roi': summary['avg_roi'],
                        'cpa': summary['avg_cpa'],
                        'roas': summary['avg_roas']
                    })
    
    return pd.DataFrame(results)

def visualize_funnel(funnel_df, summary):
    """
    Create visualizations for the funnel.
    """
    # Set the style
    plt.style.use('ggplot')
    sns.set_palette("viridis")
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(15, 12))
    
    # 1. Funnel visualization
    funnel_steps = ['clicks', 'checkouts', 'sales', 'upsells']
    funnel_values = [funnel_df[step].sum() for step in funnel_steps]
    
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.bar(funnel_steps, funnel_values)
    ax1.set_title('Funnel Visualization')
    ax1.set_ylabel('Number of Users')
    
    # Add conversion rates
    for i in range(len(funnel_steps)-1):
        cvr = funnel_values[i+1] / funnel_values[i] if funnel_values[i] > 0 else 0
        ax1.annotate(f'{cvr:.1%}', 
                     xy=((i+0.5), min(funnel_values[i], funnel_values[i+1]) + (abs(funnel_values[i] - funnel_values[i+1])/2)),
                     xytext=(0, 0),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontsize=10, color='black')
    
    # 2. Revenue breakdown
    ax2 = fig.add_subplot(2, 2, 2)
    revenue_sources = ['main_offer_revenue', 'upsell_revenue']
    revenue_values = [funnel_df[source].sum() for source in revenue_sources]
    ax2.pie(revenue_values, labels=revenue_sources, autopct='%1.1f%%')
    ax2.set_title('Revenue Breakdown')
    
    # 3. Cumulative profit over time
    ax3 = fig.add_subplot(2, 2, 3)
    funnel_df['cumulative_profit'] = funnel_df['profit'].cumsum()
    ax3.plot(funnel_df.index, funnel_df['cumulative_profit'])
    ax3.set_title('Cumulative Profit Over Time')
    ax3.set_xlabel('Days')
    ax3.set_ylabel('Profit ($)')
    
    # 4. Daily Metrics
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(funnel_df.index, funnel_df['cpa'], label='CPA')
    ax4.plot(funnel_df.index, funnel_df['aov'], label='AOV')
    ax4.set_title('Daily Customer Metrics')
    ax4.set_xlabel('Days')
    ax4.set_ylabel('Value ($)')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('funnel_visualization.png')
    
    # Print summary metrics
    print("\nFunnel Summary Metrics:")
    print(f"Total Ad Spend: ${summary['total_ad_spend']:,.2f}")
    print(f"Total Clicks: {summary['total_clicks']:,.0f}")
    print(f"Total Sales: {summary['total_sales']:,.0f}")
    print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
    print(f"Total Profit: ${summary['total_profit']:,.2f}")
    print(f"Average CPA: ${summary['avg_cpa']:,.2f}")
    print(f"Average AOV: ${summary['avg_aov']:,.2f}")
    print(f"Average ROI: {summary['avg_roi']:.2%}")
    print(f"Average ROAS: {summary['avg_roas']:.2f}x")
    print(f"Profit Margin: {summary['profit_margin']:.2%}")
    
    return fig

def run_sensitivity_analysis(base_params=None):
    """
    Run sensitivity analysis on key metrics.
    """
    if base_params is None:
        base_params = {
            'daily_ad_spend': 1000,
            'avg_cpc': 1.5,
            'lp_cvr': 0.03,
            'checkout_cvr': 0.20,
            'upsell_take_rate': 0.30,
            'main_offer_price': 97,
            'upsell_price': 47,
            'cogs_percent': 0.20,
            'fulfillment_cost': 5,
            'main_offer_refund_rate': 0.10,
            'upsell_refund_rate': 0.05,
            'days': 30
        }
    
    # Parameters to test with ranges (param_name: (min_value, max_value, steps))
    params_to_test = {
        'avg_cpc': (0.5, 3.0, 10),
        'lp_cvr': (0.01, 0.1, 10),
        'checkout_cvr': (0.05, 0.4, 10),
        'upsell_take_rate': (0.1, 0.6, 10),
        'main_offer_price': (47, 197, 10),
        'main_offer_refund_rate': (0.05, 0.2, 10)
    }
    
    results = {}
    
    # Run analysis for each parameter
    for param_name, (min_val, max_val, steps) in params_to_test.items():
        param_values = np.linspace(min_val, max_val, steps)
        roi_values = []
        profit_values = []
        
        for value in param_values:
            test_params = base_params.copy()
            test_params[param_name] = value
            
            _, summary = calculate_funnel_economics(**test_params)
            roi_values.append(summary['avg_roi'])
            profit_values.append(summary['total_profit'])
        
        results[param_name] = {
            'param_values': param_values,
            'roi_values': roi_values,
            'profit_values': profit_values
        }
    
    # Create visualization
    fig, axs = plt.subplots(len(params_to_test), 2, figsize=(15, 4 * len(params_to_test)))
    
    for i, (param_name, data) in enumerate(results.items()):
        # ROI plot
        axs[i, 0].plot(data['param_values'], data['roi_values'])
        axs[i, 0].set_title(f'ROI Sensitivity to {param_name}')
        axs[i, 0].set_xlabel(param_name)
        axs[i, 0].set_ylabel('ROI')
        
        # Profit plot
        axs[i, 1].plot(data['param_values'], data['profit_values'])
        axs[i, 1].set_title(f'Profit Sensitivity to {param_name}')
        axs[i, 1].set_xlabel(param_name)
        axs[i, 1].set_ylabel('Profit ($)')
    
    plt.tight_layout()
    plt.savefig('sensitivity_analysis.png')
    
    return results, fig

if __name__ == "__main__":
    # Base case funnel economics
    funnel_df, summary = calculate_funnel_economics()
    
    # Visualize the funnel
    visualize_funnel(funnel_df, summary)
    
    # Find breakeven metrics
    breakeven_df = find_breakeven_metrics(target_roi=0.5)
    print("\nSample Breakeven Metrics (for 50% ROI):")
    if not breakeven_df.empty:
        print(breakeven_df.sort_values('roi').head(5))
    else:
        print("No combinations found that achieve the target ROI.")
    
    # Run sensitivity analysis
    run_sensitivity_analysis()
    
    print("\nFunnel economic model complete. Check the generated visualizations.") 