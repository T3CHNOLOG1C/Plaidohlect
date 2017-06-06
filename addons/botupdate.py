from subprocess import call
import discord
import os
from discord.ext import commands
from sys import argv

class botupdate:
    """
    Bot Updating Commands (Owners Only)
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, name="pull")
    async def pull(self, ctx):
        """Pull from GitHub (Owner Only)"""
        call(['git', 'pull'])
        await self.bot.say("Changes pulled from GitHub, Restarting...")
        await self.bot.close()

def setup(bot):
    bot.add_cog(botupdate(bot))
