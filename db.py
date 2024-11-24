import os
import pymysql
from sqlalchemy import create_engine, String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session
from datetime import date
from sqlalchemy.ext.declarative import declarative_base


DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_NAME = os.environ.get('DB_NAME', 'mf_kakeibo')

Base = declarative_base()


class Cashflow(Base):
    __tablename__ = 'cashflow'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    calc: Mapped[bool] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(nullable=False)
    fiscal_month: Mapped[int] = mapped_column(nullable=False)
    # 内容
    content: Mapped[str] = mapped_column(String(100), nullable=False)
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

    lcategory: Mapped[str] = mapped_column(String(30), primary_key=True)
    budget: Mapped[int] = mapped_column(nullable=True)


def create_database_if_not_exists():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        charset='utf8mb4'
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
        conn.commit()
    finally:
        conn.close()


create_database_if_not_exists()

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
