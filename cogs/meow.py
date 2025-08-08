from discord.ext import commands
import discord
import os
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'storage.json')

def load_data():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # Create file if missing
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"discord": {}}, f)
        return {"discord": {}}

    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            if "irc" in data:
                data = {"discord": data.get("discord", {})}
            return data
    except (json.JSONDecodeError, ValueError):
        print("Warning: storage.json is empty or invalid. Resetting file.")
        with open(DATA_FILE, 'w') as f:
            json.dump({"discord": {}}, f)
        return {"discord": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

class Meow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.meow_data = load_data()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()
        guild_id = str(message.guild.id) if message.guild else "DM"

        if not content.startswith(">"):
            if "meow" in content:
                try:
                    await message.add_reaction("🐈")
                except Exception as e:
                    print(f"Failed to add reaction: {e}")

                # Count the meows
                self.meow_data["discord"].setdefault(guild_id, {})
                user_id = str(message.author.id)
                self.meow_data["discord"][guild_id].setdefault(user_id, 0)
                self.meow_data["discord"][guild_id][user_id] += 1
                save_data(self.meow_data)

    @commands.hybrid_command(name='meow', description="Check how many times you've meowed")
    async def meow_counter(self, ctx):
        """Shows your personal meow count."""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id) if ctx.guild else "DM"
        count = self.meow_data["discord"].get(guild_id, {}).get(user_id, 0)
        embed = discord.Embed(
            title="😼 Meow Counter 😼",
            description=f"**Your meows:** `{count}`",
            color=discord.Color.pink()
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='meowboard', description="Show the meow leaderboard")
    async def meow_leaderboard(self, ctx):
        """Shows the top 10 meowers in the server."""
        guild_id = str(ctx.guild.id) if ctx.guild else "DM"
        guild_counts = self.meow_data["discord"].get(guild_id, {})
        if not guild_counts:
            await ctx.send("No meows yet! Start meowing 🐾")
            return

        sorted_users = sorted(guild_counts.items(), key=lambda x: x[1], reverse=True)
        leaderboard = ""
        for i, (user_id, count) in enumerate(sorted_users[:10], start=1):
            user = await self.bot.fetch_user(int(user_id))
            leaderboard += f"**{i}.** {user.name} — `{count}` meows\n"

        embed = discord.Embed(
            title="🏆 Meow Leaderboard 🏆",
            description=leaderboard,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Meow(bot))
