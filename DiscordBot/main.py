from os import name
import discord
from discord import channel
from discord import member
from discord.ext import commands
import yaml # Burada yaml ile veri import edicez 
            # pip install yaml
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
main_channel_id = DATA['main-channel']

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(bot_prefix, intents=intents) # Declare prefix from yaml file

# Initial Command
@Bot.event
async def on_ready():
    await channel.send("I woke up")

@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    await channel.send(f"{member.mention} has joined us.Welcome to our server.")
    print(f"{member} has joined to the server!")

@Bot.event
async def on_member_remove(member):
    print(f"{member} has left the server!")

@Bot.command
async def selam(msg):
    msg.send("Selam!")

Bot.run(bot_token)