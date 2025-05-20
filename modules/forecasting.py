import streamlit as st
from prophet import Prophet
import pandas as pd

def render(df):
    st.header(" Financial Forecasting")

    if df is None or 'Date' not in df.columns:
        st.warning("Valid date-based financial data required.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df = df.groupby('Date')['Amount'].sum().reset_index()
    df.columns = ['ds', 'y']

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    st.subheader(" Forecast")
    st.line_chart(forecast.set_index('ds')[['yhat', 'yhat_upper', 'yhat_lower']])
