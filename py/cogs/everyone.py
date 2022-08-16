import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from random import randint
from pasta import ListsPas
from asyncio import sleep

"""
Ping
Sus  
report
"""


# making a function to handle the errors bc i didnt do that before for some reason
async def handleError(message, error): # im glad this works
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await message.channel.send(msg)

    elif isinstance(error, commands.MissingRequiredArgument):
        rnd = randint(0, len(ListsPas.helpPastas) - 1)
        msg = ListsPas.helpPastas[rnd]
        await message.channel.send(msg)
    
    else:
        print(error)



#--------------------------------------------------------------------------------------------------------------------------
class Everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


#--------------------------------------------------------------------------------------------------------------------------
    # ping
    
    @commands.command(
        case_insensitive=True,
        help="Pings the bot to check if its online",
        brief="Responds with 'pong'",
        )
    @commands.cooldown(1, 5, BucketType.guild)
    async def ping(self, ctx): 
        """ Responds with 'pong' """
        await ctx.channel.send("pong")


    @ping.error
    async def ping_error(self, ctx, error):
        await handleError(ctx, error)
    

#--------------------------------------------------------------------------------------------------------------------------
    #sus

    @commands.command(
        case_insensitive=True,
        help="ඞ",
        brief="ඞ",
        )
    @commands.cooldown(1, 5, BucketType.user)
    async def sus(self, ctx):
        """ Responds with an among us looking character """
        await ctx.message.delete()
        await ctx.channel.send("ඞ") 
    

    @sus.error
    async def sus_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # report

    @commands.command(
        case_insensitive=True,
        help="Use to report people, format like this: Mention the person / Reason", 
        brief="Used to report people."
        )
    @commands.cooldown(1, 20, BucketType.user)
    async def report(self, ctx, userID, *, reason):
        """ Allows any user to report another user """
        reported = userID
        reporter = ctx.author.id
        report = ctx.guild.get_channel(904829118477111366)

        await report.send(f"Reporter: <@!{reporter}> \nReported: {reported} \nReason: {reason}")

        await ctx.message.delete()
        await ctx.channel.send("User has been reported!")

    
    @report.error
    async def report_error(self, ctx, error):
        await handleError(ctx, error)
    
    
#----------------------------------------------------------------------------------------------------------------
    # avatar

    @commands.command(
        case_insensiive=True,
        help="Gets a person's avatar.",
        )
    @commands.cooldown(1, 20, BucketType.user)
    async def avatar(self, ctx, user : discord.Member):
        """ Responds with the avatar of the user mentioned """
        await ctx.channel.send(user.avatar_url)


    @avatar.error
    async def avatar_error(self, ctx, error):
        await handleError(ctx, error)


#----------------------------------------------------------------------------------------------------------------
    # remindme
    # hopefully since the bot is self hosted this shouldn't break as much

    @commands.command(
        help="Reminds you about something after a certain amount of time",
    )
    @commands.cooldown(1, 20, BucketType.user)
    async def remindme(self, ctx, time: str, *, reason="nothing"):
        # m, h, d
        # im going to assume that raising an exception also stops it (and i dont need to add a return)
        if len(time) < 2: raise commands.MissingRequiredArgument

        unt = time[-1]
        try:
            sec = time[:-2]
        except ValueError:
            raise commands.MissingRequiredArgument

        await ctx.channel.send(f"Alright {ctx.author.mention}, I'll remind you about \n'{reason}'")

        if unt == "m":
            sec *= 60
        elif unt == "h":
            sec *= 3600
        elif unt == "d":
            sec *= (3600 * 24)

        await sleep(sec)
        await ctx.channel.send(f"{ctx.author.mention} you wanted to be reminded about \n'{reason}'")

    
    @remindme.error
    async def remindme_error(self, ctx, error):
        await handleError(ctx, error)


#----------------------------------------------------------------------------------------------------------------

#necesseties
def setup(bot):
    bot.add_cog(Everyone(bot))