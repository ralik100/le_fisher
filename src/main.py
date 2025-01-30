import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import database
import functions

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

conn, cur = database.connect_to_database()

@bot.event
async def on_ready():

    database.create_fish_table(conn, cur)
    database.fill_fish_table(conn, cur)
    database.create_fisherman_table(conn, cur)

    print(f'Zalogowano jako {bot.user.name}')

@bot.command()
async def fishing(ctx):
    """Pozwala złowić rybke"""
    discord_user_id = str(ctx.author.id)
    discord_user_name = str(ctx.author)


    functions.add_fisherman(conn, cur, discord_user_id, discord_user_name)
    fish, experience = functions.fishing(cur)
    functions.fisherman_gain_experience(conn, cur, discord_user_id, experience)


    await ctx.channel.send(f'Udało Ci się złowić: **{fish}** i zdobyć {experience} doświadczenia.')

    has_new_rank, new_rank = functions.get_new_rank(cur, discord_user_id)


    if has_new_rank:

        functions.update_fisherman_rank(conn, cur, discord_user_id, new_rank)

        await ctx.channel.send(f'Gratulacje! Udało Ci się awansować i zdobyć nową rangę = *{new_rank}*')

    


@bot.command()
async def ranking(ctx):
    """Wyświetla ranking graczy"""
    players=functions.get_rankings(cur)
    i=0
    for player in players:
        await ctx.channel.send(f'{i+1}. **{player[0]}** (*{player[3]}*), exp = {player[1]}, złowione ryby = {player[2]}')
        i+=1
        

@bot.event
async def on_close():
    database.close_connection(conn,cur)

bot.run(token)


