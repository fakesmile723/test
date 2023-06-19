import discord
from redbot.core import commands

class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = "todo.csv"
        self.todos = self.load_todos()

    @commands.command(name="addtodo")
    async def add_todo(self, ctx, *, task: str):
        """Add a new task to the todo list."""
        if task not in self.todos:
            self.todos.append({"task": task, "done": False})
            self.save_todos()
            await ctx.send(f"Added '{task}' to the todo list.")
        else:
            await ctx.send(f"'{task}' is already on the todo list.")

    @commands.command(name="deltodo")
    async def del_todo(self, ctx, *, task: str):
        """Remove a task from the todo list."""
        for i, todo in enumerate(self.todos):
            if todo["task"] == task:
                del self.todos[i]
                self.save_todos()
                await ctx.send(f"Removed '{task}' from the todo list.")
                break
        else:
            await ctx.send(f"'{task}' is not on the todo list.")

    @commands.command(name="listtodo")
    async def list_todo(self, ctx):
        """List all tasks on the todo list."""
        if not self.todos:
            await ctx.send("The todo list is empty.")
        else:
            embed = discord.Embed(title="Todo List", color=0x00ff00)

            # Create dropdown options for each task on the todo list
            options = []
            for todo in self.todos:
                option = discord.SelectOption(label=todo["task"], value=todo["task"])
                options.append(option)
            
            # Add dropdown to the embed
            select = discord.ui.Select(placeholder="Select a task...", options=options)
            view = discord.ui.View()
            view.add_item(select)
            embed.set_footer(text="Use the dropdown to mark tasks as done.")
            await ctx.send(embed=embed, view=view)

            # Add event listener for when a dropdown option is selected
            async def select_callback(interaction: discord.Interaction):
                task = interaction.data["values"][0]
                for todo in self.todos:
                    if todo["task"] == task:
                        if not todo["done"]:
                            todo["done"] = True
                            self.save_todos()
                            await interaction.response.send_message(f"Marked '{task}' as done.")
                        else:
                            await interaction.response.send_message(f"'{task}' is already marked as done.")
                        break
                view.stop()
            
            select.callback = select_callback

    def load_todos(self):
        """Load the todo list from the CSV file."""
        try:
            with open(self.filepath, "r") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except FileNotFoundError:
            return []

    def save_todos(self):
        """Save the todo list to the CSV file."""
        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["task", "done"])
            writer.writeheader()
            writer.writerows(self.todos)
