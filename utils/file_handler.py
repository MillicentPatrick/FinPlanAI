import pandas as pd
import streamlit as st
from io import StringIO

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format.")
    except Exception as e:
        st.error(f"File error: {e}")
    return None

def load_sample_budget():
    try:
        return pd.read_csv("data/sample_budget_data.csv")
    except FileNotFoundError:
        st.warning("Sample budget data not found.")
        return None

def load_sample_investments():
    try:
        data = StringIO("""
Asset,Category,Type,Amount Invested,Return,Start Date,End Date
Stock A,Equity,Investment,1000,1200,2023-01-01,2023-12-31
Bond B,Fixed Income,Investment,2000,2100,2023-01-01,2023-12-31
Real Estate,Property,Investment,5000,5500,2022-01-01,2024-01-01
ETF C,Equity,Investment,1500,1800,2023-06-01,2024-06-01
        """)
        return pd.read_csv(data, parse_dates=["Start Date", "End Date"])
    except Exception as e:
        st.error(f"Error loading investment data: {e}")
        return None

def load_sample_projects():
    try:
        return pd.read_csv("data/sample_project_data.csv")
    except FileNotFoundError:
        st.warning("Sample project data not found.")
        return None

def load_sample_dividends():
    try:
        data = StringIO("""
Date,Stock,Amount,Reinvested
2023-01-01,AAPL,25.00,Yes
2023-02-01,GOOG,15.00,No
2023-03-01,AAPL,30.00,Yes
2023-04-01,MSFT,20.00,Yes
2023-05-01,GOOG,10.00,No
        """)
        return pd.read_csv(data, parse_dates=["Date"])
    except Exception as e:
        st.error(f"Error loading dividend data: {e}")
        return None
