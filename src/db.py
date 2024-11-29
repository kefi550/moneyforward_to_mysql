import pymysql
from sqlalchemy import create_engine, String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session
from datetime import date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Cashflow(Base):
    __tablename__ = 'cashflow'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    group: Mapped[str] = mapped_column(String(100), nullable=False)
    calc: Mapped[bool] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(nullable=False)
    fiscal_month: Mapped[int] = mapped_column(nullable=False)
    # 内容
    content: Mapped[str] = mapped_column(String(200), nullable=False)
    # 金額
    amount: Mapped[int] = mapped_column(nullable=False)
    # 金融機関
    note: Mapped[str] = mapped_column(String(30), nullable=True)
    # 大項目
    lcategory: Mapped[str] = mapped_column(String(30), nullable=False)
    # 中項目
    mcategory: Mapped[str] = mapped_column(String(30), nullable=False)
    # メモ
    memo: Mapped[str] = mapped_column(String(100), nullable=True)


class Budget(Base):
    __tablename__ = 'budget'

    group: Mapped[str] = mapped_column(String(30), primary_key=True)
    lcategory: Mapped[str] = mapped_column(String(30), primary_key=True)
    fiscal_year: Mapped[int] = mapped_column(primary_key=True)
    fiscal_month: Mapped[int] = mapped_column(primary_key=True)
    budget: Mapped[int] = mapped_column(nullable=False)


class ExpenseRatio(Base):
    __tablename__ = 'expense_ratio'

    fiscal_year: Mapped[int] = mapped_column(primary_key=True)
    fiscal_month: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    ratio: Mapped[float] = mapped_column(nullable=False)


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
