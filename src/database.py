import psycopg2

def connect_to_database():
    conn=psycopg2.connect(host='localhost',dbname='postgres',user='postgres',password='root',port=5432)
    cur=conn.cursor()

    return conn, cur

def isTableEmpty(cur):
    cur.execute("""
    SELECT * FROM fishes
                """)
    

def create_table(conn, cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS fishes(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    rarity VARCHAR(255),
    drop_chance FLOAT
    )
    """)
    conn.commit()

def fill_table(conn, cur):
    
    cur.execute("""
    INSERT INTO fishes (name, rarity, drop_chance) VALUES
    ('Karp', 'common', 0.6),
    ('Sandacz', 'rare', 0.3),
    ('Węgorz', 'epic', 0.1)
    ON CONFLICT DO NOTHING;
                """)
    conn.commit()

def close_connection(conn, cur):
    cur.close()
    conn.close()