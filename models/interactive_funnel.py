import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from funnel_economics import calculate_funnel_economics, visualize_funnel, find_breakeven_metrics, run_sensitivity_analysis

def print_header():
    print("\n" + "=" * 80)
    print("                FUNNEL ECONOMICS CALCULATOR                ")
    print("Video Ad -> Checkout/Sales Page -> Upsell 1 (Community)")
    print("=" * 80)

def get_numerical_input(prompt, default_value, min_value=0):
    while True:
        try:
            user_input = input(f"{prompt} [{default_value}]: ")
            if user_input == "":
                return default_value
            value = float(user_input)
            if value < min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_percentage_input(prompt, default_value):
    while True:
        try:
            user_input = input(f"{prompt} [{default_value*100}%]: ")
            if user_input == "":
                return default_value
            if "%" in user_input:
                user_input = user_input.replace("%", "")
            value = float(user_input) / 100
            if value < 0 or value > 1:
                print("Percentage must be between 0 and 100. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a percentage.")

def get_funnel_parameters():
    print("\n--- TRAFFIC METRICS ---")
    daily_ad_spend = get_numerical_input("Daily ad spend ($)", 1000)
    avg_cpc = get_numerical_input("Average cost per click ($)", 1.5, 0.01)
    
    print("\n--- CONVERSION METRICS ---")
    lp_cvr = get_percentage_input("Landing page conversion rate", 0.03)
    checkout_cvr = get_percentage_input("Checkout conversion rate", 0.20)
    upsell_take_rate = get_percentage_input("Upsell acceptance rate", 0.30)
    
    print("\n--- REVENUE METRICS ---")
    main_offer_price = get_numerical_input("Main offer price ($)", 97)
    upsell_price = get_numerical_input("Upsell price ($)", 47)
    
    print("\n--- COST METRICS ---")
    cogs_percent = get_percentage_input("Cost of goods sold (% of revenue)", 0.20)
    fulfillment_cost = get_numerical_input("Per-order fulfillment cost ($)", 5)
    
    print("\n--- REFUND METRICS ---")
    main_offer_refund_rate = get_percentage_input("Main offer refund rate", 0.10)
    upsell_refund_rate = get_percentage_input("Upsell refund rate", 0.05)
    
    print("\n--- TIME PERIOD ---")
    days = int(get_numerical_input("Number of days to model", 30, 1))
    
    # Return all parameters as a dictionary
    return {
        'daily_ad_spend': daily_ad_spend,
        'avg_cpc': avg_cpc,
        'lp_cvr': lp_cvr,
        'checkout_cvr': checkout_cvr,
        'upsell_take_rate': upsell_take_rate,
        'main_offer_price': main_offer_price,
        'upsell_price': upsell_price,
        'cogs_percent': cogs_percent,
        'fulfillment_cost': fulfillment_cost,
        'main_offer_refund_rate': main_offer_refund_rate,
        'upsell_refund_rate': upsell_refund_rate,
        'days': days
    }

