import discord
from discord.ext import commands
from Utils.util import prettify, load_bot_data

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = 0
        
        # Assign general variables
        DATA = load_bot_data()
        self.prefix = DATA['prefix']
        self.main_channel_id = DATA['main-channel']
        self.new_role = DATA['new-role']

    # Initial Command
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online now")
        await self.bot.get_channel(self.main_channel_id).send(prettify("Dady is home bitches!. 🥳"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        await member.add_roles(member.guild.get_role(self.new_role))
        await channel.send(prettify(f"{member.display_name} has joined us.Welcome to our server."))
        print(f"{member} has joined to the server!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel=discord.utils.get(member.guild.text_channels, name="those-who-left-us")
        await channel.send(prettify(f"{member.display_name} has left us.Good bye"))
        print(f"{member} has left the server!")

def setup(bot):
    bot.add_cog(Events(bot))