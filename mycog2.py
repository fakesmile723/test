import discord
from redbot.core import commands
from discord.ui import Button, View

class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        embed = discord.Embed(title="Verification", description="Please verify yourself.", color=discord.Color.blue())
        embed.set_footer(text="Verification")
        
        verify_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Verify")
        verify_button.callback = self.verify_callback
        
        embed_message = await ctx.send(embed=embed, view=discord.ui.View(verify_button))

        # Remove the original command message
        await ctx.message.delete()
    
    async def verify_callback(self, interaction: discord.Interaction):
        # Create the ephemeral embed with buttons
        embed = discord.Embed(title="Verification Complete", description="You have successfully verified yourself.", color=discord.Color.green())
        embed.set_footer(text="Verification Complete")

        add_role_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Add Role")
        add_role_button.callback = self.add_role_callback

        read_rules_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Please read the rules!")
        read_rules_button.disabled = True

        ephemeral_view = discord.ui.View(add_role_button, read_rules_button)
        ephemeral_message = await interaction.response.send_message(embed=embed, ephemeral=True, view=ephemeral_view)

        # Update the original message with additional options
        verify_button = interaction.message.view.children[0]
        verify_button.disabled = True
        verify_button.label = "Verified"
        await interaction.message.edit(view=interaction.message.view)

    async def add_role_callback(self, interaction: discord.Interaction):
        # Add the verified role to the user
        verified_role = discord.utils.get(interaction.guild.roles, name="Verified")
        if verified_role:
            await interaction.user.add_roles(verified_role)
            await interaction.response.send_message("You have been given the Verified role!", ephemeral=True)
        else:
            await interaction.response.send_message("The Verified role does not exist.", ephemeral=True)

        # Update the original message with additional options
        read_rules_button = interaction.message.view.children[1]
        read_rules_button.disabled = False
        await interaction.message.edit(view=interaction.message.view)

def setup(bot):
    bot.add_cog(VerifyCog(bot))
