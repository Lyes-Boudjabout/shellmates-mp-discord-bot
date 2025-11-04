import os
import random
import discord
import logging
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

from api_client import APIClient

# === Load environment variables === #
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("DISCORD_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
FACTS_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/facts"
EVENTS_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/events"
JOKES_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/jokes"
QUIZ_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/quiz"

# === Logging configuration === #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CyberBot")

# === Discord bot setup === #
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# === Event hook === #
@bot.event
async def on_ready():
    await bot.tree.sync()
    logger.info(f"✅ CyberBot connected as {bot.user} and ready.")
    print(f"CyberBot connected as {bot.user}")


# === Slash Commands === #

# /events — list all events
@bot.tree.command(name="events", description="List upcoming club events.")
async def events(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    async with APIClient(EVENTS_ENDPOINT) as api:
        events = await api.get_events()

    if not events:
        await interaction.followup.send("📭 No upcoming events found.")
        return

    embed = discord.Embed(title="Upcoming Club Events", color=discord.Color.blue())
    for e in events:
        embed.add_field(
            name=f"{e.get('title', 'Untitled')} — {e.get('date', 'TBD')}",
            value=f"{e.get('description', '')}\n📍 {e.get('location', '')}",
            inline=False
        )
    await interaction.followup.send(embed=embed)


# /add_event — add a new event
@bot.tree.command(name="add_event", description="Add a new club event (Admin only).")
@app_commands.describe(
    title="Title of the event",
    date="Date and time of the event",
    description="Brief event description",
    location="Event location or link"
)
async def add_event(interaction: discord.Interaction, title: str, date: str, description: str, location: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You lack permission to add events.", ephemeral=True)
        return

    event_data = {"title": title, "date": date, "description": description, "location": location}
    async with APIClient(EVENTS_ENDPOINT) as api:
        result = await api.create_event(event_data)

    if result:
        await interaction.response.send_message(f"✅ Event **'{title}'** added successfully!")
    else:
        await interaction.response.send_message("⚠️ Failed to add event.", ephemeral=True)


# /update_event — update an existing event (Admin only)
@bot.tree.command(name="update_event", description="Update an existing club event (Admin only).")
@app_commands.describe(
    event_id="ID of the event to update",
    title="New title (optional)",
    date="New date (optional)",
    description="New description (optional)",
    location="New location (optional)"
)
async def update_event(interaction: discord.Interaction, event_id: str, title: str = None, date: str = None, description: str = None, location: str = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You lack permission to update events.", ephemeral=True)
        return

    # Build the payload with only provided fields
    update_data = {}
    if title: update_data["title"] = title
    if date: update_data["date"] = date
    if description: update_data["description"] = description
    if location: update_data["location"] = location

    if not update_data:
        await interaction.response.send_message("⚠️ No fields provided to update.", ephemeral=True)
        return

    async with APIClient(EVENTS_ENDPOINT) as api:
        updated = await api.update_event(event_id, update_data)

    if updated:
        await interaction.response.send_message(f"✅ Event **'{event_id}'** updated successfully!")
    else:
        await interaction.response.send_message("⚠️ Failed to update event (check ID or permissions).", ephemeral=True)


# /remove_event — delete an event by ID
@bot.tree.command(name="remove_event", description="Remove an existing event (Admin only).")
@app_commands.describe(event_id="ID of the event to remove")
async def remove_event(interaction: discord.Interaction, event_id: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You lack permission to remove events.", ephemeral=True)
        return

    async with APIClient(EVENTS_ENDPOINT) as api:
        success = await api.delete_event(event_id)

    if success:
        await interaction.response.send_message(f"🗑️ Event deleted successfully.")
    else:
        await interaction.response.send_message("⚠️ Event not found or could not be removed.", ephemeral=True)


# /cyberfact — random fact
@bot.tree.command(name="cyberfact", description="Get a random cybersecurity fact.")
async def cyberfact(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    async with APIClient(FACTS_ENDPOINT) as api:
        facts = await api.get_facts()

    if not facts:
        await interaction.followup.send("📭 No cybersecurity facts available.")
        return

    fact = random.choice(facts)
    await interaction.followup.send(f"💡 **Cyber Fact:** {fact.get('content', str(fact))}")


# /add_fact — add a fact (admin-only)
@bot.tree.command(name="add_fact", description="Add a new cybersecurity fact (Admin only).")
@app_commands.describe(fact="Enter the cybersecurity fact text")
@app_commands.checks.has_permissions(administrator=True)
async def add_fact(interaction: discord.Interaction, fact: str):
    payload = {"content": fact}
    async with APIClient(FACTS_ENDPOINT) as api:
        result = await api.create_fact(payload)

    if result:
        await interaction.response.send_message("✅ Cybersecurity fact added successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ Failed to add fact.", ephemeral=True)


# /cyberjoke — random joke
@bot.tree.command(name="cyberjoke", description="Get a random cybersecurity joke.")
async def cyberjoke(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    async with APIClient(JOKES_ENDPOINT) as api:
        jokes = await api.get_jokes()

    if not jokes:
        await interaction.followup.send("📭 No cybersecurity jokes available.")
        return

    joke = random.choice(jokes)
    await interaction.followup.send(f"💡 **Cyber joke:** {joke.get('content', str(joke))}")


# /add_joke — add a joke (admin-only)
@bot.tree.command(name="add_joke", description="Add a new cybersecurity joke (Admin only).")
@app_commands.describe(joke="Enter the cybersecurity joke text")
@app_commands.checks.has_permissions(administrator=True)
async def add_joke(interaction: discord.Interaction, joke: str):
    payload = {"content": joke}
    async with APIClient(JOKES_ENDPOINT) as api:
        result = await api.create_joke(payload)

    if result:
        await interaction.response.send_message("✅ Cybersecurity joke added successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ Failed to add joke.", ephemeral=True)

# /quiz — Play a random quiz
@bot.tree.command(name="quiz", description="Test your cybersecurity knowledge with a random quiz!")
async def quiz(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    async with APIClient(QUIZ_ENDPOINT) as api:
        quizzes = await api.get_quizzes()

    if not quizzes:
        await interaction.followup.send("📭 No quizzes available right now.")
        return

    quiz = random.choice(quizzes)
    question = quiz.get("question", "Unknown question")
    options = quiz.get("options", [])
    correct_option = quiz.get("correct_option", 0)

    if not options:
        await interaction.followup.send("⚠️ This quiz has no options defined.")
        return

    view = discord.ui.View()

    async def make_callback(choice_index: int):
        async def callback(inter_btn: discord.Interaction):
            if choice_index == correct_option:
                await inter_btn.response.send_message("✅ Correct!", ephemeral=True)
            else:
                await inter_btn.response.send_message(
                    f"❌ Wrong! The correct answer was **{options[correct_option]}**.",
                    ephemeral=True
                )
            for child in view.children:
                child.disabled = True
            await inter_btn.message.edit(view=view)
        return callback

    for i, option in enumerate(options):
        button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary)
        button.callback = await make_callback(i)
        view.add_item(button)

    embed = discord.Embed(title="🧠 Cybersecurity Quiz", description=question, color=discord.Color.orange())
    await interaction.followup.send(embed=embed, view=view)

# /add_quiz — Add a new quiz (Admin only)
@bot.tree.command(name="add_quiz", description="Add a new cybersecurity quiz (Admin only).")
@app_commands.describe(
    question="Quiz question text",
    options="Comma-separated list of options (e.g. A,B,C,D)",
    correct_index="The number (starting from 1) of the correct answer"
)
async def add_quiz(interaction: discord.Interaction, question: str, options: str, correct_index: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You lack permission to add quizzes.", ephemeral=True)
        return

    # Parse & clean options, remove empty ones
    options_list = [opt.strip() for opt in options.split(",") if opt.strip() != ""]
    if len(options_list) < 2:
        await interaction.response.send_message("⚠️ You must provide at least 2 non-empty options (comma-separated).", ephemeral=True)
        return

    # Accept 1-based index from user and convert to 0-based internally
    # (user-friendly: 1 = first option, 2 = second, ...)
    user_index = correct_index
    if user_index < 1 or user_index > len(options_list):
        await interaction.response.send_message(f"⚠️ Invalid correct answer number. Send a number between 1 and {len(options_list)} (1 = first option).", ephemeral=True)
        return

    correct_zero_based = user_index - 1

    quiz_data = {
        "question": question,
        "options": options_list,
        "correct_option": correct_zero_based
    }

    async with APIClient(QUIZ_ENDPOINT) as api:
        result = await api.create_quiz(quiz_data)

    if result:
        await interaction.response.send_message("✅ Quiz added successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ Failed to add quiz.", ephemeral=True)



# /help — list all commands
@bot.tree.command(name="help", description="Display all available commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📘 CyberBot Command List", color=discord.Color.green())
    embed.add_field(name="/events", value="List upcoming club events.", inline=False)
    embed.add_field(name="/add_event", value="Add a new event (Admin only).", inline=False)
    embed.add_field(name="/update_event", value="Update an event (Admin only).", inline=False)
    embed.add_field(name="/remove_event", value="Remove an event (Admin only).", inline=False)
    embed.add_field(name="/cyberfact", value="Get a random cybersecurity fact.", inline=False)
    embed.add_field(name="/add_fact", value="Add a new fact (Admin only).", inline=False)
    embed.add_field(name="/cyberjoke", value="Get a random cybersecurity joke.", inline=False)
    embed.add_field(name="/add_joke", value="Add a new joke (Admin only).", inline=False)
    embed.add_field(name="/quiz", value="Play a random cybersecurity quiz.", inline=False)
    embed.add_field(name="/add_quiz", value="Add a new quiz (Admin only).", inline=False)
    embed.add_field(name="/help", value="Show this help message.", inline=False)
    await interaction.response.send_message(embed=embed)


# === Error Handler for Permissions === #
@add_fact.error
@add_joke.error
@add_event.error
@update_event.error
@remove_event.error
@add_quiz.error
async def permission_error(interaction: discord.Interaction, error: Exception):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ You lack administrator permissions.", ephemeral=True)
    else:
        logger.error(f"Unhandled error in command: {error}")
        await interaction.response.send_message("⚠️ An unexpected error occurred.", ephemeral=True)


# === Run the Bot === #
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("❌ DISCORD_TOKEN not found in environment.")
    bot.run(TOKEN)
