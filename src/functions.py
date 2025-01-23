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
        SELECT username, experience, total_fishes FROM fishermans ORDER BY experience;
                """)
    
    ranks = cur.fetchall()

    return ranks