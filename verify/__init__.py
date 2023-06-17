from .mycog import MyyCog


async def setup(bot):
    await bot.add_cog(MyyCog(bot))
