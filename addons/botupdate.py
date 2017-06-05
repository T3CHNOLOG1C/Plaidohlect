import discord
from discord.ext import commands
from sys import argv
from subprocess import call

class botupdate:
    """
    Bot Updating Commands (Owners Only)
    """
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, name="pull")
    async def pull(self, ctx):
       """Pull from GitHub (Owner Only)"""
        call(['git', 'pull'])

def setup(bot):
    bot.add_cog(botupdate(bot))
