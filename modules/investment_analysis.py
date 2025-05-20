import streamlit as st
import pandas as pd
import plotly.express as px

def analyze_investments(df):
    st.header("Investment Performance Analysis")

    if df is None or df.empty:
        st.warning("No investment data available.")
        return

    # Ensure correct data types
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["End Date"] = pd.to_datetime(df["End Date"])

    # Calculate additional metrics
    df["Return Amount"] = df["Return"] - df["Amount Invested"]
    df["Return %"] = (df["Return Amount"] / df["Amount Invested"]) * 100
    df["Duration (days)"] = (df["End Date"] - df["Start Date"]).dt.days

    st.dataframe(df)

    # Chart: Return by Asset
    fig = px.bar(df, x="Asset", y="Return Amount", color="Category", title="Return by Asset")
    st.plotly_chart(fig, use_container_width=True)

    # Chart: Return % by Asset
    fig2 = px.bar(df, x="Asset", y="Return %", color="Category", title="Return % by Asset")
    st.plotly_chart(fig2, use_container_width=True)

    # Summary stats
    st.subheader("Summary Statistics")
    total_invested = df["Amount Invested"].sum()
    total_return = df["Return"].sum()
    total_profit = df["Return Amount"].sum()

    st.markdown(f"""
    - **Total Invested:** ${total_invested:,.2f}  
    - **Total Return:** ${total_return:,.2f}  
    - **Total Profit:** ${total_profit:,.2f}  
    - **Average Return %:** {df['Return %'].mean():.2f}%  
    """)

