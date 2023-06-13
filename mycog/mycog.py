from redbot.core import commands
import discord
from discord.ui import Button, View

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.message_id = None
        self.role_id = None
        self.channel_id = None

    @commands.command()
    async def setverificationrole(self, ctx, role: discord.Role):
        """Set the role ID for verification."""
        self.role_id = role.id
        await ctx.send(f"Verification role set to: {role.name}")

    @commands.command()
    async def setverificationchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel ID for verification messages."""
        self.channel_id = channel.id
        await ctx.send(f"Verification channel set to: {channel.mention}")

    @commands.command()
    async def verify(self, ctx):
        if not self.role_id:
            return await ctx.send("The verification role ID is not set. Please set it using the `set_verification_role` command.")

        if not self.channel_id:
            return await ctx.send("The verification channel ID is not set. Please set it using the `set_verification_channel` command.")

        embed = discord.Embed(title="Verification", description="**Read the rules and click on the button below that says Verify to gain access**", color=0x2b2d31)
        embed.set_image(url="https://media.tenor.com/yG0BZ-wew-sAAAAC/verify-discord.gif")

        vbutton = Button(label="Verify", style=discord.ButtonStyle.blurple, emoji="<:yess:1020703229891330099>")

        async def button_callback(interaction):
            if self.message_id is None:
                message = await ctx.guild.get_channel(self.channel_id).send(embed=buttonembed, view=view2, ephemeral=True)
                self.message_id = message.id
            else:
                existing_message = await ctx.guild.get_channel(self.channel_id).fetch_message(self.message_id)
                await existing_message.edit(view=None)

        button1 = Button(emoji="👋🏻")
        button2 = Button(emoji="🔥")
        button3 = Button(emoji="🤩")
        button4 = Button(emoji="✅")

        async def button1_callback(interaction):
            await interaction.response.edit_message(content="This is button1", embed=None, view=None)

        async def button2_callback(interaction):
            member = interaction.user
            guild = interaction.guild

            role = guild.get_role(self.role_id)

            if role is not None:
                if role in member.roles:
                    await interaction.response.edit_message(content="You are already verified!", embed=None, view=None)
                else:
                    await member.add_roles(role)
                    await interaction.response.edit_message(content="Role added successfully!", embed=None, view=None)
            else:
                await interaction.response.edit_message(content="Role not found. Please contact a server administrator.", embed=None, view=None)

        async def button3_callback(interaction):
            await interaction.response.edit_message(content="This is button3", embed=None, view=None)

        async def button4_callback(interaction):
            await interaction.response.edit_message(content="This is button4", embed=None, view=None)

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

        buttonembed = discord.Embed(title="Verifying", description="You are about to verify yourself.\nIf you read the rules, click on the right emote to get verified.", color=0x2b2d31)

        view = View()
        view.add_item(vbutton)

        await ctx.send(embed=embed, view=view)

