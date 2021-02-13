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

class MonThread (threading.Thread):
    def __init__(self, bot):      # jusqua = donnée supplémentaire
        threading.Thread.__init__(self)  # ne pas oublier cette ligne
        # (appel au constructeur de la classe mère)
        self.bot = bot           # donnée supplémentaire ajoutée à la classe

    async def run(self):
        while True:
            try:
                a_file = open("./json/delivery.json", "r")
                json_object = json.load(a_file)
                for id in list(json_object):
                    for link in list(json_object.get(id)):
                        events=scraper.get(link).get("events")
                        if events.get(list(events)[0]) != json_object.get(id).get(link):
                            json_manager.update("./json/delivery.json", id, {link: list(events.values())[0]})
                            await self.bot.send_message(bot.get_user(id),list(events.values())[0])
            except:
                pass

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
        #m = MonThread(bot) 
        for i in ["280098063643705345"]:
            print(bot.get_guild("809141687979999252"))#json_manager.get("./json/config.json", "guild_id")))#.get_member(i))
            if i.id == "280098063643705345":
                print(i)
                await i.create_dm()
                await i.dm_channel.send("ss")

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

    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            bot.load_extension(f'commands.{file[:-3]}')
            print(file, "has been loaded")

    bot.run(token)