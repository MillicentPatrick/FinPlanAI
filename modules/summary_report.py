import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO
import zipfile

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

def generate_zip_download(files_dict):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip_file:
        for filename, df in files_dict.items():
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            zip_file.writestr(filename, csv_bytes)
    buffer.seek(0)
    return buffer

def render(datasets):
    st.header(" Summary Report: Financial Overview")

    # Extract individual dataframes
    budget_df = datasets.get("budget")
    investment_df = datasets.get("investments")
    project_df = datasets.get("projects")
    dividend_df = datasets.get("dividends")

    export_files = {}

    # --- Investment Section ---
    if investment_df is not None and not investment_df.empty:
        st.subheader(" Investment Summary")

        required_cols = {"Asset", "Amount Invested", "Return", "Start Date", "End Date"}
        if required_cols.issubset(investment_df.columns):
            investment_df = compute_investment_metrics(investment_df)
            st.dataframe(investment_df)
            export_files["investment_summary.csv"] = investment_df

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
        else:
            st.warning(" Investment data missing required columns.")

    # --- Budget Section ---
    if budget_df is not None and not budget_df.empty:
        st.subheader(" Budget Summary")
        st.dataframe(budget_df)
        export_files["budget_summary.csv"] = budget_df

    # --- Capital Projects Section ---
    if project_df is not None and not project_df.empty:
        st.subheader(" Capital Projects")
        st.dataframe(project_df)
        export_files["projects_summary.csv"] = project_df

    # --- Dividends Section ---
    if dividend_df is not None and not dividend_df.empty:
        st.subheader(" Dividend Overview")
        st.dataframe(dividend_df)
        export_files["dividends_summary.csv"] = dividend_df

    # --- Export All as ZIP ---
    if export_files:
        zip_data = generate_zip_download(export_files)
        st.subheader(" Export Report")
        st.download_button(
            label=" Download Full Summary (ZIP)",
            data=zip_data,
            file_name="FinPlanAI_Full_Summary.zip",
            mime="application/zip"
        )

   
            
       
