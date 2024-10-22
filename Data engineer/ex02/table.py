import psycopg2
import os


def create_new_table(cursor: object, table_name: str, file_path: str):
    table_creation = f'''
           CREATE TABLE {table_name} (
           event_time TIMESTAMPTZ,
           event_type TEXT,
           product_id BIGINT,
           price DOUBLE PRECISION,
           user_id BIGINT,
           user_session TEXT
       )
       '''
    cursor.execute(table_creation)
    with open(file_path, 'r') as csv_buf:
        next(csv_buf)
        cursor.copy_from(csv_buf, table_name, sep=',')
    csv_buf.close()


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
    file_path = 'subject/customer/'
    data_csv_to_db(file_path + 'data_2022_oct.csv')
