import discord
from discord.ext import commands
from Utils.util import prettify

req_role = "tenkstu"

class Management(commands.Cog, name="Management Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(req_role)
    async def kick(ctx, member: discord.Member, *args, reason="Yok"):
        await member.kick(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} kicked by me."))

    @commands.command()
    @commands.has_role(req_role)
    async def ban(ctx, member: discord.Member, *args, reason="Yok"):
        await member.ban(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} banned by me."))

    @commands.command()
    @commands.has_role(req_role)
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for bans in banned_users:
            user = bans.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(prettify(f'{user.display_name} has no longer banned'))
                return

def setup(bot):
    bot.add_cog(Management(bot))