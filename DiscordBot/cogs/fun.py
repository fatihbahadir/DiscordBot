import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command
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
        """ Create a list """
        await ctx.send(create_list(title,args))
    
    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Gives you a new password. """
        alphabet="abcdefghijklmnoprstuvyzxwABCDEFGHIJKLMNOPRSTUVYZXW"
        numbers="0123456789"
        indicators=alphabet+numbers
        pswrd=""
        for _ in range(nbytes):
            pswrd+=indicators[randint(0,len(indicators)-1)]
        user = await self.bot.fetch_user(ctx.message.author.id)
        await user.send(prettify("You new password: "+pswrd))
        await ctx.send(prettify(f"Hey {ctx.message.author.display_name} I send you a private message about your password request."))
    
    @commands.command()
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
    
    @commands.command()
    async def music(self,ctx):
        await ctx.send(prettify("What kind of music would you like to listen to ? \n -Emotinal \n -Happy \n -Depressed \n -Angry \n -Hopeful \n -Sad"))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in["Emotional","Happy","Depressed","Angry","Hopeful","Sad"]
        
        msg=await self.bot.wait_for("message", check= check)

        if msg.content == "Emotinal":
            emotinal=["R.E.M Everybody Hurts","Harry Chapin Cat's in the Cradle","Nirvana Something in the Way"]
            await ctx.send(emotinal[random.randint[0,2]])
        elif msg.content == "Happy":
            happy=["https://www.youtube.com/watch?v=aXJhDltzYVQ","https://www.youtube.com/watch?v=iSLwVaebsJg","https://www.youtube.com/watch?v=HgzGwKwLmgM"]
            await ctx.send(happy[random.randint(0,2)])
        elif msg.content == "Depressed":
            deppressed=["https://youtu.be/GWbiHdSgEuk","https://youtu.be/2MRdtXWcgIw","https://youtu.be/O4irXQhgMqg"]
            await ctx.send(deppressed[random.randint(0,2)])
        elif msg.content == "Angry":
            furious=["https://youtu.be/NPcyTyilmYY","https://youtu.be/0xyxtzD54rM","https://youtu.be/WaSy8yy-mr8"]
            await ctx.send(furious[random.randint(0,2)])
        elif msg.content == "Hopeful":
            hopeful=["https://youtu.be/MGurkDflu-A","https://youtu.be/wq7edbqi9n0","https://youtu.be/W9nJ9sY9BJM"]
            await ctx.send(hopeful[random.randint(0,2)])
        elif msg.content == "Sad":
            sad=["https://www.youtube.com/watch?v=4WXYjm74WFI","https://www.youtube.com/watch?v=9EKi2E9dVY8","https://www.youtube.com/watch?v=OLVWEYUqGew"]
            await ctx.send(sad[random.randint(0,2)])
        else:
            await ctx.send(prettify("Please enter a valid type"))
def setup(bot):
    bot.add_cog(Fun(bot))