def display_funnel_summary(summary):
    print("\n", "=" * 40)
    print("           FUNNEL SUMMARY           ")
    print("=" * 40)
    
    # Traffic & Conversion Metrics
    print(f"\n--- TRAFFIC & CONVERSION METRICS ---")
    print(f"Total Ad Spend: ${summary['total_ad_spend']:,.2f}")
    print(f"Total Clicks: {summary['total_clicks']:,.0f}")
    print(f"Checkout Page Visitors: {summary['total_clicks'] * summary['lp_cvr']:,.0f}")
    print(f"Conversion Rate (Ad to Checkout): {summary['lp_cvr']:.2%}")
    print(f"Conversion Rate (Checkout to Sale): {summary['checkout_cvr']:.2%}")
    print(f"Upsell Take Rate: {summary['upsell_take_rate']:.2%}")
    print(f"Total Sales: {summary['total_sales']:,.0f}")
    print(f"Total Upsells: {summary['total_sales'] * summary['upsell_take_rate']:,.0f}")
    
    # Revenue Metrics
    print(f"\n--- REVENUE METRICS ---")
    print(f"Average Order Value (AOV): ${summary['avg_aov']:,.2f}")
    print(f"Main Offer Revenue: ${summary['main_offer_revenue']:,.2f}")
    print(f"Upsell Revenue: ${summary['upsell_revenue']:,.2f}")
    print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
    
    # Cost & Profit Metrics
    print(f"\n--- COST & PROFIT METRICS ---")
    print(f"Cost Per Acquisition (CPA): ${summary['avg_cpa']:,.2f}")
    print(f"Cost Per Click (CPC): ${summary['avg_cpc']:,.2f}")
    print(f"Total Profit: ${summary['total_profit']:,.2f}")
    print(f"Profit Margin: {summary['profit_margin']:.2%}")
    print(f"Return on Ad Spend (ROAS): {summary['avg_roas']:.2f}x")
    print(f"Return on Investment (ROI): {summary['avg_roi']:.2%}")

def calculate_breakeven_metrics(params):
    print("\n", "=" * 40)
    print("      BREAKEVEN SCENARIO ANALYSIS      ")
    print("=" * 40)
    
    target_roi = get_percentage_input("\nTarget ROI for breakeven analysis", 0.5)
    
    breakeven_df = find_breakeven_metrics(
        target_roi=target_roi,
        main_offer_price=params['main_offer_price'],
        upsell_price=params['upsell_price'],
        base_metrics=params
    )
    
    if not breakeven_df.empty:
        print(f"\nTop 5 Breakeven Scenarios for {target_roi:.0%} ROI:")
        for i, row in breakeven_df.sort_values('roi').head(5).iterrows():
            print(f"\nScenario {i+1}:")
            print(f"  Landing Page CVR: {row['lp_cvr']:.2%}")
            print(f"  Checkout CVR: {row['checkout_cvr']:.2%}")
            print(f"  Upsell Take Rate: {row['upsell_take_rate']:.2%}")
            print(f"  Resulting ROI: {row['roi']:.2%}")
            print(f"  Cost Per Acquisition: ${row['cpa']:.2f}")
            print(f"  Return on Ad Spend: {row['roas']:.2f}x")
    else:
        print(f"No combinations found that achieve the target ROI of {target_roi:.0%}.")
        
    return breakeven_df

def main():
    print_header()
    
    print("\nEnter your funnel parameters (press Enter to accept default values):")
    params = get_funnel_parameters()
    
    # Calculate funnel economics with the user-provided parameters
    funnel_df, summary = calculate_funnel_economics(**params)
    
    # Add some derived metrics for display
    summary['main_offer_revenue'] = funnel_df['main_offer_revenue'].sum()
    summary['upsell_revenue'] = funnel_df['upsell_revenue'].sum()
    summary['avg_cpc'] = params['avg_cpc']
    
    # Display the summary metrics
    display_funnel_summary(summary)
    
    # Ask if the user wants to visualize the funnel
    vis_choice = input("\nDo you want to visualize the funnel? (y/n) [y]: ").lower() or 'y'
    if vis_choice == 'y':
        fig = visualize_funnel(funnel_df, summary)
        plt.show()
    
    # Ask if the user wants to run breakeven analysis
    breakeven_choice = input("\nDo you want to run breakeven analysis? (y/n) [y]: ").lower() or 'y'
    if breakeven_choice == 'y':
        breakeven_df = calculate_breakeven_metrics(params)
    
    # Ask if the user wants to run sensitivity analysis
    sensitivity_choice = input("\nDo you want to run sensitivity analysis? (y/n) [y]: ").lower() or 'y'
    if sensitivity_choice == 'y':
        print("\nRunning sensitivity analysis...")
        results, fig = run_sensitivity_analysis(params)
        plt.show()
    
    print("\nFunnel economics analysis complete!")

if __name__ == "__main__":
    main() 