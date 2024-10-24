import psycopg2
import numpy as np
import matplotlib.pyplot as plt


def fetch_data_piechart(table_name: str):
    try:
        print("\033[95mconnection to database...")
        conn = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost'
        )
        cursor = conn.cursor()
        print('\033[92mconnection with database OK')
        cursor.execute('BEGIN;')

        print('\033[93mfetching data from database...')

        cursor.execute(
            f'''
                SELECT COUNT(event_type), event_type FROM {table_name}
                GROUP BY event_type

            '''
        )
        print('\033[92mdata fetched with success!')
        fetch_data = cursor.fetchall()
        print('\033[0m', fetch_data)

        label = []
        y = np.array([])
        for count, event_type in fetch_data:
            y = np.append(y, count)
            label.append(event_type)

        plt.pie(y, labels=[event_type for c, event_type in fetch_data],
                autopct='%1.1f%%')
        plt.show()

    except Exception as e:
        print("\033[91mError: ", e)
        print('\033[93mrollback in progress...\033[0m')
        conn.rollback()
    finally:
        print("\033[95mclosing connection with database...")
        conn.close()
        cursor.close()


if __name__ == '__main__':
    fetch_data_piechart('customers')
