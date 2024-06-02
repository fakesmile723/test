import random
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import discord

class Counting(commands.Cog):
    """Cog for a counting game with leaderboards, custom reactions, per-guild configuration, and shame role."""

    default_guild = {
        "current_number": 0,
        "channel_id": None,
        "leaderboard": {},
        "correct_emote": "✅",
        "wrong_emote": "❌",
        "shame_role": None,
        "last_counter_id": None
    }

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=271828, force_registration=True)
        self.config.register_guild(**self.default_guild)

    @commands.command()
    async def startcounting(self, ctx, channel: discord.TextChannel, shame_role: discord.Role):
        """Starts the counting game in the specified channel with the given shame role."""
        await self.config.guild(ctx.guild).channel_id.set(channel.id)
        await self.config.guild(ctx.guild).current_number.set(1)
        await self.config.guild(ctx.guild).leaderboard.set({})
        await self.config.guild(ctx.guild).shame_role.set(shame_role.id)
        await self.config.guild(ctx.guild).last_counter_id.set(None)  # Reset last counter
        await channel.send("Counting game started! Next number: 1")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handles messages in the counting game channel."""
        if message.author.bot:
            return

        guild_config = await self.config.guild(message.guild).all()
        if guild_config["channel_id"] == message.channel.id:
            try:
                next_number = int(message.content)
                last_counter_id = await self.config.guild(message.guild).last_counter_id()
                if next_number == guild_config["current_number"] + 1 and message.author.id != last_counter_id:
                    await self.config.guild(message.guild).current_number.set(next_number)
                    await self.config.guild(message.guild).last_counter_id.set(message.author.id)
                    await message.add_reaction(guild_config["correct_emote"])

                    leaderboard = guild_config["leaderboard"]
                    user_id = str(message.author.id)
                    leaderboard[user_id] = leaderboard.get(user_id, 0) + 1
                    await self.config.guild(message.guild).leaderboard.set(leaderboard)
                else:
                    await message.add_reaction(guild_config["wrong_emote"])

                    # Reset count and give shame role
                    shame_role = message.guild.get_role(guild_config["shame_role"])
                    await message.author.add_roles(shame_role, reason="Wrong count or double counting")
                    await self.config.guild(message.guild).current_number.set(1)
                    await self.config.guild(message.guild).last_counter_id.set(None)

                    # Send roasting message
                    roasts = [
                        f"{message.author.name} can't count! Back to the start we go!",
                        f"{message.author.name} tried to cheat! Shame on you!",
                        f"{message.author.name} is bad at math! Let's start over.",
                    ]
                    roast = random.choice(roasts)
                    await message.channel.send(embed=discord.Embed(description=roast, color=discord.Color.red()))

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
        """Displays the leaderboard in an embed."""
        leaderboard = await self.config.guild(ctx.guild).leaderboard()
        if leaderboard:
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
            embed = discord.Embed(title="Counting Game Leaderboard", color=discord.Color.blue())
            for user_id, score in sorted_leaderboard[:10]:  # Show top 10
                user = self.bot.get_user(int(user_id))
                embed.add_field(name=user.name, value=score, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("The leaderboard is empty.")
