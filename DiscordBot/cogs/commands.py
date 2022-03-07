import discord
from discord.ext import commands
import datetime
from DiscordBot.Utils.util import prettify

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def selamCog(self, ctx):
        await ctx.send(prettify("Merhaba Ben bu kodu Cogs ile çalıştırıyorum"))

    @commands.command()
    async def time(ctx):
        x=datetime.datetime.now()
        await ctx.send(prettify(x))


def setup(bot):
    bot.add_cog(Commands(bot))