import pandas as pd
from sqlalchemy import create_engine, text, URL, insert, select, update, and_, or_, func, distinct, union
from sqlalchemy.orm import sessionmaker
import psycopg2
import datetime
import os
import math
from models import Base, Total_new, Total_old, Total, Count_Table

row_limit = 100_000

url = URL.create("postgresql+psycopg2", username='postgres', password='pass', host='127.0.0.1',
                 database='compare_total')
engine = create_engine(url)
session = sessionmaker(engine)

path_old = r"D:\Documents\total_price_compare\total 1\Страница {}.csv"
path_new = r"D:\Documents\price processing 2\catalogs\Итог\Итог - страница {}.csv"
path_to_compare = r"D:\Documents\total_price_compare\compare\Сравнение - страница {}.csv"

def load_totals_to_db(sess):
    total_load = 0
    for i in range(1, 5):
        loaded = 1
        while True:
            try:
                df = pd.read_csv(path_new.format(i), header=None, sep=';', encoding='windows-1251', nrows=row_limit,
                                 skiprows=loaded,
                                 encoding_errors='ignore', usecols=[1, 2, 8, 9, 10, 11, 13, 17, 22, 36, 38, ])
            except pd.errors.EmptyDataError:
                break
            # usecols=['Артикул поставщика', 'Производитель поставщика', '01Артикул', '02Производитель', '03Наименование',
            # 'Кол-во', '05Цена', '07Код поставщика', '14Производитель заполнен', '06Кратность', '20ИслючитьИзПрайса'])
            # {'Артикул поставщика': 'article_s', 'Производитель поставщика': 'brand_s', '01Артикул': '_01article',
            # '02Производитель': '_02brand', '03Наименование': '_03name', 'Кол-во': 'count', '05Цена': '_05price',
            # '07Код поставщика': '_07supplier_code', '14Производитель заполнен': '_14brand_filled_in', '06Кратность':
            # '_06mult', '20ИслючитьИзПрайса': '_20exclude'})
            # columns={'1': 'article_s', '2': 'brand_s', '8': '_01article', '9': '_02brand', '10': '_03name',
            #                                         '36': 'count', '11': '_05price', '13': '_07supplier_code', '17': '_14brand_filled_in',
            #                                         '38': '_06mult', '22': '_20exclude'})
            loaded += len(df)
            df = df.rename(columns={1: 'article_s', 2: 'brand_s', 8: '_01article', 9: '_02brand', 10: '_03name',
                                    36: 'count', 11: '_05price', 13: '_07supplier_code', 17: '_14brand_filled_in',
                                    38: '_06mult', 22: '_20exclude'})
            # print(len(df))
            df.to_sql(name='total_new', con=sess.connection(), if_exists='append', index=False,
                      index_label=False)  # , chunksize=row_limit)
        print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] (1) Страница {i} загружена")
        total_load += loaded - 1
    print(f"Всего загружено: {total_load}")

    total_load = 0
    for i in range(1, 5):
        loaded = 1
        while True:
            try:
                df = pd.read_csv(path_old.format(i), header=None, sep=';', encoding='windows-1251', nrows=row_limit,
                                 skiprows=loaded,
                                 encoding_errors='ignore', usecols=[1, 2, 8, 9, 10, 11, 13, 17, 22, 37, 39, ])
            except pd.errors.EmptyDataError:
                break

            loaded += len(df)
            df = df.rename(columns={1: 'article_s', 2: 'brand_s', 8: '_01article', 9: '_02brand', 10: '_03name',
                                    37: 'count', 11: '_05price', 13: '_07supplier_code', 17: '_14brand_filled_in',
                                    39: '_06mult', 22: '_20exclude'})
            dgt_cols = ['count', '_05price', '_06mult']
            for c in dgt_cols:
                df[c] = df[c].apply(to_float)

            df.to_sql(name='total_old', con=sess.connection(), if_exists='append', index=False,
                      index_label=False)  # , chunksize=row_limit)
        print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] (2) Страница {i} загружена")
        total_load += loaded - 1

    print(f"Всего загружено: {total_load}")
    sess.query(Total_old).where(Total_old._20exclude != None).delete()
    sess.query(Total_new).where(Total_new._20exclude != None).delete()

