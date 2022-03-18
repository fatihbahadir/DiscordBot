from pydoc import describe
from venv import create
import discord
from discord.ext import commands
from Utils.util import prettify, create_list, get_yt_ids, get_yt_title, remove_chars, check_steam_profile, get_steam_profile

class Scrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yt_query_url = "https://www.youtube.com/results?search_query="
        self.yt_url = "https://www.youtube.com/watch?v="

        self.steam_profile_query = "https://steamcommunity.com/id/"

    @commands.command(description="**UNDER CONSTRUCTION**")
    async def steamPP(self, ctx, url = None):
        if not url.startswith(self.steam_profile_query):
            await ctx.send(prettify("Given url is not allowed"))
            return

        content = check_steam_profile(url)
        
        profile_meta = get_steam_profile(content)

        await ctx.send(profile_meta)


    @commands.command(description="Search youtube video and return its url")
    async def youtube(self, ctx, *url_name: commands.clean_content):
        info_message = await ctx.send(prettify("Searching for videos.."))
        
        url = remove_chars(self.yt_query_url+"+".join(url_name))
        await info_message.edit(content=prettify("General video data is gathering.."))
        
        video_urls = [self.yt_url+id for id in get_yt_ids(url)]
        video_datas = get_yt_title(video_urls)
        video_titles = [data[0] for data in video_datas]
        
        allowed = [str(i) for i in range(1,len(video_urls)+1)]
        await info_message.delete()
        
        vid_lst = await ctx.send(create_list(f'Results for "{" ".join(url_name)}" : ', video_titles, numeric=True))
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.bot.wait_for("message", check = check)

        if msg.content in allowed:
            select_url = video_urls[int(msg.content)-1]
            await ctx.send(select_url)
        else:
            await ctx.send(prettify(f"Please enter valid number"))

        await vid_lst.delete()

def setup(bot):
    bot.add_cog(Scrape(bot))