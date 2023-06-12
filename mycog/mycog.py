from redbot.core import commands
import discord
from discord.ui import Button, View

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        button = Button(label="this is a test", style=discord.ButtonStyle.blurple)
        view = View()
        view.add_item(button)
        await ctx.send("The button below is a test which wont work" , view=view)