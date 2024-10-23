import psycopg2
import os


def is_table_existing(cursor: object, table_name: str):
    cursor.execute(f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = '{table_name}'
        );
    """)
    return cursor.fetchone()[0]


def create_new_table(cursor: object, table_name: str, file_path: str):
    print(f'\033[93mcreating table {table_name}...')
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
    print(f'\033[92mtable {table_name} created with success!')
    with open(file_path, 'r') as csv_buf:
        print(f'\033[93mcopying {file_path} into {table_name}...')
        next(csv_buf)
        cursor.copy_from(csv_buf, table_name, sep=',')
        print('\033[92mcopy made with success!')

    csv_buf.close()


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
        print("\033[95mconnection to database...")
        connection = psycopg2.connect(
            database="piscineds",
            user="bgales",
            password="mysecretpassword",
            host='localhost'
        )
        print('\033[92mconnection with database OK')
        cursor = connection.cursor()
        cursor.execute('BEGIN;')

        if is_table_existing(cursor, table_name) is False:
            create_new_table(cursor, table_name, file_path)
            print('\033[93mcomitting changes...')
            connection.commit()
            print("\033[92mcommited with success!")

        else:
            print(f'\033[93mtable {table_name} already exists.')

    except Exception as e:
        print("\033[91mError :", e)
        print('\033[93mrollback in progress...\033[0m')
        connection.rollback()

    finally:
        print("\033[95mclosing connection with database...")
        connection.close()
        cursor.close()


def csv_path(dir_path):

    for filename in os.listdir(dir_path):
        if filename.endswith('csv'):
            data_csv_to_db(dir_path + filename)


if __name__ == "__main__":
    dir_path = 'subject/customer/'
    csv_path(dir_path)
