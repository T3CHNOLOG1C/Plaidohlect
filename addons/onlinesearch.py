import discord
import json
import requests
import wikipedia
from discord.ext import commands
from sys import argv

class OnlineSearch:
    """
    Search stuff, or get stuff from the internet
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command()
    async def urban(self, *, term=None):
        """Lookup a term on Urban Dictionnary. If no term is specified, returns a random definition"""
        
        if term is None:
            r = requests.get("http://api.urbandictionary.com/v0/random")
            js = r.json()
        else:
            r = requests.get("http://api.urbandictionary.com/v0/define?term={}".format(term))
            js = r.json()
            if js["result_type"] == "no_results":
                try:
                    embed = discord.Embed(title="¯\_(ツ)_/¯", colour=discord.Color.orange())
                    embed.url = "http://www.urbandictionary.com/define.php?term={}".format(term.replace(" ", "%20"))
                    embed.description = "\nThere aren't any definitions for *{0}* yet.\n\n[Can you define it?](http://www.urbandictionary.com/add.php?word={1})\n".format(term, term.replace(" ", "%20"))
                    embed.set_footer(text="Error 404", icon_url="http://i.imgur.com/w6TtWHK.png")
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("¯\_(ツ)_/¯\n\n\n" + "There are no definitions for *{}* yet\n\n".format(term) + "Can you define it ?\n( http://www.urbandictionary.com/add.php?word={} )".format(term.replace(" ", "%20")))

        firstResult = js["list"][0]
        word = firstResult["word"]
        definition = firstResult["definition"]
        example = firstResult["example"]
        author = firstResult["author"]
        permalink = firstResult["permalink"]
        thumbsup = firstResult["thumbs_up"]
        thumbsdown = firstResult["thumbs_down"]

        chars = ['[', ']', '\\r\\n', "\\n"]
        for c in chars:
            if c == chars[0] or c == chars[1]:
                definition = definition.replace(c, '')
                example = example.replace(c, '')
            elif c == chars[2] or c == chars [3]:
                definition = definition.replace(c, '\n')
                example = example.replace(c, '\n')

        if example != "":
            textExamples = example
        else:
            textExamples = "None"

        try:
            embed = discord.Embed(title="Definition of {}\n\n".format(word), colour=discord.Color.orange())
            embed.set_thumbnail(url="http://i.imgur.com/B1gZbQz.png")
            embed.url = permalink
            embed.description = definition + "\n"
            if textExamples is not None:
                embed.add_field(name="__Example(s) :__", value=textExamples, inline=False)
            embed.add_field(name="Upvotes", value="👍 **{}**".format(thumbsup), inline=True)
            embed.add_field(name="Downvotes", value="👎 **{}**\n\n".format(thumbsdown), inline=True)
            embed.set_footer(text="Defined by {0}".format(author))
            await self.bot.say(embed=embed)
        except:
            await self.bot.say("**__Definition of {0}__**__ ({1})__\n\n\n".format(word, permalink) + definition + "\n\n" + "__Example(s) :__\n\n" + textExamples + "\n\n\n" + str(thumbsup) + " 👍\n\n" + str(thumbsdown) + " 👎\n\n\n\n" + "*Defined by " + author + "*")

    @commands.command(name='whats', aliases=["what", "what's"])
    async def whats(self, *, term):
        """Defines / explains stuff"""

        if term[0:2] == "a " and term != "a":
            term = term[2:]
        elif term[0:5] == "is a " and term != "is a":
            term = term[5:]
        elif term[0:6] == "is an " and term != "is an":
            term = term[6:]
        elif term[0:3] == "is " and term != "is":
            term = term[3:]

        term = term.lower()

        if term == "kai" or term == "mitchy":
            kai = await self.bot.get_user_info("272908611255271425")
            try:
                embed = discord.Embed(title="Kai", colour=discord.Color.orange())
                embed.set_thumbnail(url=kai.avatar_url)
                embed.description = "An edgy kid that spends too much time on tumblr, previously named mitchy, previously named sans-serif"
                await self.bot.say(embed=embed)
            except:
                await self.bot.say("**__Kai :__**\n\nAn edgy kid that spends too much time on tumblr, previously named mitchy, previously named sans-serif")
        else:
            try:
                wiki = wikipedia.page(term)
                if wiki.summary[-13:] == "may refer to:":
                    if len(wiki.content) > 1997:
                        await self.bot.say("{}...".format(wiki.content[0:1997]))
                    else:
                        await self.bot.say(wiki.content)
                else:
                    if len(wiki.summary) > 1997:
                        await self.bot.say("{}...".format(wiki.summary[0:1997]))
                    else:
                        await self.bot.say(wiki.summary) #embed soonTM
            except wikipedia.exceptions.PageError: 
                await self.bot.say("Sorry, none of my sources have an explanation for this term :(")
                    #try other websites
            except wikipedia.exceptions.DisambiguationError:
                await self.bot.say("Please be more precise! `{}` can refer to many terms!".format(term))


#TO-DO : google web and image search

#Load the extension
def setup(bot):
    bot.add_cog(OnlineSearch(bot))