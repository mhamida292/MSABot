# MSABOT v0.9 (UNFINISHED)
# IDEAS FOR IMPROVEMENT 
    # ADD COMMAND FOR LISTING PRAYER TIME 
    # FIX EXPECTED BUGS TO COME WITH REFRESH PERIOD 
    # ADD INTERESTING COMMANDS THAT COULD BE BENEFICIAL FOR USERS 
    # HOST ON SERVER FOR MAX UP TIME
import discord
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from datetime import time 
import requests
import asyncio
import json
import random
import authkey

global fajr 
fajr = " "
global dhuhr 
dhuhr  = " "
global asr
asr = " "
global maghrib
maghrib  = " "
global isha 
isha = " d"

client = commands.Bot(command_prefix='!')
token = authkey.authkey

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"{message.author.name}: {message.content}")
    await client.process_commands(message)

@client.command(pass_context=True)
async def egg(ctx):
    await ctx.channel.send(f"egg")

@tasks.loop(hours = 24) # REFRESHING RESPONSE FROM API ONCE A DAY 
async def refreshResponse():    
    response = requests.get(f"https://dailyprayer.abdulrcs.repl.co/api/pomona")
    text = json.loads(response.text)
    global fajr
    global dhuhr
    global asr 
    global maghrib
    global isha
    fajr = text["today"]['Fajr']
    dhuhr = text["today"]['Dhuhr']
    asr = text["today"]['Asr']
    maghrib = text['today']['Maghrib']
    isha = text['today']["Isha'a"]

@tasks.loop(seconds = 45)
async def pollChecking():
    rawTime = datetime.now().time()
    currentFormattedTime = rawTime.strftime("%I:%M %p")
    print(currentFormattedTime)

    fajrTime = datetime.strptime(fajr, "%H:%M").time()
    formattedFajrTime = fajrTime.strftime("%I:%M %p")

    dhuhrTime = datetime.strptime(dhuhr, "%H:%M").time()
    formattedDhuhrTime = dhuhrTime.strftime("%I:%M %p")

    asrTime = datetime.strptime(asr, "%H:%M").time()
    formattedAsrTime = asrTime.strftime("%I:%M %p")

    maghribTime = datetime.strptime(maghrib, "%H:%M").time()
    formattedMaghribTime = maghribTime.strftime("%I:%M %p")

    ishaTime = datetime.strptime(isha, "%H:%M").time()
    formattedIshaTime = ishaTime.strftime("%I:%M %p")

    b = time(1, 27, 50)
    formattedB = b.strftime("%I:%M %p")

    print(formattedB)
    print(formattedFajrTime)
    print(formattedDhuhrTime)
    print(formattedAsrTime)
    print(formattedMaghribTime)
    print(formattedIshaTime)
    channel = client.get_channel(1019519404926578728)
    if(currentFormattedTime == formattedFajrTime):
        await channel.send("ITS FAJR TIME")
    if(currentFormattedTime == formattedDhuhrTime):
        await channel.send("ITS DHUHR TIME")
    if(currentFormattedTime == formattedAsrTime):
        await channel.send("ITS ASR TIME")
    if(currentFormattedTime == formattedMaghribTime):
        await channel.send("ITS MAGHRIB TIME")
    if(currentFormattedTime == formattedIshaTime):
        await channel.send("ITS ISHA TIME")
    if(currentFormattedTime == formattedB):
        await channel.send("<@1019519460849242134> It's time to pray!")
        pinged = 1 

refreshResponse.start()
pollChecking.start() 
client.run(token)