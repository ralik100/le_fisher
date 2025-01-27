import database
import random
import psycopg2

def fishing(cur):

    cur.execute("""
    SELECT * FROM fishes;
                """)
    
    fishes=cur.fetchall()

    total=0

    dic={}

    rand=random.random()

    for fish in fishes:

        total+=fish[3]

        dic[fish[1]]=total

        if rand<=dic[fish[1]]:
            return fish[1], get_fishing_experience(fish[2])


def get_fishing_experience(rarity):

    match rarity:
        case 'common':
            return 1
        case 'rare':
            return 5
        case 'epic':
            return 20
        case 'legendary':
            return 100
        case 'mythic':
            return 500
        case _:
            return 0


def get_rankings(cur):

    cur.execute("""
        SELECT username, experience, total_fishes, rank FROM fishermans ORDER BY experience;
                """)
    
    ranks = cur.fetchall()

    return ranks

def get_fisherman_experience(cur,author_id):

    cur.execute("""
        SELECT experience FROM fishermans where discord_id = %s;
                """, (author_id,))

    exp = cur.fetchone()
    
    return exp[0]

def get_fisherman_rank(cur,author_id):

    cur.execute("""
        SELECT rank FROM fishermans where discord_id = %s;
                """, (author_id,))

    rank = cur.fetchone()
    
    return rank[0]


def get_all_ranks():
    ranks = (
        ('Chwytacz Butelek', 0),
        ('Rybolub', 250),
        ('Król Glonów', 1000),
        ('Władca Kałuży', 10000),
        ('Specjalista od Zaczepów', 50000),
        ('Pan "Coś Dużego Uciekło"', 200000),
        ('Mistrz Niczego', 500000),
        ('Znawca Przynęt, ale nie Ryb', 1000000),
        ('Pogromca Śmieci w Wodzie', 10000000),
        ('Bohater Złowionych Kłód', 100000000)
    )

    return ranks

def get_new_rank(cur, author_id):

    exp = get_fisherman_experience(cur, author_id)
    rank = get_fisherman_rank(cur, author_id)
    ranks = get_all_ranks()



    if rank == ranks[-1][0]:
        return False, rank

    current_rank_index = next(i for i, r in enumerate(ranks) if r[0] == rank)
    for i in range(current_rank_index + 1, len(ranks)):
        if exp < ranks[i][1]: 
            return True, ranks[i - 1][0]

    return False, None
         
def update_fisherman_rank(conn, cur, author_id, new_rank):

    cur.execute("""
        UPDATE fishermans
        SET rank = %s
        where discord_id = %s;
                """, (new_rank, author_id))
    conn.commit()



def add_fisherman(conn, cur, author_id, author_username):


    if not isFishermanExisting(cur,author_id):

        cur.execute("""
            INSERT INTO fishermans (discord_id, username, rank) VALUES
            (%s, %s, 'Chwytacz Butelek')
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