def main():
    print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] Начало")
    try:
        with session() as sess:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)

            sess.query(Total_new).delete()
            sess.query(Total_old).delete()
            sess.query(Total).delete()
            sess.query(Count_Table).delete()
            sess.execute(text(f"ALTER SEQUENCE total_new_id_seq restart 1"))
            sess.execute(text(f"ALTER SEQUENCE total_old_id_seq restart 1"))
            sess.execute(text(f"ALTER SEQUENCE total_id_seq restart 1"))
            sess.execute(text(f"ALTER SEQUENCE count_table_id_seq restart 1"))

            load_totals_to_db(sess)
            sess.commit()

            print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] Сравнение...")
            # загрузить Total_old в Total, обновить _1
            sess.execute(insert(Total).from_select(['article_s_1', 'brand_s_1', '_01article_1', '_02brand_1', '_03name_1',
                                                    'count_1', '_05price_1', '_06mult_1', '_07supplier_code',
                                                    '_14brand_filled_in_1'], select(Total_old.article_s, Total_old.brand_s,
                                                    Total_old._01article, Total_old._02brand, Total_old._03name, Total_old.count,
                                                    Total_old._05price, Total_old._06mult, Total_old._07supplier_code,
                                                    Total_old._14brand_filled_in)))

            # сравнить по артикул + бренд + 07, обновить _2
            sess.execute(update(Total).where(and_(Total._01article_1==Total_new._01article, Total._02brand_1==Total_new._02brand,
                                                  Total._07supplier_code==Total_new._07supplier_code)).
                         values(article_s_2=Total_new.article_s, brand_s_2=Total_new.brand_s, _01article_2=Total_new._01article,
                                _02brand_2=Total_new._02brand, _03name_2=Total_new._03name, count_2=Total_new.count,
                                _05price_2=Total_new._05price, _06mult_2=Total_new._06mult, _14brand_filled_in_2=Total_new._14brand_filled_in))
            # у прайсов с артикул_2 == None в Total указать new_row = 'not found'
            sess.execute(update(Total).where(Total.article_s_2 == None).values(new_row='нет'))
            # обновить поля _c
            sess.execute(update(Total).where(and_(Total.new_row==None, Total.article_s_1 != Total.article_s_2)).values(article_s_c='-'))
            sess.execute(update(Total).where(and_(Total.new_row==None, Total.brand_s_1 != Total.brand_s_2)).values(brand_s_c='-'))
            # sess.execute(update(Total).where(and_(Total.new_row==None, Total._01article_1 != Total._01article_2)).values(_01article_c='-'))
            # sess.execute(update(Total).where(and_(Total.new_row==None, Total._02brand_1 != Total._02brand_2)).values(_02brand_c='-'))
            sess.execute(update(Total).where(and_(Total.new_row==None, Total._03name_1 != Total._03name_2)).values(_03name_c='-'))
            sess.execute(update(Total).where(and_(Total.new_row==None, Total.count_1 != Total.count_2)).values(count_c='-'))
            sess.execute(update(Total).where(and_(Total.new_row==None, Total._05price_1 != Total._05price_2)).values(_05price_c=1 - Total._05price_1/Total._05price_2))
            sess.execute(update(Total).where(and_(Total.new_row==None, Total._06mult_1 != Total._06mult_2)).values(_06mult_c='-'))
            sess.execute(update(Total).where(and_(Total.new_row==None, Total._14brand_filled_in_1 != Total._14brand_filled_in_2)).values(_14brand_filled_in_c='-'))

            sess.execute(update(Total).where(or_(Total.article_s_c != None, Total.brand_s_c != None, Total._03name_c != None,
                                                 Total.count_c != None, Total._05price_c != None, Total._06mult_c != None,
                                                 Total._14brand_filled_in_c != None)).values(new_row='-'))

            # для отчёта
            req = sess.execute(select(distinct(Total_old._07supplier_code)).union(select(distinct(Total_new._07supplier_code))))
            res = req.scalars().all()
            # print(res)
            # sess.execute(insert(Count_Table).from_select('_07supplier_code', req))
            vals = [{'_07supplier_code': i} for i in res]
            sess.execute(insert(Count_Table).values(vals))
            sess.execute(update(Count_Table).values(count_1=select(func.count()).
                                                    where(Total_old._07supplier_code==Count_Table._07supplier_code)))
            sess.execute(update(Count_Table).values(count_2=select(func.count()).
                                                    where(Total_new._07supplier_code==Count_Table._07supplier_code)))

            # добавить новые поля из Total_new (20 код уже удалён):
            sess.query(Total_new).where(and_(Total._01article_1==Total_new._01article, Total._02brand_1==Total_new._02brand,
                                                  Total._07supplier_code==Total_new._07supplier_code)).delete()

            #   update set mark = '+' from total_new where 01+02+07 == total 01+02+07(_2)
            sess.execute(insert(Total).from_select(['new_row', 'article_s_2', 'brand_s_2', '_01article_2', '_02brand_2',
                                                    '_03name_2', 'count_2', '_05price_2', '_06mult_2', '_07supplier_code',
                                                    '_14brand_filled_in_2'], select(func.concat('new'), Total_new.article_s, Total_new.brand_s,
                                                    Total_new._01article, Total_new._02brand, Total_new._03name, Total_new.count,
                                                    Total_new._05price, Total_new._06mult, Total_new._07supplier_code,
                                                    Total_new._14brand_filled_in)))
            #   where mark == None add to Total, new_row = 'new'
            total_cnt = sess.execute(select(func.count()).select_from(Total)).scalar()
            print(f"Итог: {total_cnt}")

            sess.commit()

            print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] Формирование csv...")
            report_parts_count = 10
            limit = 1_048_500
            loaded = 0
            for i in range(1, report_parts_count + 1):
                df = pd.DataFrame(columns=["Статус", "Артикул поставщика (старое)", "Артикул поставщика (новое)",
                                           "Производитель поставщика (старое)", "Производитель поставщика (новое)",
                                           "01Артикул (старое)", "01Артикул (новое)", "01Артикул (отличие)",
                                           "02Производитель (старое)", "02Производитель (новое)", "02Производитель (отличие)",
                                           "03Наименование (старое)", "03Наименование (новое)", "03Наименование (отличие)",
                                           "Кол-во (старое)", "Кол-во (новое)", "Кол-во (отличие)",
                                           "05Цена (старое)", "05Цена (новое)", "05Цена (отличие)",
                                           "06Кратность (старое)", "06Кратность (новое)", "06Кратность (отличие)",
                                           "07Код поставщика",
                                           "14Производитель заполнен (старое)", "14Производитель заполнен (новое)",
                                           "14Производитель заполнен (отличие)",])
                df.to_csv(path_to_compare.format(i), sep=';', decimal='.', encoding="windows-1251", index=False, errors='ignore')
                req = select(Total.new_row, Total.article_s_1, Total.article_s_2, Total.brand_s_1, Total.brand_s_2,
                             Total._01article_1, Total._01article_2, Total._01article_c, Total._02brand_1,
                             Total._02brand_2, Total._02brand_c, Total._03name_1, Total._03name_2, Total._03name_c,
                             Total.count_1, Total.count_2, Total.count_c, Total._05price_1, Total._05price_2,
                             Total._05price_c, Total._06mult_1, Total._06mult_2, Total._06mult_c, Total._07supplier_code,
                             Total._14brand_filled_in_1, Total._14brand_filled_in_2, Total._14brand_filled_in_c,
                             ).order_by(Total.id).offset(loaded).limit(limit)
                df = pd.read_sql_query(req, sess.connection(), index_col=None)

                df.to_csv(path_to_compare.format(i), mode='a', sep=';', decimal='.', encoding="windows-1251", index=False,
                          header=False, errors='ignore')

                df_len = len(df)
                loaded += df_len


            sess.execute(update(Count_Table).values(diff=1-Count_Table.count_1/Count_Table.count_2).where(Count_Table.count_2 > 0))
            sess.commit()

            req = select(Count_Table._07supplier_code.label("Код прайса"),
                         Count_Table.count_1.label("Кол-во позиций (старый итог)"),
                         Count_Table.count_2.label("Кол-во позиций (новый итог)"),
                         Count_Table.diff.label("Разница в процентах"),)
            df = pd.read_sql(req, engine)
            df.to_csv(fr"{os.getcwd()}/count_report.csv", sep=';', encoding="windows-1251", index=False, header=True, errors='ignore')


    except Exception as ex:
        print('ERROR')
        # print(ex)
        raise ex

    print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] Готово")
    # input()

def to_float(x):
    try:
        x = float(str(x).replace(',', '.'))
        if math.isnan(x) or math.isinf(x):
            return 0
        if 1E+37 < x < 1E-37:  # real
            return 0
        return x
    except:
        return 0

if __name__ == '__main__':
    main()