import database
import random

def fishing(cur):

    cur.execute("""
    SELECT * FROM fishes;
                """)
    
    fishes=cur.fetchall()

    total=0

    dic={}

    rand=random.random()

    print(rand)

    print(fishes)

    for fish in fishes:

        total+=fish[3]

        print(fish)

        dic[fish[1]]=total

        if rand<=dic[fish[1]]:
            return fish[1]
