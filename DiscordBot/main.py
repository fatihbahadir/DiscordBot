from Utils.util import prettify, load_bot_data
import discord
from discord.ext import commands
import os
import asyncio

# Initial Data Assignment
DATA = load_bot_data()
bot_token = DATA['token'] # Assign bot token
bot_prefix = DATA['prefix'] # Assign bot prefix
main_channel_id = int(DATA['main-channel']) # Assign the main channel id

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(bot_prefix, intents=intents, help_command=None) # Declare prefix from yaml file

@Bot.command()
async def load(ctx, extention):
    try:
        Bot.load_extension(f"cogs.{extention}")
        await ctx.send(f"{extention} has loaded succesfully! ✔️")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(prettify(f"Module has already loaded!"))
    except Exception as e:
        print(e)
        await ctx.send(prettify(f"No module named {extention}"))

@Bot.command()
async def unload(ctx, extention):
    try:
        Bot.unload_extension(f"cogs.{extention}")
        await ctx.send(f"{extention} has unloaded succesfully! ❌")
    except commands.ExtensionNotFound:
        await ctx.send(prettify(f"No module named as {extention}"))

@Bot.command()
async def reload(ctx, extention):
    
    await cog_switch(ctx, extention)
    await asyncio.sleep(3)
    await cog_switch(ctx, extention)


@Bot.command()
async def cog_switch(ctx, cog_name):
    try:
        Bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(prettify("Cog is loaded"))
    except commands.ExtensionNotFound:
        await ctx.send(prettify("Cog not found"))
    else:
        Bot.unload_extension(f"cogs.{cog_name}")
        await ctx.send(prettify("Cog is unloaded"))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        try:
            Bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

Bot.run(bot_token)