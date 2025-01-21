import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

@bot.command()
async def asd(ctx):
    print(f'sent message in channel: {ctx.channel}')
    await ctx.send("ns")

@bot.event
async def on_message(message):
   
    if message.author == bot.user:
        return

    if message.content.startswith('nehring'):
        await message.channel.send(':)')

    await bot.process_commands(message)

bot.run(token)
