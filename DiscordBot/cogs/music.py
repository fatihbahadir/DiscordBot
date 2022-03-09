import discord
from discord.ext import commands
import random
from Utils.util import prettify,create_list

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_music(self,ctx):
        music_type=["Emotional","Happy","Depressed","Angry","Hopeful","Sad"]
        await ctx.send(create_list("What kind of music would you like to listen to ?" ,music_type))
       
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel 
        
        msg = await self.bot.wait_for("message", check= check)
        
      
        if  msg.content == music_type[0]:
            emotional=["https://www.youtube.com/watch?v=5rOiW_xY-kc","https://www.youtube.com/watch?v=KUwjNBjqR-c","https://www.youtube.com/watch?v=1YhR5UfaAzM"]
            await ctx.send(emotional[random.randint(0,2)])
        elif msg.content == music_type[1]:
            happy=["https://www.youtube.com/watch?v=aXJhDltzYVQ","https://www.youtube.com/watch?v=iSLwVaebsJg","https://www.youtube.com/watch?v=HgzGwKwLmgM"]
            await ctx.send(happy[random.randint(0,2)])
        elif msg.content == "Depressed":
            deppressed=["https://youtu.be/GWbiHdSgEuk","https://youtu.be/2MRdtXWcgIw","https://youtu.be/O4irXQhgMqg"]
            await ctx.send(deppressed[random.randint(0,2)])
        elif msg.content == music_type[2]:
            furious=["https://youtu.be/NPcyTyilmYY","https://youtu.be/0xyxtzD54rM","https://youtu.be/WaSy8yy-mr8"]
            await ctx.send(furious[random.randint(0,2)])
        elif msg.content == music_type[3]:
            hopeful=["https://youtu.be/MGurkDflu-A","https://youtu.be/wq7edbqi9n0","https://youtu.be/W9nJ9sY9BJM"]
            await ctx.send(hopeful[random.randint(0,2)])
        elif msg.content == music_type[4]:
            sad=["https://www.youtube.com/watch?v=4WXYjm74WFI","https://www.youtube.com/watch?v=9EKi2E9dVY8","https://www.youtube.com/watch?v=OLVWEYUqGew"]
            await ctx.send(sad[random.randint(0,2)])
        else:
            await ctx.send(prettify("Please enter a valid type"))

def setup(bot):
    bot.add_cog(Music(bot))