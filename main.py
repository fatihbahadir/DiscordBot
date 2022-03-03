import discord
from discord.ext import commands

Bot= commands.Bot("!btw")

@Bot.event
async def on_ready():
    print("Uyandım.")