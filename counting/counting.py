from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord

class Counting(commands.Cog):
    """Cog for a counting game with leaderboards, custom reactions, and per-guild configuration."""

    default_guild = {
        "current_number": 0,
        "channel_id": None,
        "leaderboard": {},
        "correct_emote": "✅",
        "wrong_emote": "❌"
    }

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=271828, force_registration=True)
        self.config.register_guild(**self.default_guild)

    @commands.command()
    async def startcounting(self, ctx, channel: discord.TextChannel):
        """Starts the counting game in the specified channel."""
        await self.config.guild(ctx.guild).channel_id.set(channel.id)
        await self.config.guild(ctx.guild).current_number.set(1)
        await self.config.guild(ctx.guild).leaderboard.set({})
        await channel.send("Counting game started! Next number: 1")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handles messages in the counting game channel."""
        if message.author.bot:  # Ignore bot messages
            return

        guild_config = await self.config.guild(message.guild).all()
        if guild_config["channel_id"] == message.channel.id:
            try:
                next_number = int(message.content)
                if next_number == guild_config["current_number"] + 1:
                    await self.config.guild(message.guild).current_number.set(next_number)
                    await message.add_reaction(guild_config["correct_emote"])

                    leaderboard = guild_config["leaderboard"]
                    user_id = str(message.author.id)
                    leaderboard[user_id] = leaderboard.get(user_id, 0) + 1
                    await self.config.guild(message.guild).leaderboard.set(leaderboard)
                else:
                    await message.add_reaction(guild_config["wrong_emote"])
            except ValueError:
                pass  # Ignore non-numeric messages

    @commands.command()
    async def currentnumber(self, ctx):
        """Displays the current number in the counting game."""
        current_number = await self.config.guild(ctx.guild).current_number()
        await ctx.send(f"The current number is: {current_number}")

    @commands.group()
    async def countingset(self, ctx):
        """Configuration commands for the counting game."""
        pass  # Placeholder for subcommands

    @countingset.command(name="correctemote")
    async def set_correct_emote(self, ctx, emote: discord.Emoji):
        """Sets the emote to use for correct guesses."""
        await self.config.guild(ctx.guild).correct_emote.set(str(emote))
        await ctx.send(f"Correct guess emote set to: {emote}")

    @countingset.command(name="wrongemote")
    async def set_wrong_emote(self, ctx, emote: discord.Emoji):
        """Sets the emote to use for wrong guesses."""
        await self.config.guild(ctx.guild).wrong_emote.set(str(emote))
        await ctx.send(f"Wrong guess emote set to: {emote}")

    @countingset.command(name="leaderboard")
    async def view_leaderboard(self, ctx):
        """Displays the leaderboard."""
        leaderboard = await self.config.guild(ctx.guild).leaderboard()
        if leaderboard:
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
            leaderboard_str = "\n".join(f"{self.bot.get_user(int(user_id)).name}: {score}" for user_id, score in sorted_leaderboard)
            await ctx.send(f"**Leaderboard:**\n{leaderboard_str}")
        else:
            await ctx.send("The leaderboard is empty.")
