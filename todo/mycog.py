import discord
from discord.ext import commands
from discord.ui import Select,  Button, View

import pymongo


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        mongo_url = "your_mongo_url_here"
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client["todo"]
        self.collection = self.db["tasks"]

    @commands.command()
    async def add(self, ctx, *, task):
        self.collection.insert_one({"task": task})
        await ctx.send(f"Task '{task}' added to the list.")

    @commands.command()
    async def remove(self, ctx, *, task):
        if self.collection.find_one({"task": task}):
            self.collection.delete_one({"task": task})
            await ctx.send(f"Task '{task}' removed from the list.")
        else:
            await ctx.send(f"Task '{task}' not found in the list.")

    @commands.command()
    async def done(self, ctx, *, task):
        if self.collection.find_one({"task": task}):
            self.collection.update_one({"task": task}, {"$set": {"status": "done"}})
            await ctx.send(f"Task '{task}' marked as 'done'.")
        else:
            await ctx.send(f"Task '{task}' not found in the list.")

    @commands.command()
    async def delete(self, ctx, *, task):
        if self.collection.find_one({"task": task}):
            self.collection.delete_one({"task": task})
            await ctx.send(f"Task '{task}' deleted from the list.")
        else:
            await ctx.send(f"Task '{task}' not found in the list.")

    @commands.command()
    async def edit(self, ctx, *, task):
        if self.collection.find_one({"task": task}):
            view = EditView(task)
            await ctx.send("Please select an option:", view=view)
        else:
            await ctx.send(f"Task '{task}' not found in the list.")

    @commands.command()
    async def list(self, ctx):
        tasks = []
        for task in self.collection.find():
            tasks.append(task["task"])
        if tasks:
            view = TodoView(tasks)
            await ctx.send("Todo List:", view=view)
        else:
            await ctx.send("No tasks found in the list.")


class TodoView(View):
    def __init__(self, tasks):
        super().__init__()
        options = [{"label": task, "value": task} for task in tasks]
        self.add_item(Select(options=options, placeholder="Select a task to manage", min_values=1, max_values=1))
        self.add_item(Button(style=discord.ButtonStyle.red, label="Delete All", custom_id="delete_all"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.message.author:
            await interaction.response.send_message("You cannot interact with this message.", ephemeral=True)
            return False
        return True

    @staticmethod
    async def delete_all_tasks():
        mongo_url = "your_mongo_url_here"
        client = pymongo.MongoClient(mongo_url)
        db = client["todo"]
        collection = db["tasks"]
        collection.drop()

    @View.select(0)
    async def task_select(self, select_menu, selected_option):
        task = selected_option.value
        view = TaskView(task)
        await select_menu.response.edit_message(view=view)

    @View.button(0)
    async def delete_all(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.delete_all_tasks()
        await interaction.response.edit_message(content="All tasks deleted from the list.", view=None)


class TaskView(View):
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.add_item(Button(style=discord.ButtonStyle.green, label="Done", custom_id="done"))
        self.add_item(Button(style=discord.ButtonStyle.gray, label="Edit", custom_id="edit"))
        self.add_item(Button(style=discord.ButtonStyle.red, label="Delete", custom_id="delete"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.message.author:
            await interaction.response.send_message("You cannot interact with this message.", ephemeral=True)
            return False
        return True

    async def update_task(self, status=None, new_task=None):
        update_query = {}
        if status is not None:
            update_query.update({"status": status})
        if new_task is not None:
            update_query.update({"task": new_task})
            self.collection.update_one({"task": self.task}, {"$set": update_query})

            @View.button(0)
            async def done(self, button: discord.ui.Button, interaction: discord.Interaction):
                await self.update_task(status="done")
                await interaction.response.edit_message(content=f"Task '{self.task}' marked as 'done'.", view=None)

            @View.button(1)
            async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
                await interaction.response.edit_message(content=f"Please enter the new task for '{self.task}'.")
                try:
                    reply = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30.0)
                except asyncio.TimeoutError:
                    await interaction.followup.send("No response received. Task not updated.")
                    return
                new_task = reply.content
                self.update_task(new_task=new_task)
                await interaction.followup.send(f"Task '{self.task}' updated to '{new_task}'.", view=None)

            @View.button(2)
            async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
                self.collection.delete_one({"task": self.task})
                await interaction.response.edit_message(content=f"Task '{self.task}' deleted from the list.", view=None)
class EditView(View):
    def init(self, task):
        super().__init__()
        self.task = task
        self.add_item(Button(style=discord.ButtonStyle.green, label="Mark as Done", custom_id="done"))
        self.add_item(Button(style=discord.ButtonStyle.gray, label="Edit", custom_id="edit"))
        self.add_item(Button(style=discord.ButtonStyle.red, label="Delete", custom_id="delete"))
        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user != self.message.author:
                await interaction.response.send_message("You cannot interact with this message.", ephemeral=True)
                return False
            return True

        @View.button(0)
        async def done(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.bot.get_cog("Todo").done.invoke(interaction.message.channel, task=self.task)
            await interaction.response.edit_message(view=None)

        @View.button(1)
        async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.bot.get_cog("Todo").edit.invoke(interaction.message.channel, task=self.task)
            await interaction.response.edit_message(view=None)

        @View.button(2)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.bot.get_cog("Todo").delete.invoke(interaction.message.channel, task=self.task)
            await interaction.response.edit_message(view=None)
    def setup(bot):
        bot.add_cog(Todo(bot))