from Utils.util import prettify
import discord
from discord.ext import commands
import yaml
import os

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
Bot = commands.Bot(bot_prefix, intents=intents, help_command=None) # Declare prefix from yaml file

# Initial Command
@Bot.event
async def on_ready():
    print("Bot is online now")
    await Bot.get_channel(main_channel_id).send(prettify("Dady is home bitches!. 🥳"))

@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    await member.add_roles(member.guild.get_role(949767411928801381))
    await channel.send(prettify(f"{member.display_name} has joined us.Welcome to our server."))
    print(f"{member} has joined to the server!")

@Bot.event
async def on_member_remove(member):
    channel=discord.utils.get(member.guild.text_channels, name="those-who-left-us")
    await channel.send(prettify(f"{member.display_name} has left us.Good bye"))
    print(f"{member} has left the server!")

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