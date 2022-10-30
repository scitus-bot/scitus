""" 
Commands List:
    ping
    sus
    report
    avatar
    remindme
"""


from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from pasta import ChannelIDs



class Everyone(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="ping",
        description="Pings the bot to check if it's online."
    )
    async def ping(self, inter: discord.Interaction) -> None:
        await inter.response.send_message("Pong!")
    

#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="sus",
        description="sus",
    )
    async def sus(self, inter: discord.Interaction) -> None:
        await inter.response.send_message("ඞ")
        

#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="report",
        description="Use to report someone anonymously.",
    )
    async def report(self, inter: discord.Interaction, member: discord.Member, reason: Optional[str] = None) -> None:
        report = self.bot.get_channel(ChannelIDs.report)
        
        await inter.response.send_message("Reported Successfully!")
        await inter.delete_original_response()
        
        await report.send(f"Reporter: {inter.user.mention}\nReported: {member.mention}")
        if reason is not None:
            await report.send(f"Reason: {reason}")
            
            

#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="avatar",
        description="Gets the avatar of a user."
    )
    async def avatar(self, inter: discord.Interaction, member: Optional[discord.Member] = None) -> None:
        member = member or inter.user
        await inter.response.send_message(member.display_avatar)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Everyone(bot))