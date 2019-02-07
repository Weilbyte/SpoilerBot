import discord
import asyncio
import sys
import os 
from SQLHandler import *

tokenFile = "token.txt"
prefix = "##"

def getToken():
    if os.path.isfile(tokenFile):
        file = open(tokenFile,"r")
        return file.read()
    else:
        file = open(tokenFile,"w") 
        file.write("REPLACE_WITH_TOKEN")
        file.close()
        exit

spoilerBot = discord.Client()
doDb()

@spoilerBot.event
async def on_message(message):
    if message.content.startswith(prefix + "status"):
        await spoilerBot.send_message(message.channel, gameStatus("get", 0, message.server.id))
    if message.content.startswith(prefix + "wladd"):
        strip = message.content.replace(prefix + "wladd", '')
        if message.author.server_permissions.administrator:    
            await spoilerBot.send_message(message.channel, whiteList("add", strip, message.server.id))
        else:
            await spoilerBot.send_message(message.channel, "Uh-oh! You need to have Administrator permission to use this command!")
    if message.content.startswith(prefix + "wldel"):
        strip = message.content.replace(prefix + "wldel", '')
        if message.author.server_permissions.administrator:    
            await spoilerBot.send_message(message.channel, whiteList("del", strip, message.server.id))
        else:
            await spoilerBot.send_message(message.channel, "Uh-oh! You need to have Administrator permission to use this command!")



spoilerBot.run(getToken())

