# from bardapi import Bard
# from redbot.core import commands
# from Bard import Chatbot
# import os
# import discord


import discord
from redbot.core import commands
from Bard import Chatbot

class BAIChat(commands.Cog):
    def __init__(self, bot: commands.Bot, bard_token: str, use_images: bool = False):
        self.bot = bot
        self.bard = Chatbot(bard_token)
        self.use_images = use_images

    @commands.command(name='chat')
    async def chat(self, ctx: commands.Context, *, message: str):
        max_length = 1900
        response = self.bard.ask(message)
        if not response:
            await ctx.reply("I couldn't generate a response. Please try again.")
            return
        images = response['images']
        words = response['content'].split()
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

        for chunk in formatted_chunks:
            await ctx.reply(chunk)
        if self.use_images and images:
            for image in images:
                await ctx.send(image)

def setup(bot: commands.Bot):
    # Set your Google Bard API token here
    bard_token = "XQgKEYeG9Dbv3EdnRu3k8MUm0QJvFIQnKUDhcyxbrS6cxwBrLEYuDUjQgmn-zJM9tYMjkA."
    # Set whether to use images in responses (True or False)
    use_images = False
    bot.add_cog(BAIChat(bot, bard_token, use_images))