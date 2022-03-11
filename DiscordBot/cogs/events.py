import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from Utils.util import prettify, load_bot_data, create_list, get_channels
import asyncio

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = 0
        
        # Assign general variables
        DATA = load_bot_data()
        self.prefix = DATA['prefix']
        self.main_channel_id = DATA['main-channel']
        self.new_role = DATA['new-role']
        self.needed_channels = DATA['needed-channels']

    # Initial Command
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online now")

        text_channel_list = get_channels(self.bot)
        missing_channels = [channel for channel in self.needed_channels if channel not in [chan[0] for chan in text_channel_list]]
        
        await self.bot.get_channel(self.main_channel_id).send(prettify("Dady is home bitches!. 🥳"))
        if missing_channels:
            await self.bot.get_channel(self.main_channel_id).send(create_list("Missing Channels:", missing_channels, numeric=True), delete_after=3)

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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(prettify(f"Command not found: '{str(ctx.message.content)}'"))
            return
        raise error

def setup(bot):
    bot.add_cog(Events(bot))