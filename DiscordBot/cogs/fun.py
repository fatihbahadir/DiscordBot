import discord
from discord.ext import commands
from Utils.util import prettify,create_list
from random import randint
import random
import wikipedia
from Utils.util import add_garbage, fetch_json_data

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
        
        json_data = fetch_json_data()        
        self.bot = bot

        self.counter = json_data['garbage']['tenkstu'] if "tenkstu" in json_data['garbage'] else 0

    @commands.command(description="Repeat something as many times as you want ")
    async def repeat(self, ctx, times : int, content="repeating"):
        for _ in range(times):
            await ctx.send(prettify(content))

    @commands.command(description="Play various games")
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
                await ctx.send(prettify(f"There is no game such that {game_type} "))

    @commands.command(description="Buy someone a beer")
    async def beer(self, ctx, user: discord.Member = None,  reason: commands.clean_content = ""):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"{ctx.author.name}: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot {ctx.author.name}, but I don't think it will respond to you :/")

        beer_offer = f"{user.name}, you got a 🍺 from {ctx.author.name}"
        beer_offer = beer_offer + f"\n\nReason: {reason}" if reason else beer_offer
        msg = await ctx.send(prettify(beer_offer))

    @commands.command(description="Press F to pay respect")
    async def f(self,ctx, *, text: commands.clean_content = None):
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for {text} " if text else ""
        await ctx.send(prettify(f"{ctx.author.name} has paid their respect {reason}{random.choice(hearts)}"))
    
    @commands.command(description="Create a list")
    async def createlist(self,ctx,title : str,*args):
        await ctx.send(create_list(title,args))
    
    @commands.command(description="Request a new password")
    async def password(self, ctx, nbytes: int = 18):
        alphabet="abcdefghijklmnoprstuvyzxwABCDEFGHIJKLMNOPRSTUVYZXW"
        numbers="0123456789"
        indicators=alphabet+numbers
        pswrd=""
        for _ in range(nbytes):
            pswrd+=indicators[randint(0,len(indicators)-1)]
        user = await self.bot.fetch_user(ctx.message.author.id)
        await user.send(prettify("You new password: "+pswrd))
        await ctx.send(prettify(f"Hey {ctx.message.author.display_name} I send you a private message about your password request."))
    
    @commands.command(description="Guess the number.")
    async def guess(self,ctx):
        computer = random.randint(1, 10)
        await ctx.send(prettify('Guess my number'))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        msg = await self.bot.wait_for("message", check=check)

        if int(msg.content) == computer:
            await ctx.send(prettify("Correct"))
        else:
            await ctx.send(prettify(f"Nope it was {computer}"))
    
    @commands.command(description="A counter")
    async def thankstu(self,ctx):
        self.counter+=1
        await ctx.send(prettify(f'Thankstu counter is now %d' %self.counter))
        add_garbage("tenkstu", self.counter)

def setup(bot):
    bot.add_cog(Fun(bot))