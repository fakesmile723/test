from .bard import BAIChat


async def setup(bot):
    await bot.add_cog(BAIChat(bot))
