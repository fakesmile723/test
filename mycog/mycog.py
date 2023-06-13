from redbot.core import commands
import discord
from discord.ui import Button, View

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        embed=discord.Embed(title="Verification", description="Read the rules and click on the button below that says verify to verify yourself", color=0x2b2d31)
        embed.set_image(url="https://media.tenor.com/yG0BZ-wew-sAAAAC/verify-discord.gif")
        embed.add_field(name="field", value="value", inline=False)

        await ctx.send(embed=embed)
        button = Button(label="this is a test", style=discord.ButtonStyle.blurple)
        button2 = Button(label="this is a test2", style=discord.ButtonStyle.red)

        async def button_callback(interaction):
            await interaction.response.send_message("you clicked it!", ephemeral=True)
        async def button2_callback(interaction):
            await interaction.response.send_message("you clicked it again!", ephemeral=True)

        button2.callback = button2_callback

        button.callback = button_callback
        view = View(timeout=180)
        view.add_item(button)
        view.add_item(button2)
        await ctx.send(embed = embed , view=view)
        await ctx.bot.remove_cog("MyyCog")
        await ctx.bot.add_cog(MyyCog(ctx.bot))