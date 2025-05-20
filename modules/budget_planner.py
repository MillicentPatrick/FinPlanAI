import streamlit as st


def render(df):
    st.header(" Budget Planner")

    if df is None:
        st.warning("No data loaded.")
        return

    st.write("### Sample Data:")
    st.dataframe(df.head())

    expenses = df[df['Type'].str.lower() == 'expense']
    income = df[df['Type'].str.lower() == 'income']

    total_income = income['Amount'].sum()
    total_expense = expenses['Amount'].sum()
    savings = total_income - total_expense

    st.metric(" Total Income", f"${total_income:,.2f}")
    st.metric(" Total Expenses", f"${total_expense:,.2f}")
    st.metric(" Net Savings", f"${savings:,.2f}")

    st.subheader(" Expenses by Category")
    if not expenses.empty:
        exp_chart = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        st.bar_chart(exp_chart)
