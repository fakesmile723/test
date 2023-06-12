from redbot.core import commands

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def madd(self, ctx, num1: int, num2: int):
    #      await ctx.send(num1 + num2)
    @commands.hybrid_command()
    async def madd(self, ctx, *nums: int):
        if len(nums) < 2:
            await ctx.send("Please specify at least two numbers to add.", ephemeral=True)
            return

        result = sum(nums)
        await ctx.send(f"The sum of {', '.join(map(str, nums))} is {result}.", ephemeral=True)