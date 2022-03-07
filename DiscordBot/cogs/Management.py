import discord
from discord.ext import commands
from DiscordBot.Utils.util import prettify

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("tenkstu")
    async def kick(ctx, member: discord.Member, *args, reason="Yok"):
        await member.kick(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} kicked by me."))

    @commands.command()
    @commands.has_role("tenkstu")
    async def ban(ctx, member: discord.Member, *args, reason="Yok"):
        await member.ban(reason=reason)
        await ctx.send(prettify(f"The {member.display_name} banned by me."))

    @commands.command()
    @commands.has_role("tenkstu")
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
    bot.add_cog(commands(bot))