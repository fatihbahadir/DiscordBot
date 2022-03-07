import discord
from discord.ext import commands
from Utils.util import prettify
from random import randint

class Game:

    @staticmethod
    def roll():
        return randint(1, 6)

    @staticmethod
    def flip():
        coin = ["head", "tail"]
        selected = coin[randint(0,1)]
        return selected
    
    @staticmethod
    def givelane():
        lane=["top","jungle","mid","adc","support"]
        selected=lane[randint(0,len(lane)-1)]
        return selected

class Fun(commands.Cog,name="Fun Commands"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def repeat(self, ctx, times : int, content="repeating"):
        for _ in range(times):
            await ctx.send(prettify(content))

    @commands.command()
    async def game(self, ctx, game_type : str):

        methods = [method for method in dir(Game) if not method.startswith("__") and not method.endswith("_")]
        
        if game_type.lower() == "show":
            await ctx.send("Game List:")
            for method in methods:
                await ctx.send("- "+method)
        else:
            if game_type.lower() in methods:
                method = getattr(Game, game_type.lower())
                result = method()
                await ctx.send(prettify(result))
            else:
                await ctx.send("")

def setup(bot):
    bot.add_cog(Fun(bot))