from typing import Optional
import os
from pdf2image import convert_from_path
from PIL import Image
from time import time


import discord
from discord import app_commands
from discord.ext import commands

from pasta import file_to_dict, pdf_to_image, DATA

data = DATA
channels: dict = file_to_dict(data + "channels.json")



class MyView(discord.ui.View): 
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") 
    async def button_callback(self, inter: discord.Interaction, button):
        await inter.response.send_message("You clicked the button!", ephemeral=True) 

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
    placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
    min_values = 1, # the minimum number of values that must be selected by the users
    max_values = 1, # the maximum number of values that can be selected by the users
    options = [ # the list of options from which users can choose, a required field
        discord.SelectOption(
            label="Vanilla",
            description="Pick this if you like vanilla!"
        ),
        discord.SelectOption(
            label="Chocolate",
            description="Pick this if you like chocolate!"
        ),
        discord.SelectOption(
            label="Strawberry",
            description="Pick this if you like strawberry!"
        )
    ]
    )
    async def select_callback(self, inter: discord.Interaction, select): # the function called when the user is done selecting options
        await inter.response.send_message(f"Awesome! I like {select.values[0]} too!", ephemeral=True)





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
        
        latency: str = f"[{round(self.bot.latency *1000)}ms]"
        
        embed: discord.Embed = discord.Embed(
            title="Pong!",
            color=0xEEDB83,
            description=latency
        )
        
        await inter.response.send_message(embed=embed)
        

#--------------------------------------------------------------------------------------------------------------------------
    # report

    @app_commands.command(
        name="report",
        description="Use to report someone anonymously.",
    )
    async def report(
            self, 
            inter: discord.Interaction,
            member: discord.Member, 
            reason: Optional[str] = ""
        ) -> None:
        """ Reports a user """
        
        report = self.bot.get_channel(channels["report"])
        
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
            self, 
            inter: discord.Interaction,
            member: Optional[discord.Member] = None
        ) -> None:
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
                ("\\documentclass[border={2pt, 2pt, 2pt, 2pt}]{standalone}\n"
                 "\\usepackage{amssymb}\n"
                "\\begin{document}\n"
                "$\\displaystyle\n")
            )
            l.write(prompt)
            l.write(
                ("\n$\n\\end{document}")
            )
            
        
        # Compiling latex to pdf
        os.system(f"pdflatex -quiet {fname}.tex")
        
        
        # Converting pdf to an image
        images: list = convert_from_path(f"{fname}.pdf", 1000)
        images[0].save(f"image{fname}.jpg", "JPEG")
        
        # Cropping and sending the generated image
        # im = Image.open(f"image{fname}.jpg")
        # im1 = im.crop((0, 1240, 4133, 3446))
        
        # im1.save(f"crop{fname}.jpg")
        
        
        embed: discord.Embed = discord.Embed(
            title="LaTeX output",
            color=0xEEDB83,
            description=prompt
        )
        file = discord.File(f"image{fname}.jpg", filename=f"image{fname}.jpg")
        embed.set_image(url=f"attachment://image{fname}.jpg")
        await inter.channel.send(
            content=None,
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
        # os.remove(f"crop{fname}.jpg")
        

    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Everyone(bot))