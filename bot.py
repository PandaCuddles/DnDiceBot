# bot.py
import os
import random
import dice_engine
from dotenv import load_dotenv

from discord.ext import commands

# TODO: Finish help message for !roll command
help_msg = f"Dice Bot Help!"

# Uses .env file for loading Discord bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Determines what is processed as a command
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='roll', help=help_msg)
async def roll(ctx, roll):
    #print(ctx.message.content)
    print(ctx.bot)
    print(ctx.command)
    if (len(ctx.message.content)>6):
        dice_roll=ctx.message.content[6:100]
        print(dice_roll)
        response=dice_engine.parse(dice_roll)
    else:
        response="No dice roll given. Type '!help roll' for more info."
    
    #response = f"This is an automated test of the Roll Inc. dice roller!\nPlease stand by!\n"
    await ctx.send(response)

bot.run(TOKEN)

