import argparse
import os
from moneyforward_selenium import MoneyForwardScraper
from db import Cashflow, session


MONEYFORWARD_USER = os.environ["MONEYFORWARD_USER"]
MONEYFORWARD_PASSWORD = os.environ["MONEYFORWARD_PASSWORD"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("group", help='グループ名')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    group = args.group
    with MoneyForwardScraper(MONEYFORWARD_USER, MONEYFORWARD_PASSWORD, group_name=group) as mf:
        fiscal_year = 2024
        for i in range(10, 13):
            cashflows = mf.get_cashflows_of_fiscal_month(fiscal_year=fiscal_year, fiscal_month=i)
            for cashflow in cashflows:
                c = Cashflow(
                    id=cashflow.id,
                    calc=cashflow.calc,
                    date=cashflow.date,
                    fiscal_year=cashflow.fiscal_year,
                    fiscal_month=cashflow.fiscal_month,
                    content=cashflow.content,
                    amount=cashflow.amount,
                    note=cashflow.note,
                    lcategory=cashflow.lcategory,
                    mcategory=cashflow.mcategory,
                    memo=cashflow.memo,
                )
                session.merge(c)
                session.commit()
