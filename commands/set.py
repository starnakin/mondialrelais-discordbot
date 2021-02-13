import discord
from discord.ext import commands

import uuid
import json

import scraper
import json_manager

def setup(bot):
    bot.add_cog(Set(bot))

class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set(self, ctx, arg1, arg2=None):
        if arg2==None:
            pass

        json_manager.update("./json/delivery.json", ctx.author.id, {arg1: list(scraper.get(arg1).get("events").values())[0]})
