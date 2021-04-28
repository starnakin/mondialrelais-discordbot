import discord
from discord.ext import commands
import asyncio

import uuid
import json

import json_manager
import scraper

def setup(bot):
    bot.add_cog(Set(bot))

class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set(self, ctx, arg0, arg1):
        url = (arg0, arg1)[arg1.find("mondialrelay.fr/suivi-de-colis/?NumeroExpedition=")>=0]
        await ctx.send(url)