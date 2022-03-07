from distutils import extension
from unittest import async_case
from Utils.util import prettify
import discord
from discord import channel
from discord.ext import commands
import yaml # Burada yaml ile veri import edicez 
            # pip install yaml
from functions import Game
import asyncio
import os
import datetime

# Load Bot Data
def load_bot_data(path="Reqs//bot_adj.yaml"):
    with open(path, "r") as stream: # Read YAML data
        try:
            data = yaml.safe_load(stream) # Convert YAML to list in array
            return data
        except yaml.YAMLError as exc:
            raise Exception("ERROR: "+exc)

# Initial Data Assignment
DATA = load_bot_data()
bot_token = DATA['token'] # Assign bot token
bot_prefix = DATA['prefix'] # Assign bot prefix
main_channel_id = int(DATA['main-channel'])

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(bot_prefix, intents=intents) # Declare prefix from yaml file
game = Game()

# Initial Command
@Bot.event
async def on_ready():
    print("Bot is online now")
    await Bot.get_channel(main_channel_id).send(prettify("bot is online"))

@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    await channel.send(prettify(f"{member.display_name} has joined us.Welcome to our server."))
    print(f"{member} has joined to the server!")

@Bot.event
async def on_member_remove(member):
    channel=discord.utils.get(member.guild.text_channels, name="those-who-left-us")
    await channel.send(prettify(f"{member.display_name} has left us.Good bye"))
    print(f"{member} has left the server!")

@Bot.command()
async def selam(ctx):
    await ctx.send(prettify("Selam!"))

@Bot.command()
async def ping(ctx):
    await ctx.send(prettify(f'Pong! In {round(Bot.latency * 1000)}ms'))

@Bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    message = await ctx.send(prettify(f"I have deleted {amount} messages.")) 
    await asyncio.sleep(3)  
    await message.delete()
    await asyncio.sleep(4) 

# general function
@Bot.command()
async def run(ctx, *args):
    
    if "game" in args:  
        if "roll" in args:
            await ctx.send(prettify(game.roll_dice()))
        elif "flip" in args:
            await ctx.send(prettify(game.flip_coin()))
        elif "givelane" in args:
            await ctx.send(prettify(game.give_lane()))
        else:
            await ctx.send(prettify("Function couldn't found in Bot currently. You can contact with log command (!btw log <text>) to create information post."))
    else:
        await ctx.send(prettify("Currently given run command not required. You can contact with log command (!btw log <text>) to create information post."))

@Bot.command(pass_context=True)
async def giverole(ctx, user: discord.Member,*,role: discord.Role):
    await user.add_roles(role)
    await ctx.send(prettify(f"{ctx.author.name} gives the {role.name} role , to {user.name}  " ))

@Bot.command()
async def repeat(ctx,times : int,content="repeating"):
    for i in range(times):
        await ctx.send(content) 

@Bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(prettify(f"{numOne} + {numTwo} = {numOne + numTwo}"))

@Bot.command()
async def multiply(ctx, numOne: int, numTwo: int):
    await ctx.send(prettify(f"{numOne} * {numTwo} = {numOne * numTwo}"))

@Bot.command()
async def substract(ctx, numOne: int, numTwo: int):
    await ctx.send(prettify(f"{numOne} - {numTwo} = {numOne - numTwo}"))

@Bot.command()
async def divide(ctx, numOne: float, numTwo: float):
    remainder=numOne%numTwo
    await ctx.send(prettify(f"{numOne} / {numTwo} = {numOne / numTwo}"))

@Bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="The server is created for developing a Discord Bot.", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    await ctx.send(embed=embed)
    

@Bot.command()
async def load(ctx, extention):
    Bot.load_extension(f"cogs.{extention}")

@Bot.command()
async def unload(ctx, extention):
    Bot.unload_extension(f"cogs.{extention}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        Bot.load_extension(f"cogs.{filename[:-3]}")

Bot.run(bot_token)