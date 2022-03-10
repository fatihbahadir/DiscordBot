import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from Utils.util import prettify, load_bot_data, get_random_color, adjust_commands, get_max_lenght, get_random_color, create_list

class Calc:

    @staticmethod
    def sum(num1, num2):
        return num1 + num2
    
    @staticmethod
    def subs(num1, num2):
        return num1 - num2

    @staticmethod
    def mult(num1, num2):
        return num1 * num2

    @staticmethod
    def div(num1, num2):
        return num1 / num2

class General(commands.Cog, name="General Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.afk_list = []

        DATA = load_bot_data()
        self.prefix = DATA['prefix']

    @commands.command(description="Return hello to user")
    async def Hello(self, ctx):
        await ctx.send(prettify("Hello from BTW bot!"))

    @commands.command(description="Demonstrate what time it is currently")
    async def time(self, ctx):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M, %A")
        await ctx.send(prettify(date_time))

    @commands.command(description="Basic calculator")
    async def calc(self, ctx, *args):
        print(args)

    @commands.command(description="Display general info about user")
    async def info(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="The server is created for developing a Discord Bot.", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
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
                self.afk_list.append(user_id)
                await ctx.send(prettify("You are added to afk list"))
            else:
                await ctx.send(prettify("You are already in afk list"))

        elif stat == "off":
            user_id = ctx.author.id
            if user_id in self.afk_list:
                
                self.afk_list.remove(user_id)
                await ctx.send(prettify("You are removed from afk list"))

            else:
                await ctx.send(prettify("You are not in afk list"))
        
        else:
            await ctx.send(prettify("Requirement is not satisfied! ($afk <on/off>)"))

    @commands.command()
    async def afk_list(self, ctx):
        afk_users = [self.bot.get_user(id).name for id in self.afk_list]
        if afk_users:
            await ctx.send(create_list("Afk List:", afk_users))
        else:
            await ctx.send(prettify("No afk user found!."))

    @commands.Cog.listener()
    async def on_message(self, msg):
        user_id = msg.author.id
        if user_id in self.afk_list:
            await msg.delete()
            info_msg = await msg.channel.send(prettify("You are in afk list! You can talk only if you get out of it."))
            await asyncio.sleep(2)
            await info_msg.delete()
            await asyncio.sleep(3)

def setup(bot):
    bot.add_cog(General(bot))