from redbot.core import commands
from redbot.core.bot import Red
import discord

ROLE_ID = 1118228001415508031

class ButtonsView(discord.ui.View):
    @discord.ui.button(emoji="👋🏻", custom_id="1")
    async def button_1_callback(self, interaction: discord.Interaction, item: discord.ui.Button):
        await interaction.response.edit_message(content="This is button 1.", embed=None, view=None)

    @discord.ui.button(emoji="🔥", custom_id="2")
    async def button_2_callback(self, interaction: discord.Interaction, item: discord.ui.Button):
        member = interaction.user
        guild = interaction.guild
        if (role := guild.get_role(ROLE_ID)) is None:
            await interaction.response.edit_message(content=f"Role {ROLE_ID} not found. Please contact a server administrator.", embed=None, view=None)
            return
        if role in member.roles:
            await interaction.response.edit_message(content="You are already verified!", embed=None, view=None)
        else:
            await member.add_roles(role)
            await interaction.response.edit_message(content="Role added successfully!", embed=None, view=None)

    @discord.ui.button(emoji="🤩", custom_id="3")
    async def button_3_callback(self, interaction: discord.Interaction, item: discord.ui.Button):
        await interaction.response.edit_message(content="This is button 3.", embed=None, view=None)

    @discord.ui.button(emoji="✅", custom_id="4")
    async def button_4_callback(self, interaction: discord.Interaction, item: discord.ui.Button):
        await interaction.response.edit_message(content="This is button 4.", embed=None, view=None)

class MyView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @discord.ui.button(label="Verify",style=discord.ButtonStyle.green,emoji="ℹ️",custom_id="mycog_verify")
    async def button_callback(self, interaction: discord.Interaction, item: discord.ui.Button):
        button_embed: discord.Embed = discord.Embed(title="Verifying",description="You are about to verify yourself /n if you read the rules click on the right emote to get verified",color=0x2b2d31)
        await interaction.response.send_message(embed=button_embed, view=ButtonsView(), ephemeral=True)

class MyyCog(commands.Cog):
    """My custom cog."""

    def __init__(self, bot: Red) -> None:
        self.bot: Red = bot

    async def cog_load(self) -> None:
        self.bot.add_view(MyView())

    # @commands.admin_or_permissions(administrator=True)
    @commands.command()
    async def verify(self, ctx: commands.Context):
        embed: discord.Embed = discord.Embed(title="Verification",description="**Read the rules and click on the button below that says Verify to gain access**",color=0x2b2d31)
        embed.set_image(url="https://media.tenor.com/yG0BZ-wew-sAAAAC/verify-discord.gif")