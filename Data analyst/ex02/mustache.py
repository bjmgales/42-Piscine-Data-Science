import psycopg2
import numpy as np
from psycopg2.extras import DictCursor
import matplotlib.pyplot as plt


def hide_ticks_frame():
    plt.tick_params(axis='both', which='both', length=0)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().set_facecolor('#EAEAF2')


def display_info(result: dict, sells_arr):
    result['mean'] = np.mean(sells_arr)
    result['std'] = np.std(sells_arr)
    result['min'] = np.min(sells_arr)
    result['quarter'] = np.percentile(sells_arr, 25)
    result['mean'] = np.percentile(sells_arr, 50)
    result['three_quarter'] = np.percentile(sells_arr, 75)
    result['max'] = np.max(sells_arr)
    print(f'count {result["profit"]}')
    print(f"mean {result['mean']}")
    print(f"std {result['std']}")
    print(f"min {result['min']}")
    print(f"25% {result['quarter']}")
    print(f"50% {result['mean']}")
    print(f"75% {result['three_quarter']}")
    print(f"max {result['max']}")


def display_graph_one(sells_arr: list[int]):
    plt.figure(figsize=(10, 6))
    hide_ticks_frame()
    gray = '#5E5E5E'
    bplot = plt.boxplot(sells_arr, vert=False,
                        medianprops={'color': gray},
                        whiskerprops={'color': gray, 'linewidth': '1.5'},
                        flierprops={'marker': 'd', 'markerfacecolor': gray,
                                    'markeredgecolor': gray},
                        widths=2.0, patch_artist=True)
    for patch in bplot['boxes']:
        patch.set_facecolor(gray)

    plt.xlabel("price")
    plt.yticks([])
    plt.grid(axis='x', color='white', linestyle='-')
    plt.show()


def display_zoomed_graph_one(result: dict, sells_arr: list[int]):
    plt.figure(figsize=(10, 6))
    hide_ticks_frame()
    gray = '#5E5E5E'
    bplot = plt.boxplot(sells_arr, vert=False,
                        medianprops={'color': gray},
                        whiskerprops={'color': gray},
                        flierprops={'marker': 'd', 'markerfacecolor': gray,
                                    'markeredgecolor': gray},
                        widths=2.0, showfliers=False, patch_artist=True)
    for patch in bplot['boxes']:
        patch.set_facecolor('#7DBA7F')
    plt.xlabel("price")
    plt.xlim(-0.5, 12.5)
    plt.yticks([])
    plt.grid(axis='x', color='white', linestyle='-')
    plt.show()


def graph_one(cursor: object):
    print('\033[93mfetching data from database for first graph...\033[0m')
    cursor.execute(
        '''
            SELECT
                (SElECT SUM(price) FROM customers
                    WHERE event_type = 'purchase') AS profit,
                (SELECT COUNT(event_type)
                    FROM customers WHERE event_type = 'purchase')
                        AS nbr_of_purchase
        '''
    )
    result = cursor.fetchone()
    result = dict(result)

    cursor.execute(
        '''
            SELECT price
            FROM customers
            WHERE event_type = 'purchase'
        '''
    )
    sells_arr = np.array(cursor.fetchall())

    display_info(result, sells_arr)
    display_graph_one(sells_arr)
    display_zoomed_graph_one(result, sells_arr)


def fetch_data_display_box(table_name: str):
    try:
        print("\033[95mconnection to database...")
        conn = psycopg2.connect(
            database='piscineds',
            user='bgales',
            password='mysecretpassword',
            host='localhost'
        )
        cursor = conn.cursor(cursor_factory=DictCursor)
        print('\033[92mconnection with database OK')

        cursor.execute('BEGIN;')
        graph_one(cursor)
    except Exception as e:
        print("\033[91mError: ", e)
        print('\033[93mrollback in progress...\033[0m')
        conn.rollback()
    finally:
        print("\033[95mclosing connection with database...")
        conn.close()
        cursor.close()


if __name__ == '__main__':
    fetch_data_display_box('customers')
