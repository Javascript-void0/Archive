import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
#client.remove_command('help')
TOKEN = os.getenv("TOKEN")

cat_count = 3
doc_count = 0

@client.event
async def on_ready():
    print('[+] Started {0.user}'.format(client))
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the Archives | .help"))

@client.command(help='Reloads Cogs')
@commands.is_owner()
async def reload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
    await ctx.send(f'`[+] Reloaded Cogs`')

for file in os.listdir('./index'):
    doc_count += 1  

@client.command(help='Load Cogs')
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension}')

@client.command(help='Unload Cogs')
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'[+] Loaded {filename}')

if __name__ == '__main__':
    client.run(TOKEN)