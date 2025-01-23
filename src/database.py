import psycopg2

def connect_to_database():
    conn=psycopg2.connect(host='localhost',dbname='postgres',user='postgres',password='root',port=5432)
    cur=conn.cursor()

    return conn, cur

def isTableEmpty(cur,dbname):

    cur.execute(f"""
    SELECT * FROM {dbname}
                """)
    
    values=cur.fetchall()
    return values==[]

def create_fish_table(conn, cur):

    cur.execute("""CREATE TABLE IF NOT EXISTS fishes(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        rarity VARCHAR(255),
        drop_chance FLOAT
        )
        """)
    conn.commit()

def fill_fish_table(conn, cur):
    
    if isTableEmpty(cur, 'fishes'):
        cur.execute("""
            INSERT INTO fishes (name, rarity, drop_chance) VALUES
            ('Karp', 'common', 0.7),
            ('Sandacz', 'rare', 0.2),
            ('Węgorz', 'epic', 0.05),
            ('Leszcz', 'legendary', 0.02),
            ('Okoń jasnogórski', 'legendary', 0.025),
            ('Karaś ludojad', 'mythic', 0.005)
            ON CONFLICT DO NOTHING;
            """)
        
        conn.commit()

    else:
        print(f'table is filled')

def close_connection(conn, cur):
    print('connection is closed')
    cur.close()
    conn.close()