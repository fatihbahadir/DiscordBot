import discord
from discord.ext import commands
import selenium

class Scrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def steamPP(self, ctx, link = None):
        ctx.send("General Steam Profile: "+ link)

def setup(bot):
    bot.add_cog(Scrape(bot))