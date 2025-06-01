# investment_simulator.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use("Agg")

# For Excel export
from io import BytesIO

def calculate_investment_summary(
    purchase_price,
    purchase_costs,
    equity,
    loan_interest,
    loan_repayment,
    loan_years, 
    size_sqm,
    maintenance_per_sqm,
    vacancy_rate,
    rents,
    service_charge_annual,
    deductible_service_charge_pct,
    tax_rate,
    amortization_rate 
):
    results = []
    total_cost = purchase_price + purchase_costs
    loan_amount = total_cost - equity

    MAX_SIMULATION_YEARS = 100 # To avoid endless loops

    
    annual_amortization_value = purchase_price * amortization_rate 
    

    annual_fixed_repayment_amount = loan_amount * loan_repayment

    for rent in rents:
        maintenance_cost = maintenance_per_sqm * size_sqm
        equity_increase = 0
        current_remaining_debt = loan_amount 
        
        df_rows = [] 

        
        df_rows.append({
            "Year": 0,
            "**Gross Rent (€)**": 0.0,
            "Interest Payment (€)": 0.0,
            "Deductible Service Charge (€)": 0.0,
            "Amortization (€)": 0.0,
            "**Cashflow Before Taxes (€)**": 0.0,
            "Taxes (€)": 0.0,
            "Loan Repayment (Principal) (€)": 0.0,
            "Maintenance (€)": 0.0,
            "Vacancy Loss (€)": 0.0,
            "Non-Deductible Service Charge (€)": 0.0,
            "**Net Cashflow (€)**": 0.0,
            "Total Equity (€)": equity,
            "Remaining Debt (€)": current_remaining_debt,
            "Annual Return on Invested Equity (Cash-on-Cash) (%)": 0.0
        })
        
        simulated_year = 0
        # Loop runs as long as debt > 0
        while current_remaining_debt > 0.0 and simulated_year < MAX_SIMULATION_YEARS:
            simulated_year += 1 

            gross_rent = rent * size_sqm * 12
            deductible_service_charge = service_charge_annual * deductible_service_charge_pct
            non_deductible_service_charge = service_charge_annual - deductible_service_charge
            vacancy_loss = gross_rent * vacancy_rate

            current_interest_payment = 0.0
            current_loan_repayment = 0.0
            
            if current_remaining_debt > 0.0:
                current_interest_payment = current_remaining_debt * loan_interest
                
                
                current_loan_repayment = min(annual_fixed_repayment_amount, current_remaining_debt)
                
                current_remaining_debt -= current_loan_repayment
                if current_remaining_debt < 0.0:
                    current_remaining_debt = 0.0 
            
            # Operative area
            cashflow_before_taxes_calc = gross_rent - vacancy_loss - maintenance_cost - non_deductible_service_charge - current_interest_payment
            
            # Taxable income: (Gross Rent - Deductible Service Charge - Interest - Amortization)
            taxable_income = gross_rent - deductible_service_charge - current_interest_payment - annual_amortization_value
            taxes = max(0.0, taxable_income * tax_rate)

            # Cashflow After Taxes 
            cashflow_after_taxes = cashflow_before_taxes_calc - taxes
            
            # Net Cashflow 
            net_cashflow = cashflow_after_taxes - current_loan_repayment
            
            annual_roe_cash_on_cash = (cashflow_after_taxes / equity) * 100 if equity > 0 else 0.0
            
            equity_increase += current_loan_repayment 
            total_equity = equity + equity_increase

            df_rows.append({
                "Year": simulated_year,
                "**Gross Rent (€)**": gross_rent,
                "Interest Payment (€)": current_interest_payment,
                "Deductible Service Charge (€)": deductible_service_charge,
                "Amortization (€)": annual_amortization_value,
                "**Cashflow Before Taxes (€)**": cashflow_before_taxes_calc,
                "Taxes (€)": taxes,
                "Loan Repayment (Principal) (€)": current_loan_repayment,
                "Maintenance (€)": maintenance_cost,
                "Vacancy Loss (€)": vacancy_loss,
                "Non-Deductible Service Charge (€)": non_deductible_service_charge,
                "**Net Cashflow (€)**": net_cashflow,
                "Total Equity (€)": total_equity,
                "Remaining Debt (€)": max(current_remaining_debt, 0.0), 
                "Annual Return on Invested Equity (Cash-on-Cash) (%)": annual_roe_cash_on_cash
            })

        
        df = pd.DataFrame(df_rows)
        
        
        paid_off_year = None
        
        
        
        df_for_payoff = df[df['Year'] > 0].copy()
        df_for_payoff['Remaining Debt (€)'] = pd.to_numeric(df_for_payoff['Remaining Debt (€)'])

        
        payoff_row = df_for_payoff[df_for_payoff['Remaining Debt (€)'] <= 0].head(1)

        if not payoff_row.empty:
            year_of_payoff = payoff_row['Year'].iloc[0]
            
            
            if year_of_payoff == 1:
                paid_off_year = 1.0
            else:
                
                prev_year_data = df_for_payoff[df_for_payoff['Year'] == year_of_payoff - 1]
                if not prev_year_data.empty:
                    debt_at_start_of_payoff_year = prev_year_data['Remaining Debt (€)'].iloc[0]
                    repayment_in_payoff_year = df_for_payoff[df_for_payoff['Year'] == year_of_payoff]['Loan Repayment (Principal) (€)'].iloc[0]

                    if repayment_in_payoff_year > 0: 
                        
                        paid_off_year = (year_of_payoff - 1) + (debt_at_start_of_payoff_year / repayment_in_payoff_year)
                    else:
                        
                        paid_off_year = float(year_of_payoff)
                else: 
                    paid_off_year = float(year_of_payoff)
        else: 
            paid_off_year = None

        
        results.append((rent, df.iloc[1:].reset_index(drop=True), paid_off_year))

    return results

