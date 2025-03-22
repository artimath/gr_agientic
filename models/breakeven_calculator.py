#!/usr/bin/env python3
"""
Breakeven Calculator for Video Ad -> Checkout/Sales Page -> Upsell Funnel

A simplified calculator that focuses on determining the key metrics needed
for a profitable funnel without all the detailed analysis.
"""

def calculate_breakeven_metrics(
    # Basic inputs
    ad_spend=1000,           # Daily ad spend in dollars
    main_price=97,           # Price of main offer
    upsell_price=47,         # Price of upsell
    
    # Cost structure
    cogs_percent=0.20,       # Cost of goods as percentage of revenue
    fulfillment_cost=5,      # Shipping & handling per order
    
    # Known metrics (if any)
    lp_cvr=None,             # Landing page CVR (if known)
    checkout_cvr=None,       # Checkout CVR (if known)
    upsell_rate=None,        # Upsell take rate (if known)
    avg_cpc=None,            # Average cost per click (if known)
    
    # Target metrics
    target_roi=0.3,          # Target ROI (30% by default)
    
    # Refund rates
    main_refund_rate=0.1,    # Main offer refund rate
    upsell_refund_rate=0.05  # Upsell refund rate
):
    """Calculate the breakeven metrics for the funnel."""
    
    # Adjust prices for refunds
    effective_main_price = main_price * (1 - main_refund_rate)
    effective_upsell_price = upsell_price * (1 - upsell_refund_rate)
    
    # Calculate average order value with upsell
    def calc_aov(upsell_rate):
        return effective_main_price + (effective_upsell_price * upsell_rate)
    
    # Calculate costs per order
    def calc_costs_per_order(aov):
        return (aov * cogs_percent) + fulfillment_cost
    
    # Calculate breakeven CPA
    def calc_breakeven_cpa(aov, target_roi=target_roi):
        costs = calc_costs_per_order(aov)
        return (aov - costs) / (1 + target_roi)
    
    # Calculate the combined funnel CVR (from click to purchase)
    def calc_funnel_cvr(lp_cvr, checkout_cvr):
        return lp_cvr * checkout_cvr
    
    # Calculate CPA from CVR and CPC
    def calc_cpa(funnel_cvr, cpc):
        return cpc / funnel_cvr
    
    # Results dictionary
    results = {
        'inputs': {
            'ad_spend': ad_spend,
            'main_price': main_price, 
            'upsell_price': upsell_price,
            'cogs_percent': cogs_percent,
            'fulfillment_cost': fulfillment_cost,
            'target_roi': target_roi
        },
        'breakeven': {},
        'scenarios': []
    }
    
    # Calculate for different upsell rates if not provided
    upsell_rates = [upsell_rate] if upsell_rate is not None else [0.1, 0.2, 0.3, 0.4, 0.5]
    
    for ur in upsell_rates:
        aov = calc_aov(ur)
        breakeven_cpa = calc_breakeven_cpa(aov)
        
        scenario = {
            'upsell_rate': ur,
            'aov': aov,
            'breakeven_cpa': breakeven_cpa
        }
        
        # If we know the CPC, calculate needed CVR
        if avg_cpc is not None:
            breakeven_cvr = avg_cpc / breakeven_cpa
            scenario['needed_cvr'] = breakeven_cvr
            
            # If we know landing page CVR, calculate checkout CVR
            if lp_cvr is not None:
                needed_checkout_cvr = breakeven_cvr / lp_cvr
                scenario['needed_checkout_cvr'] = needed_checkout_cvr
            
            # If we know checkout CVR, calculate landing page CVR
            if checkout_cvr is not None:
                needed_lp_cvr = breakeven_cvr / checkout_cvr
                scenario['needed_lp_cvr'] = needed_lp_cvr
        
        # If we know both CVRs, calculate breakeven CPC
        if lp_cvr is not None and checkout_cvr is not None:
            funnel_cvr = calc_funnel_cvr(lp_cvr, checkout_cvr)
            breakeven_cpc = breakeven_cpa * funnel_cvr
            scenario['breakeven_cpc'] = breakeven_cpc
        
        results['scenarios'].append(scenario)
    
    # If we have complete information, calculate the best scenario
    if None not in [lp_cvr, checkout_cvr, upsell_rate, avg_cpc]:
        funnel_cvr = calc_funnel_cvr(lp_cvr, checkout_cvr)
        cpa = calc_cpa(funnel_cvr, avg_cpc)
        aov = calc_aov(upsell_rate)
        costs = calc_costs_per_order(aov)
        profit = aov - costs - cpa
        roi = profit / cpa
        
        results['current'] = {
            'funnel_cvr': funnel_cvr,
            'cpa': cpa,
            'aov': aov,
            'costs_per_order': costs,
            'profit_per_order': profit,
            'roi': roi,
            'is_profitable': roi > target_roi
        }
    
    return results

