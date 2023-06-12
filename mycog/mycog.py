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
        button2 = Button(label="this is a test2", style=discord.ButtonStyle.red)

        async def button_callback(interaction):
            await interaction.response.send_message("you clicked it!", ephemeral=True)
        async def button2_callback(interaction):
            await interaction.response.send_message("you clicked it again!", ephemeral=True)

        button2.callback = button2_callback

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send("The button below is a test which wont work" , view=view)