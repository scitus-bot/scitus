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
        name="latexraw",
        description="Generates an image using LaTeX from a given prompt that uses LaTeX syntax."
    )
    async def latexraw(
            self, 
            inter: discord.Interaction, 
            prompt: str,
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
            description=prompt,
        )
        
        # print(inter.user.display_name)
        # print(str(inter.user.display_name))
        
        embed.set_author(name=str(inter.user.display_name), icon_url=inter.user.display_avatar.url)
        
        
        
        file = discord.File(f"image{fname}.jpg", filename=f"image{fname}.jpg")
        embed.set_image(url=f"attachment://image{fname}.jpg")
        
        # sending
        await inter.channel.send(
            content=None,
            file=file,
            embed=embed   
        )
        
        # deleting original response
        await inter.delete_original_response()
        
        # Removing all the files made
        os.remove(f"{fname}.aux")
        os.remove(f"{fname}.log")
        os.remove(f"{fname}.pdf")
        os.remove(f"{fname}.tex")
        os.remove(f"image{fname}.jpg")
        # os.remove(f"crop{fname}.jpg")
        
        
        
        
    # LaTeX generate command
    @app_commands.command(
        name="latexmsg",
        description="Generates a latec thing from a message id"
    )
    async def latexmsg(
            self, 
            inter: discord.Interaction, 
            messageid: str,
        ) -> None:
        """ Convert a text prompt to a generated LaTeX file """
        
        await inter.response.send_message("Processing....")
        
        try:
            message = await inter.channel.fetch_message(messageid)
        except:
            await inter.edit_original_response("Failed to get message. Check your message ID?")
        
        # Generates a unique file name (in case multiple being processed at the same time)
        fname: str = str(inter.id)
        
        # getting prompt from message
        
        message_list: list = message.content.split("\n")
        message_list.pop(0)
        message_list.pop()

        prompt = "\n".join(message_list)


        
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
            description=prompt,
        )
        
        # print(inter.user.display_name)
        # print(str(inter.user.display_name))
        
        embed.set_author(name=str(inter.user.display_name), icon_url=inter.user.display_avatar.url)
        
        file = discord.File(f"image{fname}.jpg", filename=f"image{fname}.jpg")
        embed.set_image(url=f"attachment://image{fname}.jpg")
        
        # sending
        await inter.channel.send(
            content=None,
            file=file,
            embed=embed   
        )
        
        # deleting original response
        await inter.delete_original_response()
        
        # Removing all the files made
        os.remove(f"{fname}.aux")
        os.remove(f"{fname}.log")
        os.remove(f"{fname}.pdf")
        os.remove(f"{fname}.tex")
        os.remove(f"image{fname}.jpg")
        # os.remove(f"crop{fname}.jpg")

        
        
    @latexmsg.error
    async def latexmsg_error(self, inter: discord.Interaction, error: Exception) -> None:
        if isinstance(error, discord.NotFound):
            await inter.edit_original_response("Message not found")
        elif isinstance(error, discord.Forbidden):
            await inter.edit_original_response("Do not have permissions required to get message")

        elif isinstance(error, discord.HTTPException):
            await inter.edit_original_response("Retrieving the message failed. ")
        
        

    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Latex(bot))