# function for excel export
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Data')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def main():
    st.set_page_config(page_title="Real Estate Investment Simulator", layout="wide")
    st.title("Real Estate Investment Simulator")

    with st.sidebar:
        st.header("Purchase Inputs")
        purchase_price = st.number_input("Property Purchase Price (€)", value=100000.0)
        purchase_costs = st.number_input("Additional Purchase Costs (€)", value=10000.0)
        equity = st.number_input("Equity Contribution (€)", value=20000.0)
        size_sqm = st.number_input("Property Size (m²)", value=40.0)

        st.header("Financing Inputs")
        loan_interest = st.number_input("Loan Interest Rate (%)", value=4.0) / 100
        loan_repayment = st.number_input("Initial Repayment Rate (%)", value=3.0) / 100
        loan_years = st.number_input("Loan Duration (years)", value=10) 

        st.header("Operating Costs")
        maintenance_per_sqm = st.number_input("Maintenance Reserve per m² (€)", value=10.0)
        vacancy_rate = st.number_input("Vacancy Rate (%)", value=5.0) / 100
        service_charge_annual = st.number_input("Annual Service Charges (€)", value=1200.0)
        deductible_service_charge_pct = st.number_input("Deductible Service Charge Portion (%)", value=70.0) / 100

        st.header("Assumptions")
        rents_str = st.text_input("Expected Rent per m² (comma-separated, e.g. 15,25,30)", value="25,30,35")
        tax_rate = st.number_input("Tax Rate / Marginal Tax Rate (%)", value=30.0) / 100
        
        amortization_rate = st.number_input("Annual Amortization Rate (% of Purchase Price)", value=2.0) / 100

    rents = [float(x.strip()) for x in rents_str.split(",") if x.strip()]
    scenarios = calculate_investment_summary(
        purchase_price,
        purchase_costs,
        equity,
        loan_interest,
        loan_repayment,
        loan_years,
        size_sqm,
        maintenance_per_sqm,
        vacancy_rate,
        rents,
        service_charge_annual,
        deductible_service_charge_pct,
        tax_rate,
        amortization_rate 
    )

    st.header("Equity Return Summary")
    st.write("This table provides an overview of key financial metrics for each rent scenario:")
    summary_data = []

    for rent, df, paid_off_year in scenarios:
        total_net_cashflow = df["**Net Cashflow (€)**"].sum()
        final_equity = df["Total Equity (€)"].iloc[-1]

        roi_total = (total_net_cashflow + (final_equity - equity)) / equity if equity > 0 else 0.0

        simulated_years = df["Year"].max()
        net_cashflow_per_year_avg = total_net_cashflow / simulated_years if simulated_years > 0 else 0.0

        average_annual_roi_on_equity = (roi_total * 100) / simulated_years if simulated_years > 0 else 0.0

        summary_data.append({
            "Rent €/m²": rent,
            "Cumulative Net Cashflow (€)": total_net_cashflow,
            "Average Annual Net Cashflow (€)": net_cashflow_per_year_avg,
            "Final Equity (€)": final_equity,
            "Total ROI on Equity (%)": roi_total * 100,
            "Average Annual ROI on Equity p.a. (%)": average_annual_roi_on_equity,
            "Loan Paid Off Year": f"{paid_off_year:.1f}" if paid_off_year is not None else "N/A (within simulated years)"
        })
    summary_df = pd.DataFrame(summary_data).round(2)
    st.dataframe(summary_df)

    # Excel export button for summary
    st.download_button(
        label="Export Summary to Excel",
        data=to_excel(summary_df),
        file_name="investment_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Dropdown
    plot_metric = st.selectbox(
        "Select the metric for the plot:",
        ("Net Cashflow (€)", "Annual Return on Invested Equity (Cash-on-Cash) (%)", "Cashflow Before Taxes (€)", "Interest Payment (€)", "Taxes (€)", "Loan Repayment (Principal) (€)")
    )

    st.header(f"Comparison of {plot_metric} Across Rent Scenarios")
    st.markdown(
        "**Net Cashflow (€)**: This represents the **actual cash remaining** after *all* property expenses, including operating costs (vacancy, maintenance, non-deductible service charges), interest payments, taxes, *and principal loan repayments*. This is the true 'bottom line' profit for the investor."
    )
    st.markdown(
        "**Cashflow Before Taxes (€)**: Shows the cash generated by the property after deducting operating expenses and interest payments, but *before* taxes. This is a key metric for evaluating the property's operational efficiency before considering the tax impact."
    )
    st.markdown(
        "**Annual Return on Invested Equity (Cash-on-Cash) (%)**: Measures the annual return on the initially invested equity, based on the **Cashflow After Taxes (€)** (which is not a directly plotted column, but is the basis for this return) of that specific year. It indicates the cash return on the equity invested through ongoing income."
    )
    st.markdown(
        "**Interest Payment (€)**: The annual interest paid on the loan."
    )
    st.markdown(
        "**Taxes (€)**: The annual income tax paid on the property's taxable income, considering deductible expenses and amortization."
    )
    st.markdown(
        "**Loan Repayment (Principal) (€)**: The portion of the loan payment that reduces the outstanding principal amount each year."
    )
    st.markdown(
        "**Important Note:** The 'Annual Return on Invested Equity (Cash-on-Cash) (%)' is based on the cashflow *after taxes but before principal loan repayment*. The 'Net Cashflow (€)' is the final cash flow after all expenses, including principal repayment."
    )


    
    all_plot_data = pd.DataFrame()
    y_column_for_plot_data = ""

    
    if plot_metric == "Net Cashflow (€)":
        y_column_for_plot_data = "**Net Cashflow (€)**"
    elif plot_metric == "Cashflow Before Taxes (€)":
        y_column_for_plot_data = "**Cashflow Before Taxes (€)**"
    elif plot_metric == "Annual Return on Invested Equity (Cash-on-Cash) (%)":
        y_column_for_plot_data = "Annual Return on Invested Equity (Cash-on-Cash) (%)"
    elif plot_metric == "Interest Payment (€)":
        y_column_for_plot_data = "Interest Payment (€)"
    elif plot_metric == "Taxes (€)":
        y_column_for_plot_data = "Taxes (€)"
    elif plot_metric == "Loan Repayment (Principal) (€)":
        y_column_for_plot_data = "Loan Repayment (Principal) (€)"

    for rent, df, _ in scenarios:
        
        
        if y_column_for_plot_data in df.columns:
            temp = df[["Year", y_column_for_plot_data]].copy()
            temp.rename(columns={y_column_for_plot_data: plot_metric}, inplace=True)
            temp["Rent"] = f"{rent:.2f} €/m²"
            all_plot_data = pd.concat([all_plot_data, temp], ignore_index=True)
        else:
            st.warning(f"Column '{y_column_for_plot_data}' not found in DataFrame for rent {rent:.2f} €/m². Skipping plot data for this scenario.")


    if not all_plot_data.empty:
        fig_combined, ax_combined = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=all_plot_data, x="Year", y=plot_metric, hue="Rent", marker="o", ax=ax_combined)
        ax_combined.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax_combined.set_title(f"{plot_metric} per Rent Scenario", fontsize=16, weight="bold", pad=15)
        ax_combined.set_xlabel("Year", fontsize=12)
        ax_combined.set_ylabel(f"{plot_metric}", fontsize=12)

        ax_combined.tick_params(axis='both', labelsize=10)
        ax_combined.grid(True, linestyle="--", linewidth=0.7, alpha=0.6)
        ax_combined.spines['top'].set_visible(False)
        ax_combined.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig_combined)
    else:
        st.info("No data available to plot the selected metric.")


    # Display detailed dataframes for each scenario
    st.subheader("Detailed Scenario Dataframes")
    st.write("Each table below provides a detailed breakdown of the financial metrics for a specific rent scenario:")
    for rent, df, paid_off_year in scenarios:
        st.write(f"--- Detailed Scenario: {rent:.2f} €/m² ---")
        st.dataframe(df.style.format("{:.2f}"))

        first_positive_cf_year = df[df["**Net Cashflow (€)**"] > 0]["Year"].min()
        if pd.isna(first_positive_cf_year):
            st.markdown("**The Net Cash Flow will not be positive in this scenario.**")
        else:
            st.markdown(f"**The Net Cashflow will be positive for the first time in year {int(first_positive_cf_year)}.**")

        
        if paid_off_year is not None and paid_off_year > 0:
            st.markdown(f"**In the current scenario you will have paid off the loan in {paid_off_year:.1f} years.**")
        else:
            st.markdown(f"**The loan will not be paid back in the next {df['Year'].max()} years. Please consider your inheritors.**")


        st.download_button(
            label=f"Export Detailed Data for {rent:.2f} €/m² to Excel",
            data=to_excel(df),
            file_name=f"detailed_scenario_{rent:.2f}_eur_m2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_detailed_{rent}"
        )
        st.write("---")

if __name__ == "__main__":
    main()
