from .mycog import Todo


async def setup(bot):
    await bot.add_cog(Todo(bot))
