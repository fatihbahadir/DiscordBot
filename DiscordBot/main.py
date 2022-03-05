from Utils.util import prettify
import discord
from discord import channel
from discord.ext import commands
import yaml # Burada yaml ile veri import edicez 
            # pip install yaml
from functions import Game
import asyncio


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

@Bot.command()
@commands.has_role("tenkstu")
async def kick(ctx, member: discord.Member, *args, reason="Yok"):
    await member.kick(reason=reason)
    await ctx.send(prettify(f"The {member.display_name} kicked by me."))

@Bot.command()
@commands.has_role("tenkstu")
async def ban(ctx, member: discord.Member, *args, reason="Yok"):
    await member.ban(reason=reason)
    await ctx.send(prettify(f"The {member.display_name} banned by me."))

@Bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for bans in banned_users:
        user = bans.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(prettify(f'{user.display_name} has no longer banned'))
            return
@Bot.command(pass_context=True)
async def giverole(ctx, user: discord.Member,*,role: discord.Role):
    await user.add_roles(role)
    await ctx.send(prettify(f"{ctx.author.name} gives the {role.name} role , to {user.name}  " ))

Bot.run(bot_token)