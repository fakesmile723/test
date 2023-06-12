from redbot.core import commands
import discord
from discord.ui import Button, View
from discord.ext import commands

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def madd(self, ctx, num1: int, num2: int):
    #      await ctx.send(num1 + num2)

    # @commands.hybrid_command()
    # async def madd(self, ctx, nums: commands.Greedy[int]):
    #     if len(nums) < 2:
    #         await ctx.send("Please specify at least two numbers to add.", ephemeral=True)
    #         return

    #     result = sum(list(nums))
    #     await ctx.send(f"The sum of {', '.join(map(str, nums))} is {result}.", ephemeral=True)
    @commands.command()
    async def verify(ctx):
        button = Button(label="this is a test", style=discord.ButtonStyle.blurple)
        view = View()
        view.add_item(button)
        await ctx.send("The button below is a test which wont work" , view=view)