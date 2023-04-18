from discord.ext import commands

# this does not work 

class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voice(bot))