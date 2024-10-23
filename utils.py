import psycopg2

connect = psycopg2.connect(
    database='piscineds',
    user='bgales',
    password='mysecretpassword',
    host='localhost'
)
cursor = connect.cursor()


def del_all_tables():
    cursor.execute(
        '''
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        '''
    )
    for table in cursor.fetchall():
        cursor.execute(f'DROP TABLE {table[0]} CASCADE;')
        print(f'Deleted {table[0]}')
    connect.commit()


if __name__ == '__main__':
    del_all_tables()