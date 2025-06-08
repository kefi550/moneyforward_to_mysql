import datetime
import os
from dateutil.relativedelta import relativedelta
from moneyforward_selenium import MoneyForwardScraper
from db import Cashflow, Budget, create_session


MONEYFORWARD_USER = os.environ["MONEYFORWARD_USER"]
MONEYFORWARD_PASSWORD = os.environ["MONEYFORWARD_PASSWORD"]
MONEYFORWARD_GROUP = os.environ["MONEYFORWARD_GROUP"]
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
DB_PORT = int(os.environ.get('MYSQL_PORT', 3306))
DB_NAME = os.environ.get('DB_NAME', 'mf_kakeibo')
SELENIUM_HOST = os.environ.get("SELENIUM_HOST", "127.0.0.1")
SELENIUM_PORT = os.environ.get("SELENIUM_PORT", "4444")

UPDATE_MONTHS = os.environ.get("UPDATE_MONTHS", 3)  # 何ヶ月前までのデータを取得するか

session = create_session(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, DB_PORT, DB_NAME)
today = datetime.date.today()
for month in range(0, UPDATE_MONTHS):
    d = today - relativedelta(months=month)
    # TODO: カレンダー月になってしまっているので正しく営業月にする
    fiscal_year = d.year
    fiscal_month = d.month
    # なんか月の切り替えにたまに失敗するので、月ごとにdriverをつくりなおす
    with MoneyForwardScraper(
        moneyforward_user=MONEYFORWARD_USER,
        moneyforward_password=MONEYFORWARD_PASSWORD,
        selenium_host=SELENIUM_HOST,
        selenium_port=SELENIUM_PORT,
        moneyforward_group_name=MONEYFORWARD_GROUP,
    ) as mf:
        # 入出金の更新
        cashflows = mf.get_cashflows_of_fiscal_month(fiscal_year=fiscal_year, fiscal_month=fiscal_month)
        for cashflow in cashflows:
            c = Cashflow(
                id=cashflow.id,
                group=MONEYFORWARD_GROUP,
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

# 予算の更新
with MoneyForwardScraper(
    moneyforward_user=MONEYFORWARD_USER,
    moneyforward_password=MONEYFORWARD_PASSWORD,
    selenium_host=SELENIUM_HOST,
    selenium_port=SELENIUM_PORT,
    moneyforward_group_name=MONEYFORWARD_GROUP,
) as mf:
    budgets = mf.get_budgets_of_group()
    for budget in budgets:
        b = Budget(
            fiscal_year=today.year,
            fiscal_month=today.month,
            group=MONEYFORWARD_GROUP,
            lcategory=budget.lcategory,
            budget=budget.budget,
        )
        session.merge(b)
        session.commit()
