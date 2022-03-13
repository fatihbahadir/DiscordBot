import discord
from discord.ext import commands
from Utils.util import prettify, create_list, get_channels, load_bot_data
import asyncio
import os
from discord.utils import get

REQ_ROLE = "tenkstu"

class Management(commands.Cog, name="Management Commands"):
    def __init__(self, bot):
        self.bot = bot

        DATA = load_bot_data()
        self.needed_channels = DATA['needed-channels']

    @commands.command(description="Kick specified user from server")
    @commands.has_role(REQ_ROLE)
    async def kick(self, ctx, member: discord.Member, *args, reason="Yok"):
        """ Kick someone from the server """
        await member.kick(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} kicked by me."))

    @commands.command(description="Ban specified user from server")
    @commands.has_role(REQ_ROLE)
    async def ban(self, ctx, member: discord.Member, *args, reason="Yok"):
        """ Ban someone from the server """
        await member.ban(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} banned by me."))

    @commands.command(description="Unban specified user from server")
    @commands.has_role(REQ_ROLE)
    async def unban(self, ctx, *, member):
        """ Unban someone from the server """
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for bans in banned_users:
            user = bans.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(prettify(f'{user.display_name} has no longer banned'))
                return

    @commands.command(description="Giving role to specified user")
    @commands.has_role(REQ_ROLE)
    async def giverole(self, ctx, user: discord.Member, *, role: discord.Role):
        """ Give a role to someone """
        await user.add_roles(role)
        await ctx.send(prettify(f"{ctx.author.name} gives the {role.name} role , to {user.name}"))

    @commands.command(description="Clear the channel as given number")
    @commands.has_role(REQ_ROLE)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(prettify(f"I have deleted {amount} messages.", delete_after=3)) 

    @commands.command(description="Listing all the modules(Cogs)")
    @commands.has_role(REQ_ROLE)
    async def modules(self, ctx):
        modules = [i[:-3] for i in os.listdir("./cogs") if not i.startswith("__") and i.endswith("py")]
        await ctx.send(create_list("BTW Bot Modules:",modules))

    @commands.command(description="Mute specified user at a certain time")
    @commands.has_role(REQ_ROLE)
    async def mute(self, ctx, user : discord.Member, duration = 10,*, unit = None):
        """ Mute someone """
        roleobject = discord.utils.get(ctx.message.guild.roles, id=950509386193854465)
        await ctx.send(f":white_check_mark: Muted {user} for {duration}{unit}")
        await user.add_roles(roleobject)
        if unit == "s":
            wait = 1 * duration
            await asyncio.sleep(wait)
        elif unit == "m":
            wait = 60 * duration
            await asyncio.sleep(wait)
        await user.remove_roles(roleobject)
        await ctx.send(f":white_check_mark: {user} was unmuted")

    @commands.command(description="Create missin channels")
    @commands.has_role(REQ_ROLE)
    async def mis_channels(self, ctx):
        text_channel_list = get_channels(self.bot)
        missing_channels = [channel for channel in self.needed_channels if channel not in [chan[0] for chan in text_channel_list]]

        chan_list = await ctx.send(create_list("Missing Channels:", missing_channels, numeric=True))

        guild = ctx.guild
        member = ctx.author
        admin_role = get(guild.roles, name=REQ_ROLE)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }

        for chan in missing_channels:
            await guild.create_text_channel(chan, overwrites=overwrites)

        await chan_list.edit(content=create_list("New Channels:", missing_channels))
        await ctx.send(prettify("Channels are created succesfully!"), delete_after=3)

def setup(bot):
    bot.add_cog(Management(bot))