import discord
from discord.ext import commands
import asyncio

# Define your bot's prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Define the user ID to apply the limit to
LIMITED_USER_ID = 'put user id here'

# Define the cooldown time and maximum messages
COOLDOWN_TIME = 84600  # in seconds
MAX_MESSAGES = 5

# Counter for the number of messages sent by the limited user
message_count = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    global message_count
    
    # Ignore messages from bots
    if message.author.bot:
        return

    # Check if the message is from the limited user
    if message.author.id == LIMITED_USER_ID:
        # Increment message count
        message_count += 1
        await message.channel.send(f"{5 - message_count} left")
        # Check if the user has reached the maximum messages
        if message_count > MAX_MESSAGES:
            await message.delete()
            await message.channel.send(f"<@{LIMITED_USER_ID}>, you are sending messages too quickly. Please slow down.")

        # Reset message count after cooldown time
        await asyncio.sleep(COOLDOWN_TIME)
        message_count -= 1

    await bot.process_commands(message)

# Run the bot with your token
bot.run('Discord token here')
