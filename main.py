import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')
TOKEN = os.getenv("DISCORD_TOKEN")

doc_count = 0
cat_count = 0

for file in os.listdir('index'):
    ct = []
    ct.append(file[0])
    ct.sort()
    cat_count = (int(ct[-1]))

for file in os.listdir('index'):
    doc_count += 1

@client.event
async def on_ready():
    print('Started {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Archives"))

@client.command(help='Reloads Cog')
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded {extension}.py')

@client.command(help='Heroku Testing')
@commands.is_owner()
async def test(ctx):
    await ctx.send(f'Cat_count: {cat_count}')
    await ctx.send(f'Doc_count: {doc_count}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    client.run(TOKEN)
    client.unload_extension('cogs.list')
    client.load_extension('cogs.list')