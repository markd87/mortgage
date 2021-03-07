import pandas as pd
import numpy as np
from typing import List


def calc_monthly_payment(loan_amount: int, rate: float, years: int) -> float:
    """
    Get total monthly payment for loan amount, rate and number of years
    """
    months = years * 12
    monthly_rate = rate / 100 / 12
    return (
        loan_amount
        * monthly_rate
        * ((1 + monthly_rate) ** months)
        / ((1 + monthly_rate) ** months - 1)
    )


def get_cumulative_interest(
    loan: int, rate: float, monthly_payment: float, years: int
) -> List[float]:
    """Calculate cumulative interest paid after each month up to number of years"""
    monthly_rate = rate / 100 / 12
    months = years * 12
    return [
        (loan * monthly_rate - monthly_payment)
        / monthly_rate
        * ((1 + monthly_rate) ** i - 1)
        + monthly_payment * i
        for i in range(months + 1)
    ]


def calc_equity_loan_interest(equity_amount: int, years: int) -> List[float]:
    """
    Calculate interest payments for Help to Buy equity loan.
    """
    cpi_change = 2 / 100
    base = 2 / 100
    rate = 1.75 / 100 / 12

    payments = [0 for month in range(5 * 12)]

    for month in range((years - 5) * 12 + 1):
        payments.append(rate * equity_amount)
        if month % 12 == 0 and month > 0:
            rate = rate * (1 + cpi_change + base)

        # assume half after half the time
        # if month == years * 12 // 2:
        #     equity_amount /= 2

    return payments


def main(
    house_price: int,
    rate: float,
    years: int,
    equity_loan: float = 0,
    deposit: float = 10,
) -> None:
    """
    house_price: price of the house
    deposit: % deposit
    rate: mortgage rate (%)
    equity_loan: % of house price given as loan
    years: years for the mortgage

    return:
    """

    months = years * 12

    equity_loan_amount = equity_loan / 100 * house_price

    deposit_amount = deposit / 100 * house_price

    loan_amount = house_price - equity_loan_amount - deposit_amount

    monthly_payment = calc_monthly_payment(loan_amount, rate, years)

    total_interest_paid = monthly_payment * months - loan_amount

    # first 5 years are interest free
    equity_loan_interest = calc_equity_loan_interest(equity_loan_amount, years)

    print(f"Deposit: £{np.round(deposit_amount,2):,}")
    print(f"Equity loan: £{np.round(equity_loan_amount,2):,}")
    print(f"Mortgage loan: £{np.round(loan_amount,2):,}")
    print(f"Mortgage interest paid: £{np.round(total_interest_paid, 2):,}")
    print(f"Equity loan interest paid: £{np.round(np.sum(equity_loan_interest),2):,}")


if __name__ == "__main__":
    main(500_000, 2, 25, 40, 10)