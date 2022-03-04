from email import message
from http import client
from tracemalloc import start
import discord
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

intents = discord.Intents(message=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(bot_prefix, intents=intents) # Declare prefix from yaml file

# Initial Command
@Bot.event
async def on_ready():
    print("Bot has been started succefully.")

@Bot.event
async def on_member_join(member):
    print(f"{member} has joined to the server!")

@Bot.event
async def on_member_remove(member):
    print(f"{member} has left the server!")

@Bot.command
async def SendStartMessage(msg):
    start_message ="""
```
Bot has been runned succesfully.
```
    """
    await msg.send(start_message)


Bot.run(bot_token)