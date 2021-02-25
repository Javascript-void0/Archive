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

@client.command(help='Load Indexes (cogs)')
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'index.{extension}')
    await ctx.send(f'Loaded {extension}')

@client.command(help='Unload Indexes (cogs)')
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'index.{extension}')
    await ctx.send(f'Unloaded {extension}')

@client.command(aliases=['s'], help='Search Indexes')
async def search(ctx, index=None):
    if not index:
        await ctx.send('.search <index1 | index2 | index3>')
    else:
        with open(f'index/{index}/test.txt', 'r') as file:
            await ctx.send(file.read().strip())

'''
for filename in os.listdir('./index'):
    if filename.endswith('.py'):
        client.load_extension(f'index.{filename[:-3]}')
'''

if __name__ == '__main__':
    client.run('TOKEN')