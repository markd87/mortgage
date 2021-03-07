from main import (
    main,
    calc_monthly_payment,
    get_cumulative_interest,
    calc_equity_loan_interest,
)
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.write("# Mortgage Calculator")

house_price = st.sidebar.number_input(
    "House Price (£)",
    value=500_000,
    min_value=100_000,
    max_value=None,
    step=10_000,
    format="%d",
)

rate = st.sidebar.number_input(
    "Fixed Rate (%)", value=1.0, min_value=0.1, max_value=5.0, step=0.5
)

deposit = st.sidebar.number_input(
    "Deposit (%)", value=10, min_value=5, max_value=100, step=5
)

years = st.sidebar.number_input("Years", value=25, min_value=1, max_value=None, step=5)

equity_loan = st.sidebar.number_input(
    "Help to buy (%)", value=0, min_value=0, max_value=40, step=20
)


tot = main(house_price, rate, years, equity_loan, deposit)

st.write("\n")

deposit_amount = deposit * house_price / 100
equity_loan_amount = equity_loan * house_price / 100

mortgage_amount = house_price - deposit_amount - equity_loan_amount

monthly_payment = calc_monthly_payment(mortgage_amount, rate, years)

interest_payments = get_cumulative_interest(
    mortgage_amount, rate, monthly_payment, years
)
capital_payments = np.array(
    [i * monthly_payment - interest_payments[i] for i in range(years * 12 + 1)]
)

df_payments = pd.DataFrame(
    {
        "Month": np.arange(years * 12 + 1),
        "Interest payments": interest_payments,
        "Mortgage Left": mortgage_amount - capital_payments,
    }
)


st.write("## Details")
st.write(f"Buying a house for **£{house_price:,}**")
st.write(f"Deposit of **£{deposit_amount:,.2f}**")

if equity_loan:
    st.write(f"Help to buy loan amount: **£{equity_loan_amount:,.2f}**")
    loan_payments = calc_equity_loan_interest(equity_loan_amount, years)
    df_payments["Equity loan interest paid"] = np.cumsum(loan_payments)
    tot_equity_interest_paid = np.sum(loan_payments)
    total_paid = tot_equity_interest_paid + tot

df_payments = df_payments.melt(
    "Month", var_name="Payment Type", value_name="Payment Value"
)

st.write(f"Mortgage needed for **£{mortgage_amount:,.2f}**")

st.write("## Summary")
st.write(f"Monthly payments of: **£{monthly_payment:,.2f}**")
st.write(f"Mortgage interest paid after {years} years: **£{tot:,}**")
if equity_loan:
    st.write(
        f"Equity loan interest paid after {years} years: **£{tot_equity_interest_paid:,.2f}**"
    )
    st.write(f"Total interest paid: **£{total_paid:,.2f}**")


line_chart = (
    alt.Chart(df_payments, width=500)
    .mark_line(interpolate="basis")
    .encode(
        alt.X("Month", title="Months"),
        alt.Y("Payment Value", title="£"),
        color="Payment Type:N",
        tooltip=[
            "Month",
            "Payment Type",
            alt.Tooltip("Payment Value:Q", format=",.2f"),
        ],
    )
    .properties(title="Payments with time")
).interactive()

st.altair_chart(line_chart)


# to hide streamlit link and top right menu
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
