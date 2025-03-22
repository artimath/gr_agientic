#!/usr/bin/env python3
"""
Example Funnel Scenario

This script runs the funnel economics model with realistic numbers
for a video ad -> checkout/sales page -> upsell funnel.
"""

from funnel_economics import calculate_funnel_economics, visualize_funnel

# Example 1: Profitable Funnel Scenario
def run_profitable_example():
    print("\n" + "=" * 80)
    print("                PROFITABLE FUNNEL EXAMPLE                ")
    print("=" * 80)
    
    # Realistic metrics for a profitable funnel
    funnel_df, summary = calculate_funnel_economics(
        # Traffic metrics
        daily_ad_spend=1000,
        avg_cpc=1.2,            # $1.20 CPC (realistic for video ads)
        
        # Conversion metrics
        lp_cvr=0.04,            # 4% landing page conversion rate (strong video ad)
        checkout_cvr=0.25,      # 25% checkout conversion rate (good sales page)
        upsell_take_rate=0.35,  # 35% upsell acceptance rate
        
        # Revenue metrics
        main_offer_price=97,    # $97 main offer
        upsell_price=47,        # $47 upsell (community membership)
        
        # Cost metrics
        cogs_percent=0.15,      # 15% COGS (digital product)
        fulfillment_cost=3,     # $3 fulfillment cost (digital delivery)
        
        # Refund metrics
        main_offer_refund_rate=0.08,  # 8% refund rate
        upsell_refund_rate=0.04,      # 4% upsell refund rate
        
        # Time period
        days=30                 # 30 days simulation
    )
    
    # Add avg_cpc to summary dictionary
    summary['avg_cpc'] = 1.2
    
    # Calculate some key derived metrics
    total_clicks = funnel_df['clicks'].sum()
    total_checkouts = funnel_df['checkouts'].sum()
    total_sales = funnel_df['sales'].sum()
    total_upsells = funnel_df['upsells'].sum()
    
    print(f"\nTraffic Generated: {total_clicks:.0f} clicks at ${summary['avg_cpc']:.2f} CPC")
    print(f"Visitors to Checkout: {total_checkouts:.0f} ({funnel_df['checkouts'].sum() / funnel_df['clicks'].sum():.2%} of clicks)")
    print(f"Completed Sales: {total_sales:.0f} ({funnel_df['sales'].sum() / funnel_df['checkouts'].sum():.2%} of checkouts)")
    print(f"Upsell Purchases: {total_upsells:.0f} ({funnel_df['upsells'].sum() / funnel_df['sales'].sum():.2%} of customers)")
    
    print(f"\nAverage Order Value: ${summary['avg_aov']:.2f}")
    print(f"Cost Per Acquisition: ${summary['avg_cpa']:.2f}")
    print(f"Return on Ad Spend: {summary['avg_roas']:.2f}x")
    print(f"Profit Margin: {summary['profit_margin']:.2%}")
    print(f"Total Profit: ${summary['total_profit']:,.2f}")
    
    return funnel_df, summary


