from typing import Optional
import os
from pdf2image import convert_from_path
from PIL import Image
from time import time


import discord
from discord import app_commands
from discord.ext import commands

from pasta import ChannelIDs


class MyView(discord.ui.View): 
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") 
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") 

def pdf_to_image(file_name: str) -> None:
    pages: list = convert_from_path(file_name, 500)
    for count, page in enumerate(pages):
        page.save(f"{count}.jpg", "JPEG")

    


class Everyone(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

#--------------------------------------------------------------------------------------------------------------------------
    # ping

    @app_commands.command(
        name="ping",
        description="Pings the bot to check if it's online."
    )
    async def ping(self, inter: discord.Interaction) -> None:
        """ Responds with the bot's latency """
        await inter.response.send_message(f"Pong! ({round(self.bot.latency * 1000)}ms)")
        

#--------------------------------------------------------------------------------------------------------------------------
    # report

    @app_commands.command(
        name="report",
        description="Use to report someone anonymously.",
    )
    async def report(
            self, inter: discord.Interaction,
            member: discord.Member, reason: Optional[str] = "") -> None:
        """ Reports a user """
        
        report = self.bot.get_channel(ChannelIDs.report)
        
        await inter.response.send_message("Reported Successfully!", ephemeral=True)
            
        embed: discord.Embed = discord.Embed(
            title="Report", 
            color=0xff0000,
        )
        embed.set_thumbnail(url=inter.guild.icon.url)
        embed.add_field(name="User Reported:", value=member.mention, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Reported By:", value=inter.user.mention, inline=True)
        await report.send(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # avatar

    @app_commands.command(
        name="avatar",
        description="Gets the avatar of a user."
    )
    async def avatar(
            self, inter: discord.Interaction,
            member: Optional[discord.Member] = None) -> None:
        """ Returns a user's avatar """
        await inter.response.send_message("....")
        
        member = member or inter.user
        
        embed: discord.Embed = discord.Embed(
            title="Avatar",
            description=f"{member.name}'s avatar.",
            color=0xEEDB83
        ) 
        embed.set_image(url=member.avatar.url)
        await inter.edit_original_response(content=None, embed=embed)

        
#--------------------------------------------------------------------------------------------------------------------------
    # server info

    @app_commands.command(
        name="info",
        description="Gets the server info."
    )
    async def info(self, inter: discord.Interaction) -> None:
        """ Server info """
        
        infoStr: str = f"Member count: {inter.guild.member_count}\nCreated at: {inter.guild.created_at}"
        
        embed = discord.Embed(
            title=f"{inter.guild.name}'s Info",
            color=0xEEDB83,
        )
        embed.add_field(name="Server Info", value=infoStr)
        embed.set_image(url=inter.guild.icon.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="buttoncommand",
    )
    async def buttoncommand(self, inter: discord.Interaction) -> None:
        await inter.response.send_message("button", view=MyView())


#--------------------------------------------------------------------------------------------------------------------------
    # LaTeX


    @app_commands.command(
        name="latex",
        description="Generates an image using LaTeX from a given prompt that uses LaTeX syntax."
    )
    async def latex(self, inter: discord.Interaction, prompt: str) -> None:
        """ Convert a text prompt to a generated LaTeX file """
        await inter.response.send_message("Processing....")
        
        # Generates a unique file name (in case multiple being processed at the same time)
        fname: str = str(round(time()))
        
        
        # Writing to the latex file
        with open(f"{fname}.tex", "w") as l:
            l.write(
                ("\\documentclass{slides}\n"
                "\\begin{document}\n\\begin{center}\n"
                "\\thispagestyle{empty}\n\\begin{math}\n")
            )
            l.write(prompt)
            l.write(
                ("\n\\end{math}\n\\end{center}\n\\end{document}")
            )
            
        
        # Compiling latex to pdf
        os.system(f"pdflatex -quiet {fname}.tex")
        
        
        # Converting pdf to an image
        images: list = convert_from_path(f"{fname}.pdf", 500)
        images[0].save(f"image{fname}.jpg", "JPEG")
        
        # Cropping and sending the generated image
        im = Image.open(f"image{fname}.jpg")
        im1 = im.crop((0, 1240, 4133, 3446))
        
        im1.save(f"crop{fname}.jpg")
        
        
        embed: discord.Embed = discord.Embed(
            title="LaTeX output",
            color=0xEEDB83
        )
        file = discord.File(f"crop{fname}.jpg", filename=f"crop{fname}.jpg")
        embed.set_image(url=f"attachment://crop{fname}.jpg")
        await inter.channel.send(
            content="** **",
            file=file,
            embed=embed   
        )
        await inter.delete_original_response()
        
        # Removing all the files made
        os.remove(f"{fname}.aux")
        os.remove(f"{fname}.log")
        os.remove(f"{fname}.pdf")
        os.remove(f"{fname}.tex")
        os.remove(f"image{fname}.jpg")
        os.remove(f"crop{fname}.jpg")
        
    
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Everyone(bot))