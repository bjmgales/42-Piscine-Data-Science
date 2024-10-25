import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def hide_ticks_frame(ax):
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)


def display_graph_two(conn: object, table_name: str):
    print('\033[93mfetching data from database...\033[0m')
    df = pd.read_sql_query(
        f'''
            SELECT TO_CHAR(event_time AT TIME ZONE 'UTC', 'YYYY-MM')
                AS event_date,
                SUM (price) as daily_income
            FROM {table_name}
            WHERE event_type = 'purchase'
            GROUP by event_date
        ''', conn)

    fig, ax = plt.subplots()
    plt.bar(df['event_date'], df['daily_income'])

    ax.set_xticklabels(['Oct', 'Nov', 'Dec', 'Jan', 'Feb'])

    # remove awful scientific notation indicator from chart
    ax.set_yticklabels([f'{v / 1e6:.1f}' for v in ax.get_yticks()])

    hide_ticks_frame(ax)
    plt.ylabel('total sales in million of ₳')
    plt.xlabel('month')
    plt.show()


def display_graph_one(conn: object, table_name: str):
    print('\033[93mfetching data from database...\033[0m')
    df = pd.read_sql(
        f'''
            SELECT DATE(event_time AT TIME ZONE 'UTC') AS event_date,
                COUNT (DISTINCT user_id) as daily_customer_count
            FROM {table_name}
            WHERE event_type = 'purchase'
            GROUP by event_date
        ''', conn)
    fig, ax = plt.subplots()
    ax.plot(df['event_date'], df['daily_customer_count'])
    plt.ylabel('Number of customers')

    # format YYYY-MM-DD into months
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # remove march from labels
    plt.setp(ax.get_xticklabels()[-1], visible=False)

    # remove ticks and frame
    hide_ticks_frame(ax)
    plt.show()


def fetch_data_to_graph(table_name: str):
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
        display_graph_one(conn, table_name)
        display_graph_two(conn, table_name)
        # display_graph_three(conn, table_name)

    except Exception as e:
        print("\033[91mError: ", e)
        print('\033[93mrollback in progress...\033[0m')
        conn.rollback()
    finally:
        print("\033[95mclosing connection with database...")
        conn.close()
        cursor.close()


if __name__ == '__main__':
    fetch_data_to_graph('customers')
