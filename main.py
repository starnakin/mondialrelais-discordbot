import discord
from discord.ext import commands

import asyncio

import cogs

import json_manager
import scraper

import os 
import time
import threading
import json

token=json_manager.get(json_manager.config_file_uri, "token")
prefix=json_manager.get(json_manager.config_file_uri, "prefix")

if token == "":
    print("error token is not defined !")
elif prefix == "":
    print("error prefix is not defined !")
else:
    bot=commands.Bot(command_prefix=prefix, description="Bot of group !")
    
    @bot.event
    async def on_ready():
        print("Bot Started !")

    @bot.command()
    async def load(ctx, name=None):
        if name:
            bot.load_extension(name)
            print(name, "has been loaded")
            await ctx.send(str(name + " has been loaded"))
        
    @bot.command()
    async def unload(ctx, name=None):
        if name:
            bot.unload_extension(name)
            print(name, "has been unloaded")
            await ctx.send(str(name + " has been unloaded"))

    @bot.command()
    async def reload(ctx, name=None):
        if name:
            try:
                bot.reload_extension(name)
                print(name, "has been reloaded")
                await ctx.send(str(name + " has been reloaded"))
            except:
                bot.load_extension(name)
                print(name, "has been loaded")
                await ctx.send(str(name + " has been loaded"))

    for file in ['get', "set"]:
        bot.load_extension('commands.{}'.format(file))
        print(file, "has been loaded")

    async def scan():
        while True:
            await bot.wait_until_ready()
            file=json_manager.curent_file("./json/delivery.json")
            for url in file:
                print("dfssd")
                last_event = list(scraper.get(url).get("events").values())[0]
                if last_event == "Colis livré au destinataire":
                    await bot.get_channel(json_manager.get(json_manager.config_file_uri, "relais_channel_id")).send("formidable ! "+file.get(url).get("name")+"viens d'arriver")
                    dict_without_it=json_manager.curent_file("./json/delivery.json")
                    del dict_without_it[url]
                    a_file = open("./json/delivery.json", "w")
                    json.dump(dict_without_it, a_file, indent = 4)  
                    a_file.close()
                else:
                    if not file.get(url).get("last_event") == last_event:
                        await bot.get_channel(json_manager.get(json_manager.config_file_uri, "relais_channel_id")).send(file.get(url).get("name")+"```\n"+last_event+"```")
                        json_manager.update("./json/delivery.json", url, {"author": file.get(url).get("author"), "name": file.get(url).get("name"), "last_event": last_event})
            await asyncio.sleep(100)

    bot.loop.create_task(scan())
    bot.run(token)
