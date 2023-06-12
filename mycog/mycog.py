from redbot.core import commands

class MyyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def madd(self, ctx, num1: int, num2: int):
         await ctx.send(num1 + num2)
