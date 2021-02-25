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
async def search(ctx, index=None):
    #text = []
    if not index:
        await ctx.send('.search <index1 | index2 | index3>')
    else:
#        with open(f'index/{index}/test.txt', "rb") as file:
#            await ctx.send("Your file is:", file=discord.File(file, "test.txt"))

        with open(f'index/{index}/test.txt', 'r') as file:
            title, body = file.read().split(" SPLIT ")
            embed = discord.Embed(title=f'{index}. Document', description='Page NUM')
            embed.add_field(name=title, value=body)
            await ctx.send(embed=embed)
    
if __name__ == '__main__':
    client.run('ODE0Mjg1NjUyMTE1OTgwMzcw.YDbonA.kSPMPXSj2G2WYh5w3rtb62vnVz0')