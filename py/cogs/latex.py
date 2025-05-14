from typing import Optional
import os
from pdf2image import convert_from_path
from PIL import Image

import discord
from discord import app_commands
from discord.ext import commands

from pasta import file_to_dict, DATA, fail_embed, process_embed, success_embed

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
            
            # if the user has set a preamble
            if os.path.isfile(path):
                lines.append("\\input{" + path + "}")
            
        # begin document
        lines.append("\\begin{document}")

        # if user has passed in a minipage length
        if minipage:
            lines.append("\\begin{minipage}{" + str(minipage) + "}")
            
        if preamble == "maths":
            lines.append("\\(")
            
        # write user prompt
        lines.append(prompt)
        
        if preamble == "maths":
            lines.append("\\)")

        # close the minipage
        if minipage:
            lines.append("\\end{minipage}")
            
        # end document
        lines.append("\\end{document}")
        
        file.writelines(lines)
        
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

    preamble_commands: app_commands.Group = app_commands.Group(name="preamble", description="...")

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
        embed.set_footer("`/maths`")
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
        name="latex",
        description="Generates a latec thing from a message id"
    )
    async def latex(
            self, 
            inter: discord.Interaction, 
            messageid: str,
            preamble: Optional[discord.User] = None,
            minipage: Optional[int] = 120
        ) -> None:
        """ Convert a text prompt to a generated LaTeX file """
        
        await inter.response.send_message(content=None, embed=process_embed())
        
        try:
            message = await inter.channel.fetch_message(messageid)
        except Exception as e:
            await inter.edit_original_response(content=None, embed=fail_embed(e))
            return
        
        
        # Generates a unique file name (in case multiple being processed at the same time)
        fname: str = str(inter.id)
        
        
        # getting prompt from message
        # this doesnt work if people put their last ``` on the same line
        message_list: list = message.content.split("\n")
        message_list.pop(0)
        message_list.pop()

        prompt = "\n".join(message_list)
        
        if preamble is None:
            preamble = inter.user

        embed: discord.Embed = prompt_to_embed(fname, prompt, str(preamble.id), minipage)
        
        embed.description = message.jump_url        
        embed.set_author(name=str(inter.user.display_name), icon_url=inter.user.display_avatar.url)
        embed.set_image(url=f"attachment://image{fname}.jpg")
        embed.set_footer(f"`/latex`. Using {preamble.mention} preamble. ")
        
        
        file = discord.File(f"image{fname}.jpg", filename=f"image{fname}.jpg")
        # sending
        await inter.channel.send(
            content=None,
            file=file,
            embed=embed   
        )
        
        # deleting original response
        await inter.delete_original_response()
        
        os.remove(f"image{fname}.jpg")
        
    @latex.error
    async def latex_error(self, inter: discord.Interaction, error: Exception) -> None:
        if isinstance(error, discord.NotFound):
            await inter.edit_original_response("Message not found")
        elif isinstance(error, discord.Forbidden):
            await inter.edit_original_response("Do not have permissions required to get message")

        elif isinstance(error, discord.HTTPException):
            await inter.edit_original_response("Retrieving the message failed. ")
        
        
    @preamble_commands.command(
        name="set",
        description="Let's you set a preamble from a message id. "
    )
    async def set(
            self, 
            inter: discord.Interaction, 
            messageid: str
        ) -> None:
        
        # getting content from message
        
        await inter.response.send_message(content=None, embed=process_embed())

        try: 
            message = await inter.channel.fetch_message(messageid)
        except Exception as e:
            await inter.edit_original_response(content=None, embed=fail_embed(e))
            return


        message_list: list = message.content.split("\n")
        message_list.pop(0)
        message_list.pop()
        
        prompt = "\n".join(message_list)

        # writing
        
        try:
            filepath: str = "/data/latex/" + str(inter.user.id) + ".tex"

            with open(filepath, "w") as file:
                file.write(prompt)
        except Exception as e:
            await inter.edit_original_response(content=None, embed=fail_embed(e))
            return

        await inter.edit_original_response(
            content=None, 
            embed=success_embed("Preamble changed successfully")
        )
        
    @preamble_commands.command(
        name="get",
        description="Let's you see another user's preamble."
    )
    async def get(
            self,
            inter: discord.Interaction,
            user: Optional[discord.User] = None
        ) -> None:
        
        if not user:
            user = inter.user
        
        # get path of file
        path: str = "/data/latex/" + str(user.id) + ".tex"

        # check if it exists
        if not os.path.isfile(path):
            await inter.response.send_message(content=None, embed=fail_embed("No preamble found"))
            return
        
        
        # if there is a preamble
        
        # getting the content
        prompt: list[str] = []
        with open(path, "r") as file:
            prompt = [l.strip() for l in file.readlines()]
            
        content = "```tex\n" + "\n".join(prompt) + "\n```"

        await inter.response.send_message(content=None, embed=success_embed(content))

        
        
        
    

    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Latex(bot))