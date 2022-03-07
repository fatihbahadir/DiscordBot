import discord
from discord.ext import commands
import datetime
from Utils.util import prettify, create_list
import os

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
        """ Say hello to Cog """
        await ctx.send(prettify("Merhaba Ben bu kodu Cogs ile çalıştırıyorum"))

    @commands.command()
    async def time(self, ctx):
        """ Tells you what time is it"""
        x=datetime.datetime.now()
        await ctx.send(prettify(x))

    @commands.command()
    async def calc(self, ctx, *args):
        """ Some basic calculations """
        print(args)

    @commands.command()
    async def info(self, ctx):
        """ See the server info """
        embed = discord.Embed(title=f"{ctx.guild.name}", description="The server is created for developing a Discord Bot.", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(prettify(f'Pong! 🏓 In {round(self.bot.latency * 1000)}ms'))

    @commands.command()
    async def modules(self, ctx):
        modules = [i[:-3] for i in os.listdir("./cogs") if not i.startswith("__") and i.endswith("py")]

def setup(bot):
    bot.add_cog(General(bot))