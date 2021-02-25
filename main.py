import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print('Started {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Around the Clock Archives"))

@client.command(aliases=['s'], help='Search Indexes')
async def search(ctx, index=None, p=None):
    if not index:
        await ctx.send('.search <index1 | index2 | index3>')
    else:
        if not p:
            p = 1
        if p <= 0:
            p = 1
        with open(f'index/{index}/test.txt', 'r') as file:
            lines = file.read().splitlines()
            for s in lines:
                title, body = s.split(" SPLIT ")
                embed = discord.Embed(title=f'{index}. Document', description=f'Page {p}')
                embed.add_field(name=title, value=body)
                await ctx.send(embed=embed)

if __name__ == '__main__':
    client.run(TOKEN)