import psycopg2


def remove_february():
    try:
        connect = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost'
        )
        cursor = connect.cursor()
        cursor.execute(
            '''
                DELETE FROM customers
                WHERE event_time::date >= '2023-02-01'
            '''
        )
        connect.commit()
    except Exception as e:
        print(f'Error:{e}')
        connect.rollback()
    finally:
        cursor.close()
        connect.close()


if __name__ == '__main__':
    remove_february()
