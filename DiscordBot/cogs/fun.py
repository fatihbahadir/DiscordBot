import discord
from discord.ext import commands
from Utils.util import prettify
from random import randint

class Fun(commands.Cog,name="Fun Commands"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def repeat(self,ctx,times : int,content="repeating"):
        for i in range(times):
            await ctx.send(prettify(content))

class Game:

    @staticmethod
    def roll_dice():
        return randint(1, 7)

    @staticmethod
    def flip_coin():
        coin = ["head", "tail"]
        selected = coin[randint(0,2)]
        return selected
    
    @staticmethod
    def give_lane():
        lane=["top","jungle","mid","adc","support"]
        selected=lane[randint(0,len(lane))]
        return selected

def setup(bot):
    bot.add_cog(Fun(bot))