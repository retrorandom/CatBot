import discord
from discord.ext import commands, tasks
import json
import os
import time
import asyncio
import random
import sys

def ensure_config_exists():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    if not os.path.exists(config_path):
        # Create default config with your exact structure
        default_config = {
            "discord_token": ""
        }

        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        print("Created config.json")
        print("Please edit config.json and add your Discord bot token!")
        return False
    return True


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    # Ensure config exists first
    if not ensure_config_exists():
        sys.exit(1)

    # Load the config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading config.json: {e}")
        sys.exit(1)

    # Validate token exists and isn't empty
    if not config.get('discord_token') or config['discord_token'].strip() == "":
        print("Please set your Discord bot token in config.json")
        print("The discord_token field is empty")
        sys.exit(1)

    return config

config = load_config()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents, help_command=None)

start_time = time.time()
bot.start_time = start_time

# List of rotating statuses
statuses = [
    discord.Game("Meowing Back At Cat's ₍^. .^₎⟆"),
    discord.Game("Chasing lasers 🔦"),
    discord.Game("Napping in the sun ☀️"),
    discord.Game("Playing with yarn 🧶"),
    discord.Activity(type=discord.ActivityType.watching, name="cat videos on YouTube"),
    discord.Activity(type=discord.ActivityType.listening, name="purrs and meows"),
    discord.Activity(type=discord.ActivityType.competing, name="Cat Olympics"),
]


@tasks.loop(seconds=60)  # Change every 60 seconds
async def rotate_status():
    new_status = random.choice(statuses)
    await bot.change_presence(status=discord.Status.online, activity=new_status)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    await rotate_status.start()


# Absolute path to cogs folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COGS_DIR = os.path.join(BASE_DIR, 'cogs')


async def load_cogs():
    if os.path.exists(COGS_DIR):
        for filename in os.listdir(COGS_DIR):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f"Loaded cog: {filename[:-3]}")
                except Exception as e:
                    print(f"Failed to load cog {filename[:-3]}: {e}")
    else:
        print("⚠️  No cogs folder found - creating empty cogs directory")
        os.makedirs(COGS_DIR, exist_ok=True)


async def main():
    async with bot:
        await load_cogs()
        try:
            await bot.start(config["discord_token"])
        except discord.LoginFailure:
            print("Invalid Discord token! Please check your config.json")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nCat bot stopped by user")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())