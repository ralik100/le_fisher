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

def create_fisherman_table(conn, cur):

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fishermans(
        id SERIAL PRIMARY KEY,
        discord_id VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(255),
        experience INT DEFAULT 0,
        total_fishes INT DEFAULT 0
        );
        """)
    conn.commit()


def add_fisherman(conn, cur, author_id, author_username):


    if not isFishermanExisting(cur,author_id):

        cur.execute("""
            INSERT INTO fishermans (discord_id, username) VALUES
            (%s, %s)
            ON CONFLICT DO NOTHING;
                    """, (author_id, author_username))
        conn.commit()


def isFishermanExisting(cur, author_id):

    cur.execute("""
        SELECT * FROM fishermans where discord_id = %s;
                """, (author_id,))

    fisherman = cur.fetchall()

    return fisherman != []

def fisherman_gain_experience(conn, cur, author_id, experience):

    if isFishermanExisting(cur, author_id):
        cur.execute("""
            UPDATE fishermans
            SET experience = experience + %s,
                total_fishes = total_fishes + 1
            WHERE discord_id = %s;
        """, (experience, author_id))  

        conn.commit()

def close_connection(conn, cur):
    print('connection is closed')
    cur.close()
    conn.close()