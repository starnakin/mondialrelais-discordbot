import discord
from discord.ext import commands

import uuid

import json_manager
import scraper

def setup(bot):
    bot.add_cog(Get(bot))

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get(self, ctx, arg1):
        result=scraper.get(arg1)
        text="\n```"
        for i in range(len(result.get("events"))):
            text+=list(result.get("events"))[i]+"  "+list(result.get("events").values())[i]+"\n"
        text+="```"
        await ctx.send(("votre colis est arrivé", "votre colis n'est pas arrivé")[not result.get("delivered")] + text)