import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def simulate_growth(initial, growth_rate, div_yield, years, reinvest=True):
    value = initial
    dividends = 0
    history = []

    for year in range(1, years + 1):
        dividend = value * div_yield
        dividends += dividend
        if reinvest:
            value = value * (1 + growth_rate) + dividend
        else:
            value = value * (1 + growth_rate)
        history.append((year, value, dividends))

    return pd.DataFrame(history, columns=["Year", "Portfolio Value", "Cumulative Dividends"])


def render(df):
    st.header("📈 Dividends & Reinvestment Simulation")

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df.columns = df.columns.str.strip()

    # Detect format
    if {"Asset", "Initial Investment", "Annual Dividend Yield (%)", "Annual Growth Rate (%)", "Years"}.issubset(df.columns):
        run_projection_simulation(df)
    elif {"Date", "Stock", "Amount", "Reinvested"}.issubset(df.columns):
        run_historical_dividend_view(df)
    else:
        st.error("Unsupported format. Please provide either historical dividend data or simulation inputs.")
        st.write("Available columns:", list(df.columns))


def run_projection_simulation(df):
    st.subheader("📊 Simulated Dividend Projection")

    for _, row in df.iterrows():
        asset = row["Asset"]
        try:
            initial = float(row["Initial Investment"])
            div_yield = float(row["Annual Dividend Yield (%)"]) / 100
            growth_rate = float(row["Annual Growth Rate (%)"]) / 100
            years = int(row["Years"])
        except Exception as e:
            st.warning(f"Skipping {asset}: {e}")
            continue

        reinvest_df = simulate_growth(initial, growth_rate, div_yield, years, reinvest=True)
        cash_df = simulate_growth(initial, growth_rate, div_yield, years, reinvest=False)

        st.subheader(f"{asset}: {years}-Year Projection")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Reinvesting Dividends")
            st.dataframe(reinvest_df)
        with col2:
            st.write("Taking Dividends as Cash")
            st.dataframe(cash_df)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=reinvest_df["Year"], y=reinvest_df["Portfolio Value"],
                                 mode='lines+markers', name='Reinvest'))
        fig.add_trace(go.Scatter(x=cash_df["Year"], y=cash_df["Portfolio Value"],
                                 mode='lines+markers', name='Cash'))
        fig.update_layout(title=f"{asset}: Portfolio Growth",
                          xaxis_title="Year", yaxis_title="Value ($)")
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            f"Reinvested Dividends: ${reinvest_df['Cumulative Dividends'].iloc[-1]:,.2f} | "
            f"Cash Dividends: ${cash_df['Cumulative Dividends'].iloc[-1]:,.2f}"
        )


def run_historical_dividend_view(df):
    st.subheader("📘 Historical Dividend Records")

    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna()

    total_dividends = df.groupby("Stock")["Amount"].sum().reset_index()

    st.dataframe(df)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=total_dividends["Stock"], y=total_dividends["Amount"],
                         name="Total Dividends"))
    fig.update_layout(title="Total Dividends per Stock", xaxis_title="Stock", yaxis_title="Amount ($)")
    st.plotly_chart(fig, use_container_width=True)

    reinvest_summary = df.groupby("Reinvested")["Amount"].sum().reset_index()
    st.subheader("Reinvestment Summary")
    st.dataframe(reinvest_summary)
