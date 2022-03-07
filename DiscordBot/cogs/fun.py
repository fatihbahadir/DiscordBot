import discord
from discord.ext import commands
from Utils.util import prettify,create_list
from random import randint
import random
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
        """ Repeat something as many times as you want """
        for _ in range(times):
            await ctx.send(prettify(content))

    @commands.command()
    async def game(self, ctx, game_type : str):
        """ Select a game  """

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
                await ctx.send(prettify(f"There is no game such that {game_type} "))

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None,  reason: commands.clean_content = ""):
        """ Buy someone a beer """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"{ctx.author.name}: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot {ctx.author.name}, but I don't think it will respond to you :/")

        beer_offer = f"{user.name}, you got a 🍺 from {ctx.author.name}"
        beer_offer = beer_offer + f"\n\nReason: {reason}" if reason else beer_offer
        msg = await ctx.send(prettify(beer_offer))

    @commands.command()
    async def f(self,ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for {text} " if text else ""
        await ctx.send(prettify(f"{ctx.author.name} has paid their respect {reason}{random.choice(hearts)}"))
    
    @commands.command()
    async def createlist(self,ctx,title : str,*args):
        await ctx.send(create_list(title,args))


def setup(bot):
    bot.add_cog(Fun(bot))