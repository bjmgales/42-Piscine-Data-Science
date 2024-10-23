import psycopg2


def create_tmp_table_replace_old(cursor: object, connection: object):
    cursor.execute('''
        CREATE TABLE temp_table (LIKE customers INCLUDING ALL);
    ''')

    cursor.execute('''
        INSERT INTO temp_table SELECT DISTINCT * FROM customers;
    ''')

    cursor.execute('''
        DROP TABLE customers;
    ''')

    cursor.execute('''
        ALTER TABLE temp_table RENAME TO customers;
    ''')
    connection.commit()


def rem_duplicate_sql_table():
    try:
        connection = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost',
        )
        cursor = connection.cursor()
        create_tmp_table_replace_old(cursor, connection)
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error : {e}")
        return


if __name__ == '__main__':
    rem_duplicate_sql_table()