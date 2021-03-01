import discord
import os
import config
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['i','information','info'], help='Info about the bot')
    async def help(self, ctx):
        embed = discord.Embed(title='🗑 Archive Bot', description='Random crap coming from a [Github Repository](https://github.com/Javascript-void0/Archive).')
        embed.add_field(name=f'Documents: {config.doc_count}', value='Made by Java  🍌', inline=True)
#        embed.add_field(name='Commands: 3', value='help, search, list', inline=True)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/814293652234043392/815606602316382208/totoro-560x301_3.jpg')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))