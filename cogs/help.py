import discord
import os
from config import doc_count
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['i','information','info'], help='Info about the bot')
    async def help(self, ctx, cmds=None):
        if cmds == "commands" or cmds == "cmds":
            embed = discord.Embed(title='🗑 Archive Bot Commands')
            embed.add_field(name="▪.help - Info about the bot", value="aliases - help, i, info, information\nusage - .help [commands|cmds]", inline=False)
            embed.add_field(name="▪.list - List of Files in Directory", value="aliases - list, files, index\nusage - .list [category]", inline=False)
            embed.add_field(name="▪.search - Search Directory", value="aliases - search, s, open, o\nusage - .search <file> [page|all]", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='🗑 Archive Bot', description='Random crap coming from a [Github Repository](https://github.com/Javascript-void0/Archive).')
            embed.add_field(name=f'Documents: {doc_count}', value='Made by Java 🍌', inline=True)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/814293652234043392/815606602316382208/totoro-560x301_3.jpg')
            embed.set_footer(text='✔ .help [commands] for list of commands')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))