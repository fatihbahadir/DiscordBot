import discord
from discord.ext import commands
from datetime import datetime
from Utils.util import prettify, load_bot_data, get_random_color, adjust_commands, get_max_lenght

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

def setup(bot):
    bot.add_cog(General(bot))