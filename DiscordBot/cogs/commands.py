import discord
from discord.ext import commands
import datetime
from Utils.util import prettify

class Calc:

    @staticmethod
    def sum(num1, num2):
        return num1 + num2
    
    @staticmethod
    def subs(num1, num2):
        return num1 - num2

    @staticmethod
    def mult(num1, num2):
        return num1 * num2

    @staticmethod
    def div(num1, num2):
        return num1 / num2

class General(commands.Cog, name="General Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def selamCog(self, ctx):
        await ctx.send(prettify("Merhaba Ben bu kodu Cogs ile çalıştırıyorum"))

    @commands.command()
    async def time(ctx):
        x=datetime.datetime.now()
        await ctx.send(prettify(x))

    @commands.command()
    async def calc(ctx, *args):
        print(args)

def setup(bot):
    bot.add_cog(General(bot))