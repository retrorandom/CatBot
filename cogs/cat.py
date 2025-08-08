from discord.ext import commands
from api.cat_api import get_random_cat, get_cat_fact

class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='cat', description="Get a random cat picture")
    async def cat(self, ctx):
        await ctx.send(get_random_cat())

    @commands.hybrid_command(name='randomcat', description="Get another random cat picture")
    async def randomcat(self, ctx):
        await ctx.send(get_random_cat())

    @commands.hybrid_command(name='catfact', description="Get a random cat fact")
    async def catfact(self, ctx):
        fact = get_cat_fact()
        await ctx.send(f"🐾 **Cat Fact:** {fact}")

async def setup(bot):
    await bot.add_cog(Cat(bot))
