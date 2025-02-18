import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from backend_calc import find_best_decks

description = '''Bot to evaluate MTG matches in a play group
'''
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL = 1341019500958449674 # chnage to your channel
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    channel = bot.get_channel(CHANNEL)
    await channel.send(f'Logged in as {bot.user}') #(ID: {bot.user.id})

@bot.command()
async def isReady(ctx):
    await ctx.send(str('MTG Bot is ready!'))

@bot.command()
async def top_deck(ctx , min_matches=3,rank=1):
    await ctx.send(find_best_decks(least_matches= min_matches, top_placements= rank))

bot.run(BOT_TOKEN)