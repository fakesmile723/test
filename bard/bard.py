from bardapi import Bard , Chatbot
from redbot.core import commands
import os
import discord


class BAIChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reply_all = False
        self.use_images = False
        self.allow_dm = True
        self.active_channels = set()
        self.bard = Chatbot("xxxxxx")
        self.message_id = ""
        self.images = []

    async def generate_response(self, prompt: str) -> list:
        max_length = 1900
        response = self.bard.ask(prompt)
        if not response or "Google Bard encountered an error" in response["content"]:
            return []
        self.images = response["images"]
        words = response["content"].split()
        chunks = []
        current_chunk = []
        for word in words:
            if len(" ".join(current_chunk)) + len(word) + 1 > max_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
            else:
                current_chunk.append(word)
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        formatted_chunks = []
        for chunk in chunks:
            formatted_chunk = chunk.replace(" * ", "\n* ")
            formatted_chunks.append(formatted_chunk)
        return formatted_chunks

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="/help"))
        print(f"{self.bot.user.name} has connected to Discord!")
        invite_link = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=discord.Permissions(administrator=True),
            scopes=("bot", "applications.commands")
        )
        print(f"Invite link: {invite_link}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.reply_all or (message.reference and message.reference.resolved.author == self.bot.user):
            is_dm_channel = isinstance(message.channel, discord.DMChannel)
            if message.channel.id in self.active_channels or (self.allow_dm and is_dm_channel):
                user_prompt = message.content
                async with message.channel.typing():
                    response = await self.generate_response(user_prompt)
                for chunk in response:
                    await message.reply(chunk)
                if self.use_images:
                    if self.images:
                        for image in self.images:
                            await message.reply(image)

    @commands.group(name="chat", description="Have a chat with Bard")
    async def chat(self, ctx: commands.Context):
        pass

    @chat.command(name="start", description="Start chatting with Bard")
    async def start_chat(self, ctx: commands.Context, *, message: str):
        is_dm_channel = isinstance(ctx.channel, discord.DMChannel)
        if ctx.channel.id not in self.active_channels and not (self.allow_dm and is_dm_channel):
            return
        allowed_mentions = discord.AllowedMentions(users=False)
        interaction_response = f'> **{message}** - {ctx.author.mention} \n\n'
        response = await self.generate_response(message)
        await ctx.send(interaction_response, allowed_mentions=allowed_mentions)
        for chunk in response:
            try:
                await ctx.send(chunk)
            except discord.errors.HTTPException:
                await ctx.send("I couldn't generate a response. Please try again.")
        if self.use_images:
            if self.images:
                for image in self.images:
                    await ctx.send(image)

    @commands.command(name="toggledm", description="Toggle DM for chatting.")
    async def toggle_dm(self, ctx: commands.Context):
        self.allow_dm = not self.allow_dm
        await ctx.send(f"DMs are now {'allowed' if self.allow_dm else 'disallowed'} for active channels.")

    @commands.command(name="togglechannel", description="Toggle active channels.")
    async def toggle_active(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        if channel_id in self.active_channels:
            self.active_channels.remove(channel_id)
            await ctx.send(
                f"{ctx.channel.mention} has been removed from the list of active channels."
            )
        else:
            self.active_channels.add(channel_id)
            await ctx.send(
                f"{ctx.channel.mention} has been added to the list of active channels!"
            )

    @commands.command(name="reset", description="Reset the bot's context.")
    async def reset(self, ctx: commands.Context):
        self.bard.conversation_id = ""
        self.bard.response_id = ""
        self.bard.choice_id = ""
        await ctx.send("Bot context has been reset.")

    @commands.command(name="public", description="Toggle if bot should respond to /chat or all messages in chat.")
    async def public(self, ctx: commands.Context):
        if self.reply_all is False:
            self.reply_all = True
            await ctx.send(f"Bot will now respond to all messages in chat.")
        else:
            await ctx.send(f"Bot is already in public mode.")

    @commands.command(name="private", description="Toggle if bot should only respond to /chat or all messages in chat.")
    async def private(self, ctx: commands.Context):
        if self.reply_all:
            self.reply_all = False
            await ctx.send(f"Bot will now only respond to /chat.")
        else:
            await ctx.send(f"Bot is already in private mode.")

    @commands.command(name="images", description="Toggle if bot should respond with images")
    async def toggle_images(self, ctx: commands.Context):
        if self.use_images is False:
            self.use_images = True
            await ctx.send(f"Bot will now respond with images.")
        elif self.use_images:
            self.use_images = False
            await ctx.send(f"Bot will now respond with text.")
        else:
            await ctx.send(f"Unknown value for 'USE_IMAGES' environment variable.")

    @commands.command(name="help", description="Get all other commands!")
    async def bardhelp(self, ctx: commands.Context):
        embed = discord.Embed(title="Bot Commands", color=0x00ff00)
        embed.add_field(name="/chat start [message]", value="Start chatting with Bard.", inline=False)
        embed.add_field(name="/reset", value="Reset bot's context.", inline=False)
        embed.add_field(name="/togglechannel", value="Add the channel you are currently in to the Active Channel List.", inline=False)   
        embed.add_field(name="/toggledm", value="Toggle if DM chatting should be active", inline=False)
        embed.add_field(name="/public", value ="Toggle if bot should respond to all messages in chat", inline=False)
        embed.add_field(name="/private", value ="Toggle if bot should only respond to /chat", inline=False)
        embed.add_field(name="/images", value ="Toggle if bot should respond with images", inline=False)
        await ctx.send(embed=embed)