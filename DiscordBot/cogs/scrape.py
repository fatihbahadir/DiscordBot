import discord
from discord.ext import commands
from Utils.util import prettify, create_list, get_yt_ids, get_yt_title, remove_chars, check_steam_profile, get_steam_profile, get_random_color
import wikipedia
class Scrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yt_query_url = "https://www.youtube.com/results?search_query="
        self.yt_url = "https://www.youtube.com/watch?v="

        self.steam_profile_query = "https://steamcommunity.com/"
        self.wikipedia_query = "https://tr.wikipedia.org/w/index.php?search={}&title=%C3%96zel%3AAra&ns0=1"

    @commands.command(description="**UNDER CONSTRUCTION**")
    async def steamPP(self, ctx, url = None):
        
        await ctx.message.delete()
        
        if not url.startswith(self.steam_profile_query):
            await ctx.send(prettify("Given url is not allowed"))
            return

        content = check_steam_profile(url)
        profile_meta = get_steam_profile(content)

        emb = discord.Embed(title="Steam Profile", color=get_random_color(), timestamp=datetime.utcnow())
        # emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        emb.set_thumbnail(url=profile_meta['avatar-url'])
        emb.add_field(name="Profile Name", value=profile_meta['name'], inline=False)
        emb.add_field(name="Badget", value=profile_meta['rozet'], inline=True)
        emb.add_field(name="Games", value=profile_meta['games'], inline=True)
        emb.add_field(name="Level", value=profile_meta['level'], inline=False)
        
        max_game_url = [0, None]
        for game in profile_meta['recent-games']:
            game_url, game_time, game_name  = game
            total, recent = game_time
            emb.add_field(name=game_name.upper(),value="Total : "+total+"\nRecent : "+recent, inline=False)
            
            max_tot_val = float(total.split(" ")[0].replace(",", "."))
            if max_tot_val > max_game_url[0]:
                max_game_url = [max_tot_val, game_url]


        emb.set_image(url=max_game_url[1])
        emb.set_footer(text=f"requested by {ctx.author.display_name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=emb)



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

    @commands.command(description="gdajkghfjkhgahjk")
    async def whois(self, ctx, *, search):
        
        # await ctx.send(wikipedia.summary("".join(search), sentences=1))
        pass


def setup(bot):
    bot.add_cog(Scrape(bot))