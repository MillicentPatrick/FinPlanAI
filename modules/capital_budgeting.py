import streamlit as st
import numpy as np
import pandas as pd


def calculate_npv(rate, cash_flows):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))


def calculate_payback_period(cash_flows):
    cumulative_cash_flow = 0
    for i, cf in enumerate(cash_flows):
        cumulative_cash_flow += cf
        if cumulative_cash_flow >= 0:
            return i
    return None


def run_monte_carlo(initial_outlay, base_cash_flows, rate, num_simulations=1000):
    np.random.seed(42)
    simulations = []

    for _ in range(num_simulations):
        simulated_flows = [
            cf * np.random.normal(1, 0.1) for cf in base_cash_flows
        ]
        simulated_npv = -initial_outlay + calculate_npv(rate, simulated_flows)
        simulations.append(simulated_npv)

    return simulations


def render(df=None):
    st.header(" Capital Budgeting")

    st.write("Input details of a proposed investment/project:")

    project_name = st.text_input("Project Name", "Project A")
    initial_outlay = st.number_input("Initial Investment ($)", value=10000.0)
    lifespan = st.number_input("Project Lifespan (Years)", min_value=1, value=5)
    discount_rate = st.slider("Discount Rate (for NPV/IRR)", min_value=0.01, max_value=0.25, value=0.1)

    cash_flows = []
    st.subheader("Enter Expected Annual Cash Flows")
    for year in range(int(lifespan)):
        cf = st.number_input(f"Year {year + 1} Cash Flow ($)", value=3000.0, key=f"cf_{year}")
        cash_flows.append(cf)

    if st.button("Calculate Metrics"):
        npv = -initial_outlay + calculate_npv(discount_rate, cash_flows)
        try:
            irr = np.irr([-initial_outlay] + cash_flows)
        except Exception:
            irr = None
        payback = calculate_payback_period([-initial_outlay] + cash_flows)

        st.success(f"NPV: ${npv:,.2f}")
        st.success(f"IRR: {irr:.2%}" if irr is not None else "IRR: Not computable")
        st.success(f"Payback Period: {payback} years" if payback is not None else "Payback Period: Not achieved")

        # Monte Carlo Simulation
        st.subheader(" Monte Carlo Risk Simulation")
        simulations = run_monte_carlo(initial_outlay, cash_flows, discount_rate)
        sim_df = pd.DataFrame(simulations, columns=["Simulated NPV"])

        st.line_chart(sim_df)
        st.write(f"Mean NPV: ${np.mean(simulations):,.2f}")
        st.write(f"Probability of Loss (NPV < 0): {np.mean(np.array(simulations) < 0) * 100:.2f}%")
