import discord
from discord.ext import commands
from Utils.util import prettify, load_bot_data

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Assign general variables
        DATA = load_bot_data()
        self.prefix = DATA['prefix']
        self.main_channel_id = DATA['main-channel']

    # Initial Command
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online now")
        await self.bot.get_channel(self.main_channel_id).send(prettify("Dady is home bitches!. 🥳"))

def setup(bot):
    bot.add_cog(Events())