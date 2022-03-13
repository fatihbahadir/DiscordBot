import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from Utils.util import prettify, load_bot_data, get_random_color, adjust_commands, get_max_lenght, get_random_color, create_list, convert_time
import time
from ScrapeCurr.scrape import Scrape

class General(commands.Cog, name="General Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.afk_list = []
        self.afk_meta = {}

        DATA = load_bot_data()
        self.prefix = DATA['prefix']
        self.curr_site = DATA['curr-site']
        self.curr_data = DATA['curr-indicator']

    @commands.command(description="Return hello to user")
    async def Hello(self, ctx):
        await ctx.send(prettify("Hello from BTW bot!"))

    @commands.command(description="Demonstrate what time it is currently")
    async def time(self, ctx):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M, %A")
        await ctx.send(prettify(date_time))

    @commands.command(description="Display general info about user")
    async def info(self, ctx):
        created_at = ctx.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        embed = discord.Embed(title=f"{ctx.guild.name}", description="The server is created for developing a Discord Bot.", timestamp=datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        await ctx.send(embed=embed)

    @commands.command(description="Shows bot's ping in ms type")
    async def ping(self, ctx):
        await ctx.send(prettify(f'Pong! 🏓 In {round(self.bot.latency * 1000)}ms'))
  
    @commands.command(description="Create this text")
    async def help(self, ctx):

        random_color = get_random_color()
        emb = discord.Embed(title="Commands", description=f"**{self.prefix}help** command demostrate all avaliable commands.\nGeneral pattern => **{self.prefix}<command>**", color=random_color)

        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            cog_commands = [(c.name,c.description) for c in cog.get_commands()]
            if cog_commands:
                max_lenght = get_max_lenght([name[0] for name in cog_commands])
                commands_text = adjust_commands(max_lenght, cog_commands)
                emb.add_field(name=cog_name.title(), value=commands_text, inline=False)

        emb.set_footer(text="Information requested by: {}".format(ctx.author.display_name))

        await ctx.send(embed = emb)

    @commands.command()
    async def profile(self, ctx):

        rand_color = get_random_color()

        user = ctx.author
        user_avatar_url = user.avatar_url
        user_name = user.display_name
        user_disc = user.discriminator
        user_id = user.id
        user_created_at = user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")

        emb = discord.Embed(title=user_name.upper(), color=rand_color)
        emb.set_author(name=user_name, icon_url=user_avatar_url)
        emb.set_thumbnail(url=user_avatar_url)
        emb.add_field(name="General Information", value=user_name+"#"+user_disc, inline=False)
        emb.add_field(name="Account Created At", value=user_created_at, inline=False)
        emb.set_footer(text=f"User id: {user_id}")

        await ctx.send(embed=emb)

    @commands.command()
    async def afk(self, ctx, stat: str):
        
        if stat == "on":
            user_id = ctx.author.id
            if user_id not in self.afk_list:    
                self.afk_meta[user_id] = time.time()
                self.afk_list.append(user_id)
                full_name = ctx.author.name+"#"+ctx.author.discriminator
                await ctx.send(prettify(f"You are added to afk list ({full_name})"))
            else:
                await ctx.send(prettify("You are already in afk list"))

        elif stat == "off":
            user_id = ctx.author.id
            if user_id in self.afk_list:
                
                self.afk_list.remove(user_id)

                elapsed_time = time.time() - self.afk_meta[user_id]
                self.afk_meta.pop(user_id)
                await ctx.send(prettify("You are removed from afk list"))
                await ctx.send(prettify(f"You have been afk for {convert_time(elapsed_time)}"))

            else:
                full_name = ctx.author.name+"#"+ctx.author.discriminator
                await ctx.send(prettify("You are not in afk list ({full_name})"))
        
        else:
            await ctx.send(prettify("Requirement is not satisfied! ($afk <on/off>)"))

    @commands.command()
    async def afk_list(self, ctx):
        afk_users = [self.bot.get_user(id).name for id in self.afk_list]
        if afk_users:
            await ctx.send(create_list("Afk List:", afk_users))
        else:
            await ctx.send(prettify("No afk user found!."))

    @commands.command()
    async def pool(self, ctx, *, content):
        args = content.split(",")
        if len(args) == 3:
            rand_color = get_random_color()
            question, ans1, ans2 = args

            emb = discord.Embed(title="Pool Request", color=rand_color)
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.add_field(name="Question", value=question, inline=False)
            emb.add_field(name="Answers", value=f"☀️ {ans1}\n🌑 {ans2}", inline=False)
            emb.set_footer(text=f"requested by: {ctx.author.name}#{ctx.author.discriminator}")

            msg = await ctx.send(embed = emb)
            await msg.add_reaction(emoji="☀️")
            await msg.add_reaction(emoji="🌑")

        else:
            await ctx.send(prettify("Command not in correct typo:\n$pool <question> <first_answer> <second_answer>"))

    @commands.Cog.listener()
    async def on_message(self, msg):
        user_id = msg.author.id
        if user_id in self.afk_list:
            await msg.delete()
            await msg.channel.send(prettify("You are in afk list! You can talk only if you get out of it."), delete_after=2)            

    @commands.command()
    async def currency(self, ctx):

        s = Scrape(self.curr_site)
        soup = s.get_soup()
        curr_val = s.get_curr_data(soup, self.curr_data)

        emb = discord.Embed(title="Live Currencies", color=get_random_color())
        emb.set_thumbnail(url="https://w7.pngwing.com/pngs/306/723/png-transparent-coin-scalable-graphics-icon-coin-text-gold-coin-cartoon.png")
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        for item in curr_val:
            item_name, item_val, rate = item
            emb.add_field(name=item_name ,value=item_val.title()+"\n"+rate ,inline=False)

        emb.set_footer(text=f"requested by: {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(General(bot))