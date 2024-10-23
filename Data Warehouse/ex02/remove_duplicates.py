import psycopg2


def create_tmp_table_replace_old(cursor: object, connection: object):
    print('\033[93mcreating table temp_table with customers table\
 structure...')
    cursor.execute('''
        CREATE TABLE temp_table (LIKE customers INCLUDING ALL);
    ''')
    print('\033[92mtable temp_table created with success!')

    print('\033[93minserting distinct rows from customers \
into temp_table...')
    cursor.execute('''
        INSERT INTO temp_table SELECT DISTINCT * FROM customers;
    ''')
    print('\033[92minserted with success!')

    print('\033[91mdeleting customers table...')
    cursor.execute('''
        DROP TABLE customers;
    ''')
    print('\033[92mcustomers table deleted with success!\n\
\033[93m renaming temp_table to \"customers\"')
    cursor.execute('''
        ALTER TABLE temp_table RENAME TO customers;
    ''')


def del_dup_rows():
    try:
        print("\033[95mconnection to database...")
        connection = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost',
        )
        print('\033[92mconnection with database OK')
        cursor = connection.cursor()
        cursor.execute("BEGIN;")
        create_tmp_table_replace_old(cursor, connection)
        print('\033[93mcomitting changes...')
        connection.commit()
        print("\033[92mcommited with success!")

    except Exception as e:
        print("\033[91mError :", e)
        print('\033[93mrollback in progress...\033[0m')
        connection.rollback()
    finally:
        print("\033[95mclosing connection with database...")
        connection.close()
        cursor.close()


if __name__ == '__main__':
    del_dup_rows()
