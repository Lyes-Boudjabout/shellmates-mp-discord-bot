import os
import random
import discord
import logging
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from bot.api_client import APIClient

# === Load environment variables === #
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("DISCORD_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

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
    async with APIClient(API_BASE_URL) as api:
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
    async with APIClient(API_BASE_URL) as api:
        result = await api.create_event(event_data)

    if result:
        await interaction.response.send_message(f"✅ Event **'{title}'** added successfully!")
    else:
        await interaction.response.send_message("⚠️ Failed to add event.", ephemeral=True)


# /remove_event — delete an event by ID
@bot.tree.command(name="remove_event", description="Remove an existing event (Admin only).")
@app_commands.describe(event_id="ID of the event to remove")
async def remove_event(interaction: discord.Interaction, event_id: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You lack permission to remove events.", ephemeral=True)
        return

    async with APIClient(API_BASE_URL) as api:
        success = await api.delete_event(event_id)

    if success:
        await interaction.response.send_message(f"🗑️ Event deleted successfully.")
    else:
        await interaction.response.send_message("⚠️ Event not found or could not be removed.", ephemeral=True)


# /cyberfact — random fact
@bot.tree.command(name="cyberfact", description="Get a random cybersecurity fact.")
async def cyberfact(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    async with APIClient(API_BASE_URL) as api:
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
    async with APIClient(API_BASE_URL) as api:
        result = await api.create_fact(payload)

    if result:
        await interaction.response.send_message("✅ Cybersecurity fact added successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ Failed to add fact.", ephemeral=True)


# /help — list all commands
@bot.tree.command(name="help", description="Display all available commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📘 CyberBot Command List", color=discord.Color.green())
    embed.add_field(name="/events", value="List upcoming club events.", inline=False)
    embed.add_field(name="/add_event", value="Add a new event (Admin only).", inline=False)
    embed.add_field(name="/remove_event", value="Remove an event (Admin only).", inline=False)
    embed.add_field(name="/cyberfact", value="Get a random cybersecurity fact.", inline=False)
    embed.add_field(name="/add_fact", value="Add a new fact (Admin only).", inline=False)
    embed.add_field(name="/help", value="Show this help message.", inline=False)
    await interaction.response.send_message(embed=embed)


# === Error Handler for Permissions === #
@add_fact.error
@add_event.error
@remove_event.error
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
