from discord.ext import commands
import discord
import random

class CatRating(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name='ratecat',
        description="Rate someone as a cat from 1 to 10"
    )
    async def rate_cat(self, ctx, user: discord.Member = None):
        """Rates a mentioned user as a cat."""
        if not user:
            await ctx.send("Mention someone to rate as a cat! (`>ratecat @user`)")
            return

        rating = random.randint(1, 10)
        comments = {
            10: "Absolute purrfection! 🐱✨",
            9: "Flufftastic! So majestic 😻",
            8: "Very cuddly and cute 😽",
            7: "What a playful furball 🐾",
            6: "Silly and soft 😸",
            5: "Meow-average, but still loved 💗",
            4: "Grumpy but charming 😼",
            3: "Definitely a cat... maybe 😼",
            2: "Chaos in fur form 😹",
            1: "So mischievous it’s adorable 😼💥"
        }

        comment = comments.get(rating, "A unique kitty!")
        embed = discord.Embed(
            title="🐾 Cat Rating 🐾",
            description=f"I rate {user.mention} a **{rating}/10**\n{comment}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CatRating(bot))
