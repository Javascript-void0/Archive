import discord
import os
import asyncio
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
    if not index:
        await ctx.send('.search <i | ii | iii>')
    else:
        with open(f'index/{index}/test.txt', 'r') as file:
            lines = file.read().splitlines()
            pages = len(lines)
            page = 0
            title, body = lines[page].split(" SPLIT ")
            embed = discord.Embed(title=f'{index}. Document', description=f'Page {page+1}')
            embed.add_field(name=title, value=body)
            message = await ctx.send(embed=embed)
            await message.add_reaction("⏮")
            await message.add_reaction("◀")
            await message.add_reaction("▶")
            await message.add_reaction("⏭")
            await message.add_reaction("❌")

            def check(reaction, user):
                return reaction.message.id == message.id and user == ctx.author

            while True:
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout= 60.0, check=check)
                    if reaction.emoji == '⏮':
                        page = 0
                        title, body = lines[page].split(" SPLIT ")
                        embed = discord.Embed(title=f'{index}. Document', description=f'Page {page+1}')
                        embed.add_field(name=title, value=body)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    if reaction.emoji == '◀' and page > 0:
                        page -= 1
                        title, body = lines[page].split(" SPLIT ")
                        embed = discord.Embed(title=f'{index}. Document', description=f'Page {page+1}')
                        embed.add_field(name=title, value=body)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    if reaction.emoji == '▶' and page < pages -1:
                        page += 1
                        title, body = lines[page].split(" SPLIT ")
                        embed = discord.Embed(title=f'{index}. Document', description=f'Page {page+1}')
                        embed.add_field(name=title, value=body)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    if reaction.emoji == '⏭':
                        page = len(lines)-1
                        title, body = lines[page].split(" SPLIT ")
                        embed = discord.Embed(title=f'{index}. Document', description=f'Page {page+1}')
                        embed.add_field(name=title, value=body)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    if reaction.emoji == '❌':
                        await message.edit(content='`Timeout`', embed=embed)
                        break
                except asyncio.TimeoutError:
                    await message.edit(content='`Timeout`', embed=embed)
                    break

if __name__ == '__main__':
    client.run(TOKEN)