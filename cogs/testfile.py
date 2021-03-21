import discord
import os
from discord.ext import commands

class TestFile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['tf'], help='Tests Format of Attached File')
    async def testfile(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel) == True:
            if not ctx.message.attachments:
                await ctx.send('`[x] Attach a `.txt` file with the command`')
            else:
                attachment = ctx.message.attachments[0]
                if attachment.filename.endswith('.txt'):
                    await attachment.save(attachment.filename)
                    with open(attachment.filename, 'r') as file:
                        lines = file.read().splitlines()
                        pages = len(lines)
                        page = 0
                        link = None
                        url = f'https://github.com/Javascript-void0/Archive/blob/main/index/{attachment.filename}'
                        f = attachment.filename[2:]

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

                    os.remove(attachment.filename)
                else:
                    await ctx.send('`[x] Attach a .txt file with the command`')
        else:
            await ctx.send('`[x] This command can only be used in DMs`')

    @testfile.error
    async def testfile_error(self, ctx, error):
        if isinstance(error, IndexError):
            await ctx.send('`[-] A page is missing a required value`')

def setup(client):
    client.add_cog(TestFile(client))