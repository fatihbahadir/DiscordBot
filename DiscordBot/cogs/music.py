import discord
from discord.ext import commands
import random
from Utils.util import prettify

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_music(self,ctx):
        await ctx.send(prettify("What kind of music would you like to listen to ? \n -Emotinal \n -Happy \n -Depressed \n -Angry \n -Hopeful \n -Sad"))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in["Emotional","Happy","Depressed","Angry","Hopeful","Sad"]
        
        msg = await self.bot.wait_for("message", check= check)

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
    bot.add_cog(Music(bot))