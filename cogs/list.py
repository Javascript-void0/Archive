import discord
import os
from main import cat_count
from discord.ext import commands

class List(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['files', 'index'], help='List Files in Directory')
    async def list(self, ctx, cat=None):
        try:
            cat = int(cat)
        except TypeError:
            pass
        try:
            if cat <= cat_count and cat > 0:
                lcat = []
                for file in os.listdir('index'):
                    if file.startswith(f"{cat}_"):
                        f = file[2:]
                        lcat.append(f)
                lcat = "\n".join(lcat)
                embed = discord.Embed(title=f"Files in Category {cat}")
                embed.add_field(name=f'Category {cat}', value=lcat)
                await ctx.send(embed=embed)
        except TypeError:
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