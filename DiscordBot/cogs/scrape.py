import discord
from discord.ext import commands
import selenium
import urllib.request
import re
from Utils.util import prettify, create_list, get_yt_title

class Scrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yt_query_url = "https://www.youtube.com/results?search_query="
        self.yt_url = "https://www.youtube.com/watch?v="

    @commands.command()
    async def steamPP(self, ctx, link = None):
        ctx.send("General Steam Profile: "+ link)

    @commands.command()
    async def youtube(self, ctx, *url_name: commands.clean_content):
        info_message = await ctx.send(prettify("Searching for videos.."))
        url = self.yt_query_url+"+".join(url_name)
        html = urllib.request.urlopen(url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())[:5]
        video_data = [(get_yt_title(self.yt_url+id),self.yt_url+id) for id in video_ids]
        await info_message.delete()
        await ctx.send(prettify(video_data))

def setup(bot):
    bot.add_cog(Scrape(bot))