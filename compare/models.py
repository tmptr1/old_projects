from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import REAL, NUMERIC, String, Uuid, text, Integer, Numeric, Index, Boolean
from typing import Annotated

class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(primary_key=True)]
str_x = lambda x:Annotated[String, mapped_column(String(x), nullable=True)]
intgr = Annotated[int, mapped_column(Integer, nullable=True)]
real = Annotated[REAL, mapped_column(REAL, nullable=True)]
numeric = Annotated[Numeric, mapped_column(Numeric(12, 2), nullable=True)]

class Total_new(Base):
    __tablename__ = "total_new"
    __table_args__ = (Index("total_new_article_brand_supplier_code_index", "_01article", "_02brand", "_07supplier_code"),)

    id: Mapped[intpk]
    article_s: Mapped[str_x(256)]
    brand_s: Mapped[str_x(256)]
    _01article: Mapped[str_x(256)]
    _02brand: Mapped[str_x(256)]
    _03name: Mapped[str_x(256)]
    count: Mapped[intgr]
    _05price: Mapped[numeric]
    _06mult: Mapped[intgr]
    _07supplier_code: Mapped[str_x(20)]
    _14brand_filled_in: Mapped[str_x(256)]
    _20exclude: Mapped[str_x(50)]

class Total_old(Base):
    __tablename__ = "total_old"
    __table_args__ = (Index("total_old_article_brand_supplier_code_index", "_01article", "_02brand", "_07supplier_code"),)

    id: Mapped[intpk]
    article_s: Mapped[str_x(256)]
    brand_s: Mapped[str_x(256)]
    _01article: Mapped[str_x(256)]
    _02brand: Mapped[str_x(256)]
    _03name: Mapped[str_x(500)]
    count: Mapped[real] # diff type
    _05price: Mapped[numeric]
    _06mult: Mapped[real] # diff type
    _07supplier_code: Mapped[str_x(20)]
    _14brand_filled_in: Mapped[str_x(256)]
    _20exclude: Mapped[str_x(50)]

class Total(Base):
    __tablename__ = "total"
    __table_args__ = (Index("total_article_brand_supplier_code_index", "_01article_1", "_02brand_1", "_07supplier_code"),)
    # 1 - old, 2 - new
    id: Mapped[intpk]
    new_row: Mapped[str_x(5)]
    article_s_1: Mapped[str_x(256)]
    article_s_2: Mapped[str_x(256)]
    article_s_c: Mapped[str_x(5)]
    brand_s_1: Mapped[str_x(256)]
    brand_s_2: Mapped[str_x(256)]
    brand_s_c: Mapped[str_x(5)]
    _01article_1: Mapped[str_x(256)]
    _01article_2: Mapped[str_x(256)]
    _01article_c: Mapped[str_x(5)]
    _02brand_1: Mapped[str_x(256)]
    _02brand_2: Mapped[str_x(256)]
    _02brand_c: Mapped[str_x(5)]
    _03name_1: Mapped[str_x(500)]
    _03name_2: Mapped[str_x(500)]
    _03name_c: Mapped[str_x(5)]
    count_1: Mapped[intgr]
    count_2: Mapped[real]  # diff
    count_c: Mapped[str_x(5)]
    _05price_1: Mapped[numeric]
    _05price_2: Mapped[numeric]
    _05price_c: Mapped[real]
    _06mult_1: Mapped[intgr]
    _06mult_2: Mapped[real]  # diff
    _06mult_c: Mapped[str_x(5)]
    _07supplier_code: Mapped[str_x(20)]
    _14brand_filled_in_1: Mapped[str_x(256)]
    _14brand_filled_in_2: Mapped[str_x(256)]
    _14brand_filled_in_c: Mapped[str_x(5)]
    # _20exclude_1: Mapped[str_x(50)]
    # _20exclude_2: Mapped[str_x(50)]
    # _20exclude_c: Mapped[str_x(5)]

class Count_Table(Base):
    __tablename__ = "count_table"
    # __table_args__ = (Index("total_article_brand_supplier_code_index", "article_s_2", "brand_s_2", "_07supplier_code"),)
    id: Mapped[intpk]
    _07supplier_code: Mapped[str_x(20)]
    count_1: Mapped[intgr]
    count_2: Mapped[intgr]
    diff: Mapped[REAL] = mapped_column(REAL, nullable=True, default=-1)

