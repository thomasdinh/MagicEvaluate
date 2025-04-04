import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from backend_calc import add_match, find_top_deck

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
    await ctx.send(find_top_deck(min_matches= min_matches, top_rank= rank))

@bot.command()
async def add_entry(ctx, decklist, match_result= None, date=None, group_id = 0):
    add_match(decklist=decklist, result= match_result, filepath= None, group_id= group_id)
    await ctx.send(str(f'{decklist} has been added to the entry'))


bot.run(BOT_TOKEN)