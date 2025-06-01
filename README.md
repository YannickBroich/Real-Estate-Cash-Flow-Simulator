# Real Estate Investment Simulator

## Overview
This is a Streamlit web application designed to help users simulate potential returns and cash flows from real estate investments. It allows for detailed input of purchase costs, financing terms, operating expenses, and various rent scenarios to project the financial performance over time, including the estimated loan payoff period.

## Features
- **Comprehensive Cost Analysis:** Input purchase price, additional costs, and equity.
- **Flexible Financing Simulation:** Configure loan interest rate, initial repayment rate, and original loan duration.
- **Detailed Operating Expenses:** Account for maintenance, vacancy rates, and annual service charges (deductible and non-deductible).
- **Tax Considerations:** Incorporate a tax rate and annual amortization.
- **Multi-Scenario Rent Analysis:** Compare different rent per square meter scenarios.
- **Dynamic Simulation Length:** The simulation continues beyond the initial `loan_years` until the loan is fully repaid or a maximum simulation period is reached (currently 100 years).
- **Key Financial Metrics:** Provides tables for:
    - **Equity Return Summary:** High-level overview including cumulative net cash flow, average annual ROI, and estimated loan payoff year.
    - **Detailed Scenario Dataframes:** Year-by-year breakdown of all financial components.
- **Interactive Plots:** Visualize key metrics over time for comparative analysis across rent scenarios.
- **Loan Payoff Indicator:** A vertical line in the detailed scenario plots indicates the estimated year when the loan is fully repaid.
- **Excel Export:** Download summary and detailed data for further analysis.

