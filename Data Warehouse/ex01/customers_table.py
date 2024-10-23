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


def create_new_table(cursor: object, table_name: str, files: list[str]):
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

    cursor.execute(
        '''
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name like 'data_20%'
        '''
    )
    tables = cursor.fetchall()
    for t in tables:
        print(f'\033[93mcopying {t[0]} to customer table...')
        cursor.execute(
            f'''
            INSERT INTO {table_name}
                SELECT * FROM {t[0]}
        '''
        )
        print('\033[92mcopy success!')


def data_csv_to_db(dir_path: str):
    '''
    Reads data from a csv file formated with precise headers.

    If the data matches the table format, the csv will be put
    inside a created or existing db table named $file_path (- extension)


            Parameter:
                @file_path(str): the path to the csv file.
    '''

    try:
        files = []
        for file in os.listdir(dir_path):
            files.append(dir_path + file)

        print("\033[95mconnection to database...")
        connection = psycopg2.connect(
            database="piscineds",
            user="bgales",
            password="mysecretpassword",
            host='localhost'
        )
        print('\033[92mconnection with database OK')

        cursor = connection.cursor()
        cursor.execute("BEGIN;")

        table_name = 'customers'
        if is_table_existing(cursor, table_name) is False:
            create_new_table(cursor, table_name, files)
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


if __name__ == "__main__":
    dir_path = 'subject/customer/'
    data_csv_to_db(dir_path)
