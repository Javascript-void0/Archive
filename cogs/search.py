import discord
import os
import asyncio
from discord.ext import commands

async def update_embed(listpages, page, url, f, message):
    newpage = listpages[page]
    if newpage[2] == "None":
        embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1}')
    else:
        embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1} - [Link]({newpage[2]})')
    embed.add_field(name=newpage[0], value=f'{newpage[1]}\n\n[Document in Github]({url})')
    embed.set_footer(text=f'Page {listpages.index(newpage)+1} of {len(listpages)}')
    await message.edit(embed=embed)

class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['s','open','o'], help='Search Directory')
    async def search(self, ctx, dir=None, option=None):
        if dir == None:
            await ctx.send('`[x] Usage: .search <file> [page|all]`')

        for file in os.listdir('./index'):
            f = file[2:]
            if f == dir + ".txt":
                with open(f'index/{file}', 'r') as file:
                    lines = file.read().splitlines()
                    page = 0
                    link = None
                    url = f'https://github.com/Javascript-void0/Archive/blob/main/{file.name}'

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
                    
                    titles = []
                    texts = []
                    links = []
                    for i in range(len(lines)):
                        if lines[i].startswith(' TITLE '):
                            x = lines[i].replace(' TITLE ', "", 1)
                            titles.append(x)
                        elif lines[i].startswith(' LINK '):
                            x = lines[i].replace(' LINK ', "", 1)
                            links.append(x)
                        else:
                            texts.append(lines[i])
                            t = "\n".join(texts)
                            t = t.split("\n\n")

                    listpages = []
                    for i in range(len(titles)):
                        newpage = []
                        newpage.append(titles[i])
                        newpage.append(t[i])
                        newpage.append(links[i])
                        listpages.append(newpage)

                    if option == "all":
                        if isinstance(ctx.channel, discord.channel.DMChannel) == True:
                            for s in listpages:
                                newpage = listpages[page]
                                if newpage[2] == "None":
                                    embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1}')
                                else:
                                    embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1} - [Link]({newpage[2]})')
                                embed.add_field(name=newpage[0], value=f'{newpage[1]}\n\n[Document in Github]({url})')
                                embed.set_footer(text=f'Page {listpages.index(newpage)+1} of {len(listpages)}')
                                message = await ctx.send(embed=embed)
                                page += 1
                        else:
                            await ctx.send('`[x] Sending all pages can only be used in DMs`')

                    else:
                        newpage = listpages[page]
                        if newpage[2] == "None":
                            embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1}')
                        else:
                            embed = discord.Embed(title=f'Document {f}', description=f'Page {page+1} - [Link]({newpage[2]})')
                        embed.add_field(name=newpage[0], value=f'{newpage[1]}\n\n[Document in Github]({url})')
                        embed.set_footer(text=f'Page {listpages.index(newpage)+1} of {len(listpages)}')
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
                                    await message.remove_reaction(reaction, user)
                                    await update_embed(listpages, page, url, f, message)
                                elif reaction.emoji == '◀' and page > 0:
                                    page -= 1
                                    await message.remove_reaction(reaction, user)
                                    await update_embed(listpages, page, url, f, message)
                                elif reaction.emoji == '▶' and page < len(listpages) -1:
                                    page += 1
                                    await message.remove_reaction(reaction, user)
                                    await update_embed(listpages, page, url, f, message)
                                elif reaction.emoji == '⏭' and page != len(listpages)-1:
                                    page = len(listpages)-1
                                    await message.remove_reaction(reaction, user)
                                    await update_embed(listpages, page, url, f, message)
                                elif reaction.emoji == '❌':
                                    await message.edit(content='`[x] Timeout`', embed=embed)
                                    await message.remove_reaction(reaction, user)
                                    break
                                else:
                                    await message.remove_reaction(reaction, user)
                            except asyncio.TimeoutError:
                                await message.edit(content='`[x] Timeout`', embed=embed)
                                break

def setup(client):
    client.add_cog(Search(client))