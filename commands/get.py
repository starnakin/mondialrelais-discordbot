import discord
from discord.ext import commands
import asyncio


import uuid

import scraper
import json_manager

def setup(bot):
    bot.add_cog(Get(bot))

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get(self, ctx, *args):
        url=""
        name=""
        for i in args:
            if i.find("mondialrelay.fr/suivi-de-colis/?NumeroExpedition=")>=0:
                url = i
            else: 
                name+=i+" "
        if url == "":
            await ctx.send("url invalide")
            return False
        result=scraper.get(url)
        last_event=""
        text="\n```"
        for i in range(len(result.get("events"))):
            text+=list(result.get("events"))[i]+"  "+list(result.get("events").values())[i]+"\n"
            last_event=list(result.get("events").values())[i]
        text+="```"
        await ctx.send(("votre colis est arrivé", "votre colis n'est pas arrivé")[not result.get("delivered")] + text)
        json_manager.update("./json/delivery.json", url, {"author": ctx.message.author.id, "name": name, "last_event": last_event})