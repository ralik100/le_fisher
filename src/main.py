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

    print(f'Zalogowano jako {bot.user.name}')

@bot.command()
async def fishing(ctx):
    await ctx.channel.send(functions.fishing(cur))

@bot.command()
async def me(ctx):
    users=discord.utils.get(bot.users)
    await ctx.channel.send(users)

@bot.event
async def on_close():
    database.close_connection(conn,cur)

bot.run(token)


