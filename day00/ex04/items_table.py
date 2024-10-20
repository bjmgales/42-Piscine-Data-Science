import os
import pandas as pd
import numpy as np
import psycopg2
from io import StringIO


def create_new_table(cursor: object, table_name: str, file_path: str):
    table_creation = f'''
           CREATE TABLE {table_name} (
           product_id INT,
           category_id BIGINT,
           category_code TEXT,
           brand TEXT
       )
       '''
    cursor.execute(table_creation)
    # Create a fake file to replace empty row with NaN for pandas .to_csv() #
    # then na_rep='\\N' to remplace NaN to NULL for postgresql #
    df = pd.read_csv(file_path)
    df.replace('', np.nan)
    fake_file = StringIO()
    df.to_csv(fake_file, sep=',', index=False, header=False,
              float_format='%.0f', na_rep='\\N')
    fake_file.seek(0)
    cursor.copy_from(fake_file, table_name, sep=',')
    fake_file.close()


def is_table_existing(cursor: object, table_name: str):
    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = '{table_name}'
        );
    """)
    return cursor.fetchone()[0]


def data_csv_to_db(file_path: str):
    '''
    Reads data from a csv file formated with precise headers.

    If the data matches the table format, the csv will be put
    inside a created or existing db table named $file_path (- extension)


            Parameter:
                @file_path(str): the path to the csv file.
    '''

    try:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        connection = psycopg2.connect(
            database="piscineds",
            user="bgales",
            password="mysecretpassword",
            host='localhost'
        )
        cursor = connection.cursor()

        if is_table_existing(cursor, table_name) is False:
            print(f'table {table_name} does not exists. Creating table...')
            create_new_table(cursor, table_name, file_path)
            connection.commit()
        else:
            print(f'table {table_name} already exists.')

        connection.close()
        cursor.close()
    except Exception as e:
        print("Error :", e)
    return


if __name__ == "__main__":
    file_path = 'subject/item/'
    data_csv_to_db(file_path + 'item.csv')
