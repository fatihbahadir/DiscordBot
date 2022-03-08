from Utils.util import prettify, load_bot_data
import discord
from discord.ext import commands
import os

# Initial Data Assignment
DATA = load_bot_data()
bot_token = DATA['token'] # Assign bot token
bot_prefix = DATA['prefix'] # Assign bot prefix
main_channel_id = int(DATA['main-channel']) # Assign the main channel id

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(bot_prefix, intents=intents, help_command=None) # Declare prefix from yaml file

@Bot.command()
async def load(ctx, extention):
    Bot.load_extension(f"cogs.{extention}")
    await ctx.send(f"{extention} has loaded succesfully! ✔️")

@Bot.command()
async def unload(ctx, extention):
    Bot.unload_extension(f"cogs.{extention}")
    await ctx.send(f"{extention} has unloaded succesfully! ❌")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        try:
            Bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

Bot.run(bot_token)