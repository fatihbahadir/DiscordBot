import discord
from discord.ext import commands
from Utils.util import prettify
import asyncio

REQ_ROLE = "tenkstu"

class Management(commands.Cog, name="Management Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(REQ_ROLE)
    async def kick(self, ctx, member: discord.Member, *args, reason="Yok"):
        await member.kick(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} kicked by me."))

    @commands.command()
    @commands.has_role(REQ_ROLE)
    async def ban(self, ctx, member: discord.Member, *args, reason="Yok"):
        await member.ban(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} banned by me."))

    @commands.command()
    @commands.has_role(REQ_ROLE)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for bans in banned_users:
            user = bans.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(prettify(f'{user.display_name} has no longer banned'))
                return

    @commands.command()
    @commands.has_role(REQ_ROLE)
    async def giverole(self, ctx, user: discord.Member, *, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(prettify(f"{ctx.author.name} gives the {role.name} role , to {user.name}"))

    @commands.command()
    @commands.has_role("tenkstu")
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)
        message = await ctx.send(prettify(f"I have deleted {amount} messages.")) 
        await asyncio.sleep(3)  
        await message.delete()
        await asyncio.sleep(4) 

def setup(bot):
    bot.add_cog(Management(bot))