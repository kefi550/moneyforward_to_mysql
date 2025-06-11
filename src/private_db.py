import pymysql
import os
from sqlalchemy import create_engine, String
from sqlalchemy.orm import mapped_column, Mapped, Session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# 支出の分担割合
class ExpenseRatio(Base):
    __tablename__ = 'expense_ratio'

    fiscal_year: Mapped[int] = mapped_column(primary_key=True)
    fiscal_month: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    ratio: Mapped[float] = mapped_column(nullable=False)


# 入金ノルマ
class Deposit(Base):
    __tablename__ = 'deposit'

    fiscal_year: Mapped[int] = mapped_column(primary_key=True)
    fiscal_month: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False)  # 入金ノルマ金額


def create_database_if_not_exists(
    host,
    user,
    password,
    port,
    db_name,
):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        charset='utf8mb4'
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
        conn.commit()
    finally:
        conn.close()


def create_session(
    host,
    user,
    password,
    port,
    db_name,
):
    create_database_if_not_exists(host, user, password, port, db_name)
    DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    return session


def migrate(session):
    # 2024/12 月度時点での支出割合
    # 3:2
    expense_ratio_asuka_202401 = ExpenseRatio(
        fiscal_year=2024,
        fiscal_month=1,
        name='明日香',
        ratio=0.4,
    )
    session.merge(expense_ratio_asuka_202401)
    expense_ratio_shota_202401 = ExpenseRatio(
        fiscal_year=2024,
        fiscal_month=1,
        name='翔太',
        ratio=0.6,
    )
    session.merge(expense_ratio_shota_202401)
    # 2024/12 月度時点での支出割合
    # 1:2 とする
    expense_ratio_asuka_202412 = ExpenseRatio(
        fiscal_year=2024,
        fiscal_month=12,
        name='明日香',
        ratio=0.333,
    )
    session.merge(expense_ratio_asuka_202412)
    expense_ratio_shota_202412 = ExpenseRatio(
        fiscal_year=2024,
        fiscal_month=12,
        name='翔太',
        ratio=0.666,
    )
    session.merge(expense_ratio_shota_202412)
    # 運用開始時の2024/10 月度時点での入金ノルマ
    # 明日香が85000, 翔太が120000、明日香は配偶者手当として36000を2ヶ月に一度振り込む
    deposit_asuka_202401 = Deposit(
        fiscal_year=2024,
        fiscal_month=1,
        name='明日香',
        amount=85000,
    )
    session.merge(deposit_asuka_202401)
    deposit_shota_202401 = Deposit(
        fiscal_year=2024,
        fiscal_month=1,
        name='翔太',
        amount=120000,
    )
    session.merge(deposit_shota_202401)
    # 2024/12 月度時点での入金ノルマ
    # 1:2 として、明日香が70000, 翔太が140000、明日香は配偶者手当として36000を1ヶ月あたり18000として毎月振り込む
    deposit_asuka_202412 = Deposit(
        fiscal_year=2024,
        fiscal_month=12,
        name='明日香',
        amount=88000,
    )
    session.merge(deposit_asuka_202412)
    deposit_shota_202412 = Deposit(
        fiscal_year=2024,
        fiscal_month=12,
        name='翔太',
        amount=140000,
    )
    session.merge(deposit_shota_202412)
    session.commit()


MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
DB_PORT = int(os.environ.get('MYSQL_PORT', 3306))
DB_NAME = os.environ.get('DB_NAME', 'mf_kakeibo')
session = create_session(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, DB_PORT, DB_NAME)

migrate(session)
