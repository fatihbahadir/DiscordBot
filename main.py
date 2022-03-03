import discord
from discord.ext import commands

Bot= commands.Bot("!btw")

@Bot.event
async def on_ready():
    print("Uyandım.")

Bot.run("OTQ4OTQwNDIwMjQxNTgwMDY0.YiDHog.DJRjxJ_--3Tf_Z_11f-wIz6J-M8")