import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO

def compute_investment_metrics(df):
    df = df.copy()
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["End Date"] = pd.to_datetime(df["End Date"])
    df["Duration (Years)"] = (df["End Date"] - df["Start Date"]).dt.days / 365.25
    df["ROI (%)"] = ((df["Return"] - df["Amount Invested"]) / df["Amount Invested"]) * 100
    df["CAGR (%)"] = (
        (df["Return"] / df["Amount Invested"]) ** (1 / df["Duration (Years)"]) - 1
    ) * 100
    return df

def generate_download_link(df):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

def render(datasets):
    st.header(" Summary Report: Financial Overview")

    # Expecting a dictionary of dataframes
    budget_df = datasets.get("budget")
    investment_df = datasets.get("investments")
    project_df = datasets.get("projects")
    dividend_df = datasets.get("dividends")

    if investment_df is not None and not investment_df.empty:
        st.subheader(" Investment Summary")

        required_cols = {"Asset", "Amount Invested", "Return", "Start Date", "End Date"}
        if required_cols.issubset(investment_df.columns):
            investment_df = compute_investment_metrics(investment_df)
            st.dataframe(investment_df)

            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    investment_df,
                    values="Amount Invested",
                    names="Category",
                    title="Investment by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(
                    investment_df,
                    x="Asset",
                    y="ROI (%)",
                    color="Category",
                    title="ROI by Asset"
                )
                st.plotly_chart(fig, use_container_width=True)

            csv_data = generate_download_link(investment_df)
            st.download_button(
                label=" Download Investment CSV",
                data=csv_data,
                file_name="investment_summary.csv",
                mime="text/csv"
            )
        else:
            st.warning("Investment data missing required columns.")

    if budget_df is not None and not budget_df.empty:
        st.subheader(" Budget Summary")
        st.dataframe(budget_df)

    if project_df is not None and not project_df.empty:
        st.subheader(" Capital Projects")
        st.dataframe(project_df)

    if dividend_df is not None and not dividend_df.empty:
        st.subheader(" Dividends Overview")
        st.dataframe(dividend_df)

