import streamlit as st

# Import modules
from modules import (
    budget_planner,
    forecasting,
    investment_analysis,
    capital_budgeting,
    dividend_simulation,
    summary_report
)

# Import data loading functions
from utils.file_handler import (
    load_data,
    load_sample_budget,
    load_sample_investments,
    load_sample_projects,
    load_sample_dividends
)

# App settings
st.set_page_config(page_title="FinPlanAI", layout="wide")
st.title("FinPlanAI – Intelligent Financial Planning Dashboard")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Module",
    (
        "Budget Planner",
        "Financial Forecasting",
        "Investment Analysis",
        "Capital Budgeting",
        "Dividends & Reinvestment",
        "Summary Report"
    )
)

# Sidebar uploader
uploaded_file = st.sidebar.file_uploader("Upload your data (CSV or Excel)", type=["csv", "xlsx"])

# Sidebar help for dividends section
if menu == "Dividends & Reinvestment":
    st.sidebar.markdown("**Accepted formats:**")
    st.sidebar.markdown("- Simulated: `Asset, Initial Investment, Annual Dividend Yield (%), Annual Growth Rate (%), Years`")
    st.sidebar.markdown("- Historical: `Date, Stock, Amount, Reinvested`")

# Module routing
if menu == "Budget Planner":
    df = load_data(uploaded_file) if uploaded_file else load_sample_budget()
    budget_planner.render(df)

elif menu == "Financial Forecasting":
    df = load_data(uploaded_file) if uploaded_file else load_sample_budget()
    forecasting.render(df)

elif menu == "Investment Analysis":
    df = load_data(uploaded_file) if uploaded_file else load_sample_investments()
    investment_analysis.analyze_investments(df)

elif menu == "Capital Budgeting":
    df = load_data(uploaded_file) if uploaded_file else load_sample_projects()
    capital_budgeting.render(df)

elif menu == "Dividends & Reinvestment":
    if uploaded_file:
        df = load_data(uploaded_file)
    else:
        df = load_sample_dividends()
    dividend_simulation.render(df)

elif menu == "Summary Report":
    # Combine all modules' data for comprehensive overview
    data = {
        "budget": load_sample_budget(),
        "investments": load_sample_investments(),
        "projects": load_sample_projects(),
        "dividends": load_sample_dividends()
    }
    summary_report.render(data)
