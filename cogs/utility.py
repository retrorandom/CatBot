from discord.ext import commands
import discord
import time

def format_uptime(seconds):
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {sec}s"

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='uptime', description="Show how long the bot has been running")
    async def uptime(self, ctx):
        """Shows how long the bot has been online."""
        uptime = format_uptime(time.time() - self.bot.start_time)
        embed = discord.Embed(
            title="⏱️ Uptime",
            description=f"Bot has been running for: `{uptime}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='help', description="Show a list of available commands")
    async def help_command(self, ctx):
        """Shows the help message for CatBot."""
        embed = discord.Embed(
            title="🐱 CatBot Commands",
            description="Here's what I can do! Use these commands with `>` or `/`",
            color=discord.Color.pink(),
            timestamp=ctx.message.created_at if hasattr(ctx, "message") else discord.utils.utcnow()
        )

        embed.add_field(name="😺 Fun Commands", value=(
            "`>meow` — Show your meow count\n"
            "`>meowboard` — Leaderboard of meowers\n"
            "`>ratecat` — Rate you or another user as a cat :3\n"
            "`>catfact` — Get a random cat fact! :3"
        ), inline=False)

        embed.add_field(name="🐈 Cat Pics", value=(
            "`>cat` / `>randomcat` — Send a random cat image"
        ), inline=False)

        embed.add_field(name="⏱️ Utility", value=(
            "`>uptime` — See how long the bot has been running\n"
            "`>help` — Show this message"
        ), inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
