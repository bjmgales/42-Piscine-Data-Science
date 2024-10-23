import psycopg2


def table_fusion():

    try:
        print("\033[95mconnection to database...")
        connection = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost'
            )
        cursor = connection.cursor()
        print('\033[92mconnection with database OK')
        cursor.execute('BEGIN;')
        print('\033[93mcreating backup table for customers...')
        cursor.execute('CREATE TABLE backup_customers AS TABLE customers;')
        print('\033[92mbackup table created with success!')

        print('\033[93mcreating ready-for-merge tmp_item table...')
        cursor.execute(
            '''
                CREATE TEMP TABLE temp_item(
                product_id BIGINT,
                category_id TEXT,
                category_code TEXT,
                brand TEXT)
            '''
        )
        cursor.execute(
            '''
                INSERT INTO temp_item
                SELECT
                    product_id,
                        string_agg(DISTINCT item.category_id::TEXT, ', ')
                            FILTER (WHERE item.category_id IS NOT NULL)
                            AS category_id,
                        string_agg(DISTINCT item.category_code::TEXT, ', ')
                            FILTER (WHERE item.category_id IS NOT NULL)
                            AS category_code,
                        string_agg (DISTINCT item.brand::TEXT, ', ')
                            FILTER (WHERE item.brand IS NOT NULL)
                            AS brand
                FROM
                    public.item
                GROUP BY
                    product_id;
            '''
        )
        print('\033[92mtmp_item table created with success!')
        print('\033[93mcreating c_tmp table from customers...\n\
updating customers rows with tmp_item\'s...')
        cursor.execute(
            '''
                CREATE TABLE c_tmp AS
                    SELECT customers.product_id,
                            customers.event_type,
                            customers.event_time,
                            customers.price,
                            customers.user_id,
                            customers.user_session,
                           tmp_i.category_id,
                           tmp_i.category_code,
                           tmp_i.brand
                FROM customers
                LEFT JOIN
                    (SELECT DISTINCT
                        product_id,
                        category_id,
                        category_code,
                        brand
                        FROM temp_item
                    ) AS tmp_i
                ON customers.product_id = tmp_i.product_id
                GROUP BY customers.product_id, customers.event_type,
                    customers.event_time, customers.price,
                    customers.user_id, customers.user_session,
                    tmp_i.category_id, tmp_i.category_code, tmp_i.brand
            '''
        )
        print('\033[93mcounting rows from c_tmp to ensure \
data integrity...')
        cursor.execute('SELECT COUNT(*) FROM c_tmp;')
        print('\033[93mcounting rows from original customers table to \
ensure data integrity...')
        c_tmp_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM customers;')
        customer_count = cursor.fetchone()[0]

        if c_tmp_count != customer_count:
            raise Exception('c_tmp data corrupted...')

        print('\033[92mc_tmp table created with success!')

        print('\033[91mdeleting backup_table...')
        cursor.execute(
            '''
                DROP TABLE backup_customers
            '''
        )
        print('\033[92mbackup_customers table deleted with success!')
        print('\033[91mdeleting customers table...')
        cursor.execute(
            '''
                DROP TABLE customers
            '''
        )
        print('\033[92mcustomers table deleted with success!\n\
\033[93mrenaming c_tmp to \"customers\"')
        cursor.execute(
            '''
                ALTER TABLE c_tmp
                RENAME TO customers
            '''
        )
        print('\033[93mcomitting changes...')
        connection.commit()
        print("\033[92mcommited with success!")

    except Exception as e:
        print(f'\033[91mError: {e}')
        print('\033[93mrollback in progress...\033[0m')
        connection.rollback()
    finally:
        print("\033[95mclosing connection with database...")
        cursor.close()
        connection.close()


if __name__ == '__main__':
    table_fusion()
