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
    async def urban(self, *, term=None):
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

        try:
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
            embed.description = definition.replace("\\n", "\n") + "\n"
            if examples != "":
                embed.add_field(name="__Example(s) :__", value=examples.replace("\\n", "\n"), inline=False)
                textExamples = examples
            else:
                textExamples = "None"
            embed.add_field(name="Upvotes", value="👍 **{}**".format(thumbsup), inline=True)
            embed.add_field(name="Downvotes", value="👎 **{}**\n\n".format(thumbsdown), inline=True)
            embed.set_footer(text="Defined by {0}".format(author))
            try:
                await self.bot.say(embed=embed)
            except:
                await self.bot.say("**__Definition of {0}__**__ ({1})__\n\n\n".format(word, permalink) + definition.replace("\\n", "\n") + "\n\n" + "__Example(s) :__\n\n" + textExamples.replace("\\n", "\n") + "\n\n" + thumbsup + "👍\n\n" + thumbsdown + "👎\n\n\n\n" + "*Defined by* " + author)
        except:
            try:
                embed = discord.Embed(title="¯\_(ツ)_/¯", colour=discord.Color.orange())
                embed.url = "http://www.urbandictionary.com/define.php?term={}".format(term.replace(" ", "%20"))
                embed.description = "\nThere aren't any definitions for *{0}* yet.\n\n[Can you define it?](http://www.urbandictionary.com/add.php?word={1})\n".format(term, term.replace(" ", "%20"))
                embed.set_footer(text="Error 404", icon_url="http://i.imgur.com/w6TtWHK.png")
                await self.bot.say(embed=embed)
            except:
                await self.bot.say("¯\_(ツ)_/¯\n\n\n" + "There are no definitions for *{}* yet\n\n".format(term) + "Can you define it ?\n( http://www.urbandictionary.com/add.php?word={} )".format(term.replace(" ", "%20")))
#Load the extension
def setup(bot):
    bot.add_cog(Urban(bot))