def print_breakeven_results(results):
    """Print the breakeven calculator results in a readable format."""
    print("\n" + "=" * 60)
    print("             FUNNEL BREAKEVEN CALCULATOR              ")
    print("=" * 60)
    
    # Print scenarios
    print("\nBREAKEVEN METRICS FOR DIFFERENT UPSELL RATES:")
    print("-" * 60)
    print(f"{'Upsell Rate':^15}{'AOV':^15}{'Breakeven CPA':^15}")
    print("-" * 60)
    
    for scenario in results['scenarios']:
        upsell = f"{scenario['upsell_rate']:.0%}"
        aov = f"${scenario['aov']:.2f}"
        cpa = f"${scenario['breakeven_cpa']:.2f}"
        
        print(f"{upsell:^15}{aov:^15}{cpa:^15}")
        
        # Print additional metrics if available
        if 'needed_cvr' in scenario:
            print(f"  Needed Total CVR: {scenario['needed_cvr']:.2%}")
        if 'needed_checkout_cvr' in scenario:
            print(f"  Needed Checkout CVR: {scenario['needed_checkout_cvr']:.2%}")
        if 'needed_lp_cvr' in scenario:
            print(f"  Needed Landing Page CVR: {scenario['needed_lp_cvr']:.2%}")
        if 'breakeven_cpc' in scenario:
            print(f"  Breakeven CPC: ${scenario['breakeven_cpc']:.2f}")
        print()
    
    # Print current profitability if available
    if 'current' in results:
        print("\nCURRENT FUNNEL PROFITABILITY:")
        print("-" * 60)
        current = results['current']
        
        print(f"Funnel CVR: {current['funnel_cvr']:.2%}")
        print(f"CPA: ${current['cpa']:.2f}")
        print(f"AOV: ${current['aov']:.2f}")
        print(f"Costs Per Order: ${current['costs_per_order']:.2f}")
        print(f"Profit Per Order: ${current['profit_per_order']:.2f}")
        print(f"ROI: {current['roi']:.2%}")
        
        if current['is_profitable']:
            print("\n✅ Your funnel is PROFITABLE based on target ROI!")
        else:
            print("\n❌ Your funnel is NOT PROFITABLE based on target ROI.")
            
    print("\n" + "=" * 60)

def get_user_input():
    """Get user input for the breakeven calculator."""
    
    print("\n" + "=" * 60)
    print("             FUNNEL BREAKEVEN CALCULATOR              ")
    print("=" * 60)
    print("\nEnter your funnel metrics (press Enter to use default values):")
    
    # Helper function for inputs
    def get_float_input(prompt, default):
        value = input(f"{prompt} [{default}]: ")
        return float(value) if value else default
    
    def get_percent_input(prompt, default):
        value = input(f"{prompt} [{default*100}%]: ")
        if not value:
            return default
        if "%" in value:
            value = value.replace("%", "")
        return float(value) / 100
    
    # Basic inputs
    ad_spend = get_float_input("Daily ad spend ($)", 1000)
    main_price = get_float_input("Main offer price ($)", 97)
    upsell_price = get_float_input("Upsell price ($)", 47)
    
    # Cost structure
    cogs_percent = get_percent_input("Cost of goods (%)", 0.20)
    fulfillment_cost = get_float_input("Fulfillment cost per order ($)", 5)
    
    # Refund rates
    main_refund_rate = get_percent_input("Main offer refund rate (%)", 0.10)
    upsell_refund_rate = get_percent_input("Upsell refund rate (%)", 0.05)
    
    # Target ROI
    target_roi = get_percent_input("Target ROI (%)", 0.30)
    
    # Known metrics (optional)
    print("\nEnter known metrics (or leave blank if unknown):")
    
    lp_cvr_input = input("Landing page CVR [e.g., 3%]: ")
    lp_cvr = float(lp_cvr_input.replace("%", "")) / 100 if lp_cvr_input else None
    
    checkout_cvr_input = input("Checkout CVR [e.g., 20%]: ")
    checkout_cvr = float(checkout_cvr_input.replace("%", "")) / 100 if checkout_cvr_input else None
    
    upsell_rate_input = input("Upsell take rate [e.g., 30%]: ")
    upsell_rate = float(upsell_rate_input.replace("%", "")) / 100 if upsell_rate_input else None
    
    avg_cpc_input = input("Average CPC [$]: ")
    avg_cpc = float(avg_cpc_input) if avg_cpc_input else None
    
    return {
        'ad_spend': ad_spend,
        'main_price': main_price,
        'upsell_price': upsell_price,
        'cogs_percent': cogs_percent,
        'fulfillment_cost': fulfillment_cost,
        'main_refund_rate': main_refund_rate,
        'upsell_refund_rate': upsell_refund_rate,
        'target_roi': target_roi,
        'lp_cvr': lp_cvr,
        'checkout_cvr': checkout_cvr,
        'upsell_rate': upsell_rate,
        'avg_cpc': avg_cpc
    }

if __name__ == "__main__":
    # Get user inputs
    inputs = get_user_input()
    
    # Calculate breakeven metrics
    results = calculate_breakeven_metrics(**inputs)
    
    # Print results
    print_breakeven_results(results) 