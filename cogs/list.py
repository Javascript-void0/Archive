import discord
import os
from discord.ext import commands

doc_count = 0
cat_count = 0

for file in os.listdir('index'):
    doc_count += 1
    ct = []
    ct.append(file[0])
    ct.sort()
    cat_count = int(ct[-1])

class List(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['files', 'index'], help='List Files in Directory')
    async def list(self, ctx):
        l = {}
        em = discord.Embed(title="List of Files in Directory")
        for i in range(cat_count):
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