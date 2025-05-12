from typing import Optional
import os
from pdf2image import convert_from_path
from PIL import Image

import discord
from discord import app_commands
from discord.ext import commands

from pasta import file_to_dict, DATA

data = DATA
channels: dict = file_to_dict(data + "channels.json")


class Latex(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # LaTeX generate command
    @app_commands.command(
        name="latex",
        description="Generates an image using LaTeX from a given prompt that uses LaTeX syntax."
    )
    async def latex(
            self, 
            inter: discord.Interaction, 
            prompt: str
        ) -> None:
        """ Convert a text prompt to a generated LaTeX file """
        
        
        await inter.response.send_message("Processing....")
        # Generates a unique file name (in case multiple being processed at the same time)
        fname: str = str(inter.id)
        
        
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
        images: list[Image.Image] = convert_from_path(f"{fname}.pdf", 1000)
        images[0].save(f"image{fname}.jpg", "JPEG")
        
        
        # getting embed
        embed: discord.Embed = discord.Embed(
            title="LaTeX output",
            color=0xEEDB83,
            description=prompt
        )
        
        file = discord.File(f"image{fname}.jpg", filename=f"image{fname}.jpg")
        embed.set_image(url=f"attachment://image{fname}.jpg")
        
        await inter.response.defer()
        
        # sending
        await inter.edit_original_response(
            content=None,
            file=file,
            embed=embed   
        )
        
        # Removing all the files made
        os.remove(f"{fname}.aux")
        os.remove(f"{fname}.log")
        os.remove(f"{fname}.pdf")
        os.remove(f"{fname}.tex")
        os.remove(f"image{fname}.jpg")
        # os.remove(f"crop{fname}.jpg")
        

    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Latex(bot))