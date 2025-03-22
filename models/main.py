#!/usr/bin/env python3
"""
Funnel Economics Model - Main Interface

This script provides a unified interface to access all the funnel economics tools:
1. Interactive Funnel Calculator
2. Breakeven Calculator
3. Full Funnel Analysis with Visualizations
"""

import os
import sys
import importlib.util

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'pandas', 
        'numpy', 
        'matplotlib', 
        'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️ Missing required packages. Please install them with:")
        print(f"pip install {' '.join(missing_packages)}")
        print("\nOr run: pip install -r requirements.txt")
        return False
    
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    """Print welcome message and menu."""
    clear_screen()
    print("\n" + "=" * 80)
    print("                   FUNNEL ECONOMICS MODELING SUITE                    ")
    print("          Video Ad -> Checkout/Sales Page -> Upsell (Community)       ")
    print("=" * 80)
    
    print("\nThis suite helps you model and analyze the economics of your sales funnel.\n")
    print("Available Tools:")
    print("  1. Quick Breakeven Calculator")
    print("  2. Interactive Funnel Calculator")
    print("  3. Full Funnel Analysis with Visualizations")
    print("  4. View Documentation")
    print("  0. Exit")

def run_breakeven_calculator():
    """Run the breakeven calculator."""
    clear_screen()
    print("\nLaunching Quick Breakeven Calculator...\n")
    
    try:
        from breakeven_calculator import get_user_input, calculate_breakeven_metrics, print_breakeven_results
        
        inputs = get_user_input()
        results = calculate_breakeven_metrics(**inputs)
        print_breakeven_results(results)
        
    except ImportError:
        print("⚠️ Error: Could not import breakeven_calculator.py")
    except Exception as e:
        print(f"⚠️ Error running breakeven calculator: {e}")
    
    input("\nPress Enter to continue...")

def run_interactive_calculator():
    """Run the interactive funnel calculator."""
    clear_screen()
    print("\nLaunching Interactive Funnel Calculator...\n")
    
    try:
        from interactive_funnel import main
        main()
    except ImportError:
        print("⚠️ Error: Could not import interactive_funnel.py")
    except Exception as e:
        print(f"⚠️ Error running interactive calculator: {e}")
    
    input("\nPress Enter to continue...")

def run_full_analysis():
    """Run the full funnel analysis with visualizations."""
    clear_screen()
    print("\nLaunching Full Funnel Analysis...\n")
    
    try:
        from funnel_economics import calculate_funnel_economics, visualize_funnel, find_breakeven_metrics, run_sensitivity_analysis
        
        print("Running funnel analysis with default parameters...")
        print("(This may take a moment to generate visualizations)")
        
        # Run with default parameters
        funnel_df, summary = calculate_funnel_economics()
        visualize_funnel(funnel_df, summary)
        
        # Find breakeven metrics
        breakeven_df = find_breakeven_metrics(target_roi=0.5)
        if not breakeven_df.empty:
            print("\nSample Breakeven Metrics (for 50% ROI):")
            print(breakeven_df.sort_values('roi').head(5))
        else:
            print("No combinations found that achieve the target ROI.")
        
        # Run sensitivity analysis
        run_sensitivity_analysis()
        
        print("\nAnalysis complete! Visualizations have been saved as:")
        print("- funnel_visualization.png")
        print("- sensitivity_analysis.png")
        
    except ImportError:
        print("⚠️ Error: Could not import funnel_economics.py")
    except Exception as e:
        print(f"⚠️ Error running full analysis: {e}")
    
    input("\nPress Enter to continue...")

def view_documentation():
    """Display documentation."""
    clear_screen()
    
    try:
        with open('README.md', 'r') as f:
            readme_content = f.read()
        
        print("\n" + "=" * 80)
        print("                        DOCUMENTATION                        ")
        print("=" * 80 + "\n")
        print(readme_content)
        
    except FileNotFoundError:
        print("\n⚠️ Documentation file (README.md) not found.")
    except Exception as e:
        print(f"\n⚠️ Error reading documentation: {e}")
    
    input("\nPress Enter to continue...")

def main():
    """Main function to run the funnel economics modeling suite."""
    
    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    while True:
        print_welcome()
        
        choice = input("\nEnter your choice (0-4): ")
        
        if choice == '0':
            print("\nExiting Funnel Economics Modeling Suite. Goodbye!")
            break
        elif choice == '1':
            run_breakeven_calculator()
        elif choice == '2':
            run_interactive_calculator()
        elif choice == '3':
            run_full_analysis()
        elif choice == '4':
            view_documentation()
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 0 and 4.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 