import discord
import asyncio
import sys
import os 
import random
import string
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


def hasNumbers(inputString):   
    return any(char.isdigit() for char in inputString)

def generateString(length):
    output = ""
    answer = ""
    for i in range(0, length):
        thingToAppend = random.choice(string.ascii_letters)
        if random.random() < 0.05:
            thingToAppend = random.randint(0,9)
            answer = answer + str(thingToAppend)
        output = str(output) + str(thingToAppend)
    return "" + output + "/" + answer
    
def getSpoilers(length):
    satisfied = False
    output = "UNDEFINED"
    soutput = ""
    answer = "UNDEFINED"
    while satisfied == False:
        output = generateString(length)
        if hasNumbers(output):
            satisfied = True
            output,answer = output.split("/")
            print("ANS " + answer)
    for c in output:
        soutput = soutput + "||" + c + "||"
    return "" + soutput + "/" + answer;

spoilerBot = discord.Client()
doDb()

@spoilerBot.event
async def on_message(message):
    if message.content.startswith(prefix + "status"):
        await spoilerBot.send_message(message.channel, gameStatus("get", 0, message.server.id))
    if message.content.startswith(prefix + "wladd"):
        strip = message.content.replace(prefix + "wladd ", '')
        if message.author.server_permissions.administrator:    
            await spoilerBot.send_message(message.channel, whiteList("add", strip, message.server.id))
        else:
            await spoilerBot.send_message(message.channel, "Uh-oh! You need to have Administrator permission to use this command!")
    if message.content.startswith(prefix + "wldel"):
        strip = message.content.replace(prefix + "wldel ", '')
        if message.author.server_permissions.administrator:    
            await spoilerBot.send_message(message.channel, whiteList("del", strip, message.server.id))
        else:
            await spoilerBot.send_message(message.channel, "Uh-oh! You need to have Administrator permission to use this command!")
    if message.content.startswith(prefix + "answer"):
        strip = message.content.replace(prefix + "answer ", '')
        if gameStatus("get", 0, message.server.id) == "There is a spoiler game being currently held!":
            if gameAnswer("get", 0, message.server.id) == strip:
                await spoilerBot.send_message(message.channel, "Game ended. Winner is " + message.author.name)
                await spoilerBot.add_reaction(message, '✅')
                gameStatus("set", 0, message.server.id) 
            else:
                await spoilerBot.add_reaction(message, '❌')
        else:
            await spoilerBot.add_reaction(message, '❓')

    if message.content.startswith(prefix + "make"):
        strip = message.content.replace(prefix + "make ", '')
        allowRun = False
        if message.author.server_permissions.administrator:
            allowRun = True
        if (whiteList("get", message.author.id, message.server.id) == "yeet"):
            allowRun = True
        if allowRun:
            if strip.isdigit():
                if int(strip) > 0 and int(strip) < 401:

                    if gameStatus("get", 0, message.server.id) == "No spoiler game is currently being held :(":
                        output,answer = getSpoilers(int(strip)).split("/")
                        await spoilerBot.send_message(message.channel, output)
                        await spoilerBot.send_message(message.author, "The answer is " + answer)
                        gameStatus("set", 1, message.server.id) 
                        gameAnswer("set", answer, message.server.id)
                    else:
                        await spoilerBot.send_message(message.channel, "The game is already in progress!")       
                else:
                    await spoilerBot.send_message(message.channel, "The digit needs to be between 1-400, you uncultured swine.")
            else:
                await spoilerBot.send_message(message.channel, "Uh-oh! Parameter needs to be a digit from 1 to 400!")
        else:
            await spoilerBot.send_message(message.channel, "Uh-oh! You need to have Administrator permission to use this command!")



spoilerBot.run(getToken())

