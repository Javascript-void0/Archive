import discord
import os
from discord.ext import commands

class TestFile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['tf'], help='Tests Format of Attached File')
    async def testfile(self, ctx):
        if not ctx.message.attachments:
            await ctx.send('Attach a `.txt` file with the command')
        else:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith('.txt'):
                await attachment.save(attachment.filename)
                with open(attachment.filename, 'r') as file:
                    lines = file.read().splitlines()
                    pages = len(lines)
                    page = 0
                    link = None

                for s in lines:
                    try:
                        title, body = s.split(" SPLIT ")

                    except ValueError as e:
                        if '(expected 2)' in str(e):

                            try:
                                title, body, link = s.split(" SPLIT ")
                            except ValueError as e:
                                if '(expected 3)' in str(e):
                                    await ctx.send(f'{attachment.filename} has too many SPLITs')
                                    os.remove(attachment.filename)
                            else:
                                embed = discord.Embed(title=f'Document {attachment.filename}', description=f'Page {page+1} - [Link]({link})')

                        elif 'not enough' in str(e):
                            await ctx.send(f'{attachment.filename} is missing title/body')
                            os.remove(attachment.filename)
                    else:
                        embed = discord.Embed(title=f'Document {attachment.filename}', description=f'Page {page+1}')

                    body = f"{body}".encode().decode('unicode-escape')
                    embed.add_field(name=title, value=body)
                    page += 1
                    await ctx.send(embed=embed)

                os.remove(attachment.filename)
            else:
                await ctx.send('Attach a `.txt` file with the command')
                

def setup(client):
    client.add_cog(TestFile(client))