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

    cursor.execute(
        '''
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name like 'data_20%'
        '''
    )
    tables = cursor.fetchall()
    for t in tables:
        print(t)
        cursor.execute(
            f'''
            INSERT INTO {table_name}
                SELECT * FROM {t[0]}
        '''
        )


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

        connection = psycopg2.connect(
            database="piscineds",
            user="bgales",
            password="mysecretpassword",
            host='localhost'
        )
        cursor = connection.cursor()

        table_name = 'customers'
        if is_table_existing(cursor, table_name) is False:
            print(f"table {table_name} not existing. Creating table...")
            create_new_table(cursor, table_name, files)
            connection.commit()
        else:
            print(f"table {table_name} already exists.")

        connection.close()

    except Exception as e:
        print("Error :", e)
    return


if __name__ == "__main__":
    dir_path = 'subject/customer/'
    data_csv_to_db(dir_path)
