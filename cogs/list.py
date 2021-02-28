import discord
import os
from discord.ext import commands

class List(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['files', 'index'], help='List Files in Directory')
    async def list(self, ctx):
        for file in os.listdir('index'):
            ct = []
            ct.append(file[0])
            ct.sort()
        l = {}
        em = discord.Embed(title="List of Files in Directory")
        for i in range(int(ct[-1])):
            i += 1
            l[i] = []
            for file in os.listdir('index'):
                if file.startswith(f"{i}_"):
                    f = file[2:]
                    l[i].append(f)
            l[i] = "\n".join(l[i])
            em.add_field(name=f'Category {i}', value=l[i], inline=False)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(List(client))