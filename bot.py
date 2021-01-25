import requests
import discord
import sqlite3
from discord.ext import commands
from datetime import datetime, timedelta
import os

conn = sqlite3.connect('settings.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Prefix (
  prefix text,
  guild interger
)""")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.guild_reactions = True
intents.reactions = True

async def getPrefix(bot, message):
  prefix = '-'
  try:
    c.execute(f"SELECT * FROM Prefix WHERE guild={message.guild.id}")
    row = c.fetchone()
    shit = row['prefix']
    prefix = f'{shit}'
  except TypeError:
    prefix = '?'
  except sqlite3.OperationalError:
    prefix = '?'

  return prefix

bot = commands.Bot(command_prefix=getPrefix, case_insensitive=True, intents=intents)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
  print(f"Bot Name: {bot.user}\nBot ID: {bot.user.id}\nBot Created At: {bot.user.created_at.strftime('%d %B, %Y')}")

TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
