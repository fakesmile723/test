from redbot.core import commands
import discord
from discord.ui import Button, View

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.message = None

    @commands.command()
    async def verify(self, ctx):
        embed = discord.Embed(title="Verification", description="**Read the rules and click on the button below that says Verify to gain access**", color=0x2b2d31)
        embed.set_image(url="https://media.tenor.com/yG0BZ-wew-sAAAAC/verify-discord.gif")

        vbutton = Button(label="Verify", style=discord.ButtonStyle.blurple, emoji="<:yess:1020703229891330099>")

        async def button_callback(interaction):
            if self.message is None:
                self.message = await interaction.response.send_message(embed=buttonembed, view=view2, ephemeral=True)
            else:
                await interaction.response.edit_message(view=None)

        button1 = Button(emoji="👋🏻")
        button2 = Button(emoji="🔥")
        button3 = Button(emoji="🤩")
        button4 = Button(emoji="✅")

        async def button1_callback(interaction):
            await interaction.response.edit_message(content="this is button1", embed=None, view=None)

        async def button2_callback(interaction):
            await interaction.response.edit_message(content="this is button2", embed=None, view=None)

        async def button3_callback(interaction):
            await interaction.response.edit_message(content="this is button3", embed=None, view=None)

        async def button4_callback(interaction):
            await interaction.response.edit_message(content="this is button4", embed=None, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback
        button3.callback = button3_callback
        button4.callback = button4_callback

        view2 = View()
        view2.add_item(button1)
        view2.add_item(button2)
        view2.add_item(button3)
        view2.add_item(button4)

        vbutton.callback = button_callback

        buttonembed = discord.Embed(title="Verifying", description="You are about to verify yourself /n if you read the rules click on the right emote to get verified", color=0x2b2d31)

        view = View()
        view.add_item(vbutton)

        await ctx.send(embed=embed, view=view)
