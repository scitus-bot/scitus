from random import choice

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
        await inter.response.send_message(f"Pong! ({round(self.bot.latency * 1000)}ms)")
    

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
    async def report(self, inter: discord.Interaction, member: discord.Member, reason: Optional[str] = "") -> None:
        report = self.bot.get_channel(ChannelIDs.report)
        
        await inter.response.send_message("Reported Successfully!", ephemeral=True)
            
        embed=discord.Embed(title="Report", color=0xff0000)
        embed.set_thumbnail(url=inter.guild.icon.url)
        embed.add_field(name="User Reported:", value=member.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Reported By:", value=inter.user.mention, inline=True)
        await report.send(embed=embed)
            

#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="avatar",
        description="Gets the avatar of a user."
    )
    async def avatar(self, inter: discord.Interaction, member: Optional[discord.Member] = None) -> None:
        member = member or inter.user
        
        embed = discord.Embed(title="Avatar", description=f"{member.name}'s avatar.", color=0xEEDB83) 
        embed.set_image(url=member.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="rng",
        description="RNG"
    )
    async def button(self, inter: discord.Interaction, min: int, max: int, weight: Optional[int] = 0) -> None:
        pass
        
#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="info",
        description="Gets the server info."
    )
    async def info(self, inter: discord.Interaction) -> None:
        
        embed = discord.Embed(title=f"{inter.guild.name}'s Info", color=0xEEDB83) 
        
        infoStr: str = f"Member count: {inter.guild.member_count}\nCreated at: {inter.guild.created_at}"
        
        embed.add_field(name="Server Info", value=infoStr)
        embed.set_image(url=inter.guild.icon.url)
        await inter.response.send_message(embed=embed)
    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Everyone(bot))