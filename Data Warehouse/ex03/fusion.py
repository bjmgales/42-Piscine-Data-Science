import psycopg2


def table_fusion():

    try:
        connection = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost'
            )
        cursor = connection.cursor()
        # cursor.execute(
        #     '''
        #         CREATE TABLE c_tmp AS
        #         SELECT * FROM customers
        #         WHERE 1 = 0
        #     '''
        # )

        # cursor.execute(
        #     '''
        #         ALTER TABLE c_tmp
        #         ADD category_id BIGINT,
        #         ADD category_code TEXT,
        #         ADD brand TEXT
        #     '''
        # )
        # print('c_tmp table created...', cursor.fetchone())

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

        print('tmp_item table created... duplicates and uncomplete removed')

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
                    customers.category_id, customers.category_code,
                    customers.brand, tmp_i.category_id, tmp_i.category_code, tmp_i.brand
            '''
        )
        cursor.execute(
            '''
                DROP TABLE customers
            '''
        )
        cursor.execute(
            '''
                ALTER TABLE c_tmp
                RENAME TO customers
            '''
        )
        print('customers table re-created with updates from item')

        # cursor.execute(
        #     '''
        #         UPDATE customers
        #         SET category_id = item.category_id,
        #             category_code = item.category_code,
        #             brand = item.brand
        #         FROM item
        #         WHERE customers.product_id = item.product_id
        #     '''
        # )
        # cursor.execute(
        #     '''
        #         INSERT INTO customers (product_id, category_id, category_code,
        #         brand)
        #         SELECT * FROM item
        #         LEFT JOIN customers ON customers.product_id = item.product_id
        #         WHERE custom.product_id IS NULL
        #     '''
        # )
        connection.commit()

    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    table_fusion()