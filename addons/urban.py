import discord
from discord.ext import commands
from sys import argv
import requests

class Urban:
    """
    Urban Dictionnary requests
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command()
    async def urban(self,term=None):
        """Lookup a term on Urban Dictionnary. If no term is specified, returns a random word / definition"""
        def slicer(str,sep1:str,sep2:str=None,select=True): #Slices a defined part of a string
            if select is True:
                selectFirstDef = str.split("}", 1)[0]
                delBefore = selectFirstDef.split(sep1, 1)[1]
            else:
                delBefore = str.split(sep1, 1)[1]
            delAfter = delBefore.split(sep2, 1)[0]
            if sep2 is None:
                return delBefore
            else:
                return delAfter

        if term is None:
            r = requests.get("http://api.urbandictionary.com/v0/random")
        else:
            r = requests.get("http://api.urbandictionary.com/v0/define?term={}".format(term))
        
        source = r.text
        if source == "{\"tags\":[],\"result_type\":\"no_results\",\"list\":[],\"sounds\":[]}" : #aka error 404
            embed = discord.Embed(title="¯\_(ツ)_/¯", colour=discord.Color.orange())
            embed.url = "http://www.urbandictionary.com/define.php?term={}".format(term)
            embed.description = "\nThere aren't any definitions for *{0}* yet.\n\n[Can you define it?](http://www.urbandictionary.com/add.php?word={0})\n".format(term)
            embed.set_footer(text="Error 404", icon_url="http://i.imgur.com/w6TtWHK.png")
            await self.bot.say(embed=embed)
        else:
            word = slicer(source,"\"word\":\"","\",\"defid\":")
            definition = slicer(source,"\"definition\":\"","\",\"permalink\":\"").replace("\\r\\n", "\n")
            examples = slicer(source,"\"example\":\"","\",\"thumbs_down\":").replace("\\r\\n", "\n")
            author = slicer(source,"\"author\":\"","\",\"word\":\"")
            permalink = slicer(source,"\"permalink\":\"","\",\"thumbs_up\":")
            thumbsup = slicer(source,"\"thumbs_up\":",",\"author\":\"")
            thumbsdown = slicer(source,"\"thumbs_down\":")
#            def date(permalink, author): #there's no date field on the api site, so let's do it ourselves
 #               d = requests.get(permalink)
  #              page = d.text.replace("'", "\"")
   #             date = slicer(page,">{}</a>".format(author),"</div><div class=\"def-footer\">",False)
    #            return date
            embed = discord.Embed(title="Definition of {}\n\n".format(word), colour=discord.Color.orange())
            embed.set_thumbnail(url="http://i.imgur.com/B1gZbQz.png")
            embed.url = permalink
            embed.description = definition + "\n"
            embed.add_field(name="__Example(s) :__", value=examples + "\n\n", inline=False)
            embed.add_field(name="Upvotes", value="👍 **{}**".format(thumbsup), inline=True)
            embed.add_field(name="Downvotes", value="👎 **{}**\n\n".format(thumbsdown), inline=True)
            embed.set_footer(text="Defined by {0}".format(author))
            await self.bot.say(embed=embed)

#Load the extension
def setup(bot):
    bot.add_cog(Urban(bot))
