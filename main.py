import discord
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")

async def update_embed(page, edir, message, lines, image=None):
    try:
        title, body = lines[page].split(" SPLIT ")
    except ValueError:
        title, body, image = lines[page].split(" SPLIT ")
        embed = discord.Embed(title=f'Document {edir}', description=f'Page {page+1} - [Image]({image})')
    else:
        embed = discord.Embed(title=f'Document {edir}', description=f'Page {page+1}')
    embed.add_field(name=title, value=body)
    await message.edit(embed=embed)

@client.event
async def on_ready():
    print('Started {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Around the Clock Archives"))

@client.command(aliases=['s'], help='Search Directory')
async def search(ctx, dir=None, option=None):
    if dir == None:
        await ctx.send('Usage: `.search <file> <all>`')

    edir = dir[2:]
    with open(f'index/{dir}.txt', 'r') as file:
        lines = file.read().splitlines()
        pages = len(lines)
        page = 0
        image = None

        if option == "all":
            for s in lines:
                try:
                    title, body = s.split(" SPLIT ")
                except ValueError:
                    title, body, image = s.split(" SPLIT ")
                    embed = discord.Embed(title=f'Document {edir}', description=f'Page {page+1} - [Image]({image})')
                else:
                    embed = discord.Embed(title=f'Document {edir}', description=f'Page {page+1}')
                embed.add_field(name=title, value=body)
                page += 1
                message = await ctx.send(embed=embed)

        else:
            try:
                title, body = lines[page].split(" SPLIT ")
            except ValueError:
                title, body, image = lines[page].split(" SPLIT ")
                embed = discord.Embed(title=f'Document {edir}', description=f'Page {page+1} - [Image]({image})')
            else:
                embed = discord.Embed(title=f'Document {edir}', description=f'Page {page+1}')
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
                    if reaction.emoji == '⏮' and page != 0:
                        page = 0
                        await update_embed(page, edir, message, lines, image)
                        await message.remove_reaction(reaction, user)
                    elif reaction.emoji == '◀' and page > 0:
                        page -= 1
                        await update_embed(page, edir, message, lines, image)
                        await message.remove_reaction(reaction, user)
                    elif reaction.emoji == '▶' and page < pages -1:
                        page += 1
                        await update_embed(page, edir, message, lines, image)
                        await message.remove_reaction(reaction, user)
                    elif reaction.emoji == '⏭' and page != len(lines)-1:
                        page = len(lines)-1
                        await update_embed(page, edir, message, lines, image)
                        await message.remove_reaction(reaction, user)
                    elif reaction.emoji == '❌':
                        await message.edit(content='`Timeout`', embed=embed)
                        break
                    else:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    await message.edit(content='`Timeout`', embed=embed)
                    break

@client.command(aliases=['files, index'], help='List Files in Directory')
async def list(ctx):
    for file in os.listdir('index'):
        if file.startswith("1_"):
            await ctx.send(f"**US_History**: {file}")
        elif file.startswith("2_"):
            await ctx.send(f"**Testing**: {file}")

if __name__ == '__main__':
    client.run(TOKEN)