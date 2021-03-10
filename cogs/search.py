import discord
import os
import asyncio
from discord.ext import commands

async def update_embed(page, f, message, lines, link=None):
    try:
        title, body = lines[page].split(" SPLIT ")
    except ValueError:
        title, body, link = lines[page].split(" SPLIT ")
        embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1} - [Link]({link})')
    else:
        embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1}')
    body = f"{body}".encode().decode('unicode-escape')
    embed.add_field(name=title, value=body)
    await message.edit(embed=embed)

class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['s','open','o'], help='Search Directory')
    async def search(self, ctx, dir=None, option=None):
        if dir == None:
            await ctx.send('`[x] Usage: .search <file> [page|all]`')

        for file in os.listdir('index'):
            f = file[2:]
            if f == dir + ".txt":
                with open(f'index/{file}', 'r') as file:
                    lines = file.read().splitlines()
                    pages = len(lines)
                    page = 0
                    link = None

                    try: 
                        try:
                            if float(option).is_integer():
                                option = int(option)
                                try:
                                    if option > 0 and option <= len(lines):
                                        page = option-1
                                except IndexError:
                                    page = 0
                        except TypeError:
                            pass
                    except ValueError:
                        pass

                    if option == "all":
                        if isinstance(ctx.channel, discord.channel.DMChannel) == True:
                            for s in lines:
                                try:
                                    title, body = s.split(" SPLIT ")
                                except ValueError:
                                    title, body, link = s.split(" SPLIT ")
                                    embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1} - [Link]({link})')
                                else:
                                    embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1}')
                                body = f"{body}".encode().decode('unicode-escape')
                                embed.add_field(name=title, value=body)
                                page += 1
                                await ctx.send(embed=embed)
                        else:
                            await ctx.send('`[x] Sending all pages can only be used in DMs`')

                    else:
                        try:
                            title, body = lines[page].split(" SPLIT ")
                        except ValueError:
                            title, body, link = lines[page].split(" SPLIT ")
                            embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1} - [Link]({link})')
                        else:
                            embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1}')
                        body = f"{body}".encode().decode('unicode-escape')
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
                                reaction, user = await self.client.wait_for('reaction_add', timeout= 60.0, check=check)
                                if reaction.emoji == '⏮' and page != 0:
                                    page = 0
                                    await update_embed(page, f, message, lines, link)
                                    await message.remove_reaction(reaction, user)
                                elif reaction.emoji == '◀' and page > 0:
                                    page -= 1
                                    await update_embed(page, f, message, lines, link)
                                    await message.remove_reaction(reaction, user)
                                elif reaction.emoji == '▶' and page < pages -1:
                                    page += 1
                                    await update_embed(page, f, message, lines, link)
                                    await message.remove_reaction(reaction, user)
                                elif reaction.emoji == '⏭' and page != len(lines)-1:
                                    page = len(lines)-1
                                    await update_embed(page, f, message, lines, link)
                                    await message.remove_reaction(reaction, user)
                                elif reaction.emoji == '❌':
                                    await message.edit(content='`[x] Timeout`', embed=embed)
                                    break
                                else:
                                    await message.remove_reaction(reaction, user)
                            except asyncio.TimeoutError:
                                await message.edit(content='`[x] Timeout`', embed=embed)
                                break

def setup(client):
    client.add_cog(Search(client))