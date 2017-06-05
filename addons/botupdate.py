import discord
from discord.ext import commands
from sys import argv
from subprocess import call

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
    self.bot.say("Changes pulled from GitHub :ok_hand:")

def setup(bot):
    bot.add_cog(botupdate(bot))
