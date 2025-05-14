from typing import Optional
import os
from pdf2image import convert_from_path
from PIL import Image

import discord
from discord import app_commands
from discord.ext import commands

from pasta import file_to_dict, DATA, fail_embed, process_embed

data = DATA
channels: dict = file_to_dict(data + "channels.json")


def prompt_to_embed(
        filename: str, 
        prompt: str, 
        preamble: str = None, 
        minipage: int = None,
        compiler: str = "pdflatex"
    ) -> discord.Embed:
    """ Generates a discord embed with LaTeX generated image attached 
    Parameters
    ----------
    filename: str
        The filename used for the `.tex` file, usually `inter.id`. Do not include the extension. 
    prompt: str 
        LaTeX code that will be used to generate the output PDF.
    preamble: str, optional
        Name of the `.tex` file stored in `~/data/latex/` to be used in the preamble. Defaults to `None`, in which case no preamble is used.
    minipage: int, optional
        This is the width of the minipage used for when LaTeX is generated from a message. Defaults to `None`, in which case no minipage is used. 
    compiler: str, optional
        What LaTeX compiler to use. Defaults to `pdflatex`."""
        
    # creating source .tex file
    with open(f"{filename}.tex", "w") as file:
        # list of lines then will file.writelines(lines) at the end
        lines: list = []
        lines.append("\\documentclass[border={2pt, 2pt, 2pt, 2pt}]{standalone}")
        
        # if user has passed a preamble
        if preamble: 
            path: str = "data/latex/" + preamble + ".tex"
            lines.append("\\input{" + path + "}")
            
        # begin document
        lines.append("\\begin{document}")

        # if user has passed in a minipage length
        if minipage:
            lines.append("\\begin{minipage}{" + str(minipage) + "}")
            
        # write user prompt
        lines.append(prompt)

        # close the minipage
        if minipage:
            lines.append("\\end{minipage}")
            
        # end document
        lines.append("\\end{document}")
        
    # running latex
    try:
        os.system(f"{compiler} {filename}.tex")
    except Exception as e:
        return fail_embed(e)
    
    # pdf to images
    images: list[Image.Image] = convert_from_path(f"{filename}.pdf", 1000)
    images[0].save(f"image{filename}.jpg", "JPEG")

    # creating embed
    # author and description set elsewhere
    embed: discord.Embed = discord.Embed(
        title="LaTeX output",
        colour=0xEEDB83
    )
    
    attachment = discord.File(f"image{filename}.jpg", filename=f"image{filename}.jpg")
    embed.set_image(url=f"attachment://image{filename}.jpg")
        
    # Removing all the files made
    os.remove(f"{filename}.aux")
    os.remove(f"{filename}.log")
    os.remove(f"{filename}.pdf")
    os.remove(f"{filename}.tex")
        
    return embed



class Latex(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # LaTeX generate command
    @app_commands.command(
        name="maths",
        description="Generates a LaTeX image from given LaTeX prompt. Recommended for shorter equations."
    )
    async def maths(
            self, 
            inter: discord.Interaction, 
            prompt: str,
        ) -> None:
        """ Convert a text prompt to a generated LaTeX file """
        
        # while it is processing
        await inter.response.send_message(content=None, embed=process_embed())
        
        # Generates a unique file name (in case multiple being processed at the same time)
        fname: str = str(inter.id)
        
        # getting embed
        embed = prompt_to_embed(fname, prompt, preamble="maths")
        
        # setting things
        embed.description = prompt
        embed.set_author(name=str(inter.user.display_name), icon_url=inter.user.display_avatar.url)
        embed.set_image(url=f"attachment://image{fname}.jpg")
                
        file = discord.File(f"image{fname}.jpg", filename=f"image{fname}.jpg")
        
        # sending
        await inter.channel.send(
            content=None,
            file=file,
            embed=embed
        )
        
        # deleting original response because you can't edit the file parameter of a message after its sent
        await inter.delete_original_response()
        
        # delete the image file
        os.remove(f"image{fname}.jpg")
        
        
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
                 "\\usepackage[utf8]{inputenc}\n"
                 "\\usepackage{latexsym,amsfonts,amssymb,amsmath}\n"
                "\\begin{document}\n")
            )
            l.write(prompt)
            l.write(
                ("\n\\end{document}")
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
            description=message.jump_url,
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