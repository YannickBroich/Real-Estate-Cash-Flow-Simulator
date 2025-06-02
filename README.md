# Real Estate Investment Simulator

## Overview
This Streamlit web application is designed to help users simulate potential returns and cash flows from real estate investments. It provides a detailed financial projection based on various user inputs, including purchase costs, financing terms, operating expenses, and different rent scenarios. The simulation dynamically extends until the loan is fully repaid, offering a clear picture of the investment's long-term viability and profitability.

## Features

- **Comprehensive Cost Analysis:**  
  Input property purchase price, additional acquisition costs, and equity contribution.

- **Flexible Financing Simulation:**  
  Configure loan interest rate and an initial repayment rate. The simulation calculates the yearly interest and principal payments, automatically extending the loan duration until the debt is fully repaid.

- **Detailed Operating Expenses:**  
  Account for annual maintenance reserves per square meter, vacancy rates, annual service charges (specifying the deductible and non-deductible portions).

- **Tax Considerations:**  
  Incorporate a user-defined tax rate and an annual amortization rate based on the purchase price for tax-deductible purposes.

- **Multi-Scenario Rent Analysis:**  
  Compare the financial performance across different expected rent per square meter scenarios.

- **Dynamic Simulation Length:**  
  The simulation runs year-by-year until the loan is fully repaid or a predefined maximum simulation period (currently 100 years) is reached, providing a comprehensive long-term outlook.

- **Key Financial Metrics Summary:**  
  A summary table presents high-level insights for each rent scenario, including:
  - Cumulative Net Cashflow  
  - Average Annual Net Cashflow  
  - Final Equity at the end of the simulation  
  - Total Return on Invested Equity  
  - Average Annual Return on Invested Equity (p.a.)  
  - Estimated Loan Payoff Year (to one decimal place)

- **Interactive Plots:**  
  Visualize key financial metrics (Net Cashflow, Annual Return on Invested Equity, Cashflow Before Taxes, Interest Payment, Taxes, Loan Repayment) over time for comparative analysis across different rent scenarios.

- **Loan Payoff Indicator:**  
  Scenario plots include a vertical red dashed line indicating the year (e.g., 22.5 years) when the loan is estimated to be fully repaid.

- **Excel Export:**  
  Download both the summary table and detailed year-by-year dataframes for each scenario into Excel files for offline analysis.

  ## Input Variables

The application allows users to customize various parameters to tailor the simulation to specific investment scenarios:

### Purchase Inputs
-   **Property Purchase Price (€):** The base price of the real estate property.
-   **Additional Purchase Costs (€):** All extra costs associated with the acquisition, such as notary fees, real estate agent commissions, property transfer taxes, etc.
-   **Equity Contribution (€):** The amount of cash you invest upfront from your own funds, reducing the required loan amount.
-   **Property Size (m²):** The total living or usable area of the property in square meters.

### Financing Inputs
-   **Loan Interest Rate (%):** The annual interest rate charged on the outstanding loan balance.
-   **Initial Repayment Rate (%):** The initial annual percentage of the *original loan amount* that will be paid towards the principal. This determines the initial principal repayment component of your loan payments.
-   **Loan Duration (years):** The original planned duration of the loan. While the simulation runs until the loan is fully paid off, this input serves as a reference for typical loan structuring.

### Operating Costs
-   **Maintenance Reserve per m² (€):** The annual amount set aside per square meter for property maintenance, repairs, and capital expenditures.
-   **Vacancy Rate (%):** The estimated percentage of time the property will be vacant (unrented) during a year, leading to lost rental income.
-   **Annual Service Charges (€):** The total annual costs for services and utilities, typically shared among tenants (e.g., heating, water, garbage collection).
-   **Deductible Service Charge Portion (%):** The percentage of the annual service charges that can be deducted from taxable income.

### Assumptions
-   **Expected Rent per m² (comma-separated, e.g., 15,25,30):** One or more expected monthly rent values per square meter. The simulator will run a separate scenario for each value provided, allowing for comparative analysis.
-   **Tax Rate / Marginal Tax Rate (%):** Your personal or corporate tax rate applicable to the property's taxable income.
-   **Annual Amortization Rate (% of Purchase Price):** The annual percentage of the *property's purchase price* that can be deducted from taxable income as depreciation (e.g., for tax purposes).

## How to Run Locally

### Prerequisites
Ensure you have Python installed (Python 3.8+ is recommended).

## How to Run Locally

### Prerequisites
Ensure you have Python installed (Python 3.8+ is recommended).

### 1. Clone the Repository
Clone this repository to your local machine using Git:

bash
git clone https://github.com/YourGitHubUsername/real-estate-investment-simulator.git
cd real-estate-investment-simulator

### 2. Set Up a Virtual Environment (Recommended)
bash

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

### 3. Install Dependencies

Create a requirements.txt file with the following content:

streamlit
pandas
numpy
matplotlib
seaborn
openpyxl

Then install the dependencies

pip install -r requirements.txt

### 4. Run the Streamlit Application

Make sure you are in the right environment

bash

streamlit run app.py

This will open the application in your default web browser.





