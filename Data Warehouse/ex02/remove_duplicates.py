import psycopg2


def create_tmp_table_replace_old(cursor: object, connection: object):
    print('\033[93mremoving duplicates and server lags from customers before \
insertion into temp_table...')
    cursor.execute('''
       CREATE TABLE temp_table AS WITH _ AS(
            SELECT *,
               LEAD(event_time) OVER
               (PARTITION BY event_type, product_id,
               price, user_id, user_session ORDER BY event_time)
               AS next_time,
               LEAD(event_type) OVER
               (PARTITION BY event_type, product_id,
               price, user_id, user_session ORDER BY event_time)
               AS next_type,
               LEAD(product_id) OVER
               (PARTITION BY event_type, product_id,
               price, user_id, user_session ORDER BY event_time)
               AS next_product,
               LEAD(price) OVER
               (PARTITION BY event_type, product_id,
               price, user_id, user_session ORDER BY event_time)
               AS next_price,
               LEAD(user_id) OVER
               (PARTITION BY event_type, product_id,
               price, user_id, user_session ORDER BY event_time)
               AS next_user,
               LEAD(user_session) OVER
               (PARTITION BY event_type, product_id,
               price, user_id, user_session ORDER BY event_time)
               AS next_session
               FROM customers
            )
            SELECT * FROM _
            WHERE (event_time IS NULL OR
                (next_time - event_time) > INTERVAL '1 second' OR
                event_type IS DISTINCT FROM next_type OR
                product_id IS DISTINCT FROM next_product OR
                price IS DISTINCT FROM next_price OR
                user_id IS DISTINCT FROM next_user OR
                user_session IS DISTINCT FROM next_session)
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