# Example 2: Struggling Funnel Scenario
def run_struggling_example():
    print("\n" + "=" * 80)
    print("                STRUGGLING FUNNEL EXAMPLE                ")
    print("=" * 80)
    
    # Realistic metrics for a struggling funnel
    funnel_df, summary = calculate_funnel_economics(
        # Traffic metrics
        daily_ad_spend=1000,
        avg_cpc=2.1,            # $2.10 CPC (expensive traffic)
        
        # Conversion metrics
        lp_cvr=0.025,           # 2.5% landing page conversion rate (weak video ad)
        checkout_cvr=0.12,      # 12% checkout conversion rate (poor sales page)
        upsell_take_rate=0.20,  # 20% upsell acceptance rate (weak offer)
        
        # Revenue metrics
        main_offer_price=97,    # $97 main offer
        upsell_price=47,        # $47 upsell (community membership)
        
        # Cost metrics
        cogs_percent=0.25,      # 25% COGS (higher product costs)
        fulfillment_cost=8,     # $8 fulfillment cost (physical product)
        
        # Refund metrics
        main_offer_refund_rate=0.15,  # 15% refund rate (customer satisfaction issues)
        upsell_refund_rate=0.10,      # 10% upsell refund rate
        
        # Time period
        days=30                 # 30 days simulation
    )
    
    # Add avg_cpc to summary dictionary
    summary['avg_cpc'] = 2.1
    
    # Calculate some key derived metrics
    total_clicks = funnel_df['clicks'].sum()
    total_checkouts = funnel_df['checkouts'].sum()
    total_sales = funnel_df['sales'].sum()
    total_upsells = funnel_df['upsells'].sum()
    
    print(f"\nTraffic Generated: {total_clicks:.0f} clicks at ${summary['avg_cpc']:.2f} CPC")
    print(f"Visitors to Checkout: {total_checkouts:.0f} ({funnel_df['checkouts'].sum() / funnel_df['clicks'].sum():.2%} of clicks)")
    print(f"Completed Sales: {total_sales:.0f} ({funnel_df['sales'].sum() / funnel_df['checkouts'].sum():.2%} of checkouts)")
    print(f"Upsell Purchases: {total_upsells:.0f} ({total_upsells / total_sales:.2%} of customers)")
    
    print(f"\nAverage Order Value: ${summary['avg_aov']:.2f}")
    print(f"Cost Per Acquisition: ${summary['avg_cpa']:.2f}")
    print(f"Return on Ad Spend: {summary['avg_roas']:.2f}x")
    print(f"Profit Margin: {summary['profit_margin']:.2%}")
    print(f"Total Profit: ${summary['total_profit']:,.2f}")
    
    return funnel_df, summary


# Example 3: Breakeven Analysis
def run_breakeven_analysis():
    from funnel_economics import find_breakeven_metrics
    
    print("\n" + "=" * 80)
    print("                BREAKEVEN ANALYSIS EXAMPLE                ")
    print("=" * 80)
    
    # Base metrics
    base_metrics = {
        'daily_ad_spend': 1000,
        'avg_cpc': 1.8,         # $1.80 CPC
        'cogs_percent': 0.20,   # 20% COGS
        'fulfillment_cost': 5,  # $5 fulfillment cost
        'main_offer_price': 97, # $97 main offer
        'upsell_price': 47,     # $47 upsell
        'main_offer_refund_rate': 0.10,  # 10% refund rate
        'upsell_refund_rate': 0.05,     # 5% upsell refund rate
        'days': 1
    }
    
    # Find breakeven metrics for 30% ROI
    breakeven_df = find_breakeven_metrics(
        target_roi=0.3,  # Target 30% ROI
        base_metrics=base_metrics
    )
    
    print("\nHere are some conversion rate combinations that would achieve a 30% ROI:")
    print("-" * 80)
    print(f"{'LP CVR':^10} {'Checkout CVR':^15} {'Upsell Rate':^15} {'ROI':^10} {'CPA':^10} {'ROAS':^10}")
    print("-" * 80)
    
    # Display top 5 results
    for _, row in breakeven_df.sort_values('roi').head(5).iterrows():
        print(f"{row['lp_cvr']:.2%}".center(10) + 
              f"{row['checkout_cvr']:.2%}".center(15) + 
              f"{row['upsell_take_rate']:.2%}".center(15) + 
              f"{row['roi']:.2%}".center(10) + 
              f"${row['cpa']:.2f}".center(10) + 
              f"{row['roas']:.2f}x".center(10))
    
    return breakeven_df


# Run all examples with visualizations
if __name__ == "__main__":
    # Run profitable funnel example
    profitable_df, profitable_summary = run_profitable_example()
    visualize_funnel(profitable_df, profitable_summary)
    
    # Run struggling funnel example
    struggling_df, struggling_summary = run_struggling_example()
    visualize_funnel(struggling_df, struggling_summary)
    
    # Run breakeven analysis
    breakeven_df = run_breakeven_analysis()
    
    print("\nExample scenarios complete! Visualizations have been saved as PNG files.") 