import discord
from discord.ext import commands
import random
from Utils.util import prettify,create_list
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False

        
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
       
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            
            m_url = self.music_queue[0][0]['source']

            
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

   
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
     
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

    @commands.command(description="Return random music according to your mood")
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