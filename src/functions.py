import database

def fishing(cur):

    cur.execute("""
    SELECT * FROM fishes;
                """)
    fishes=cur.fetchall()

    return fishes