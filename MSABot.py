# MSABOT v0.91 (UNFINISHED)
# TO DO LIST
    # ADD COMMAND FOR LISTING PRAYER TIME (WITH LOCATION)
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


global text
text = " "
global fajr 
fajr = " "
global dhuhr 
dhuhr  = " "
global asr
asr = " "
global maghrib
maghrib  = " "
global isha 
isha = " "
global loc 
loc = ' '
global date 
date = ' '
global city 
city = 'pomona'
global prayerRole
prayerRole = 1019519460849242134
global prayerChannel
prayerChannel = 1020737108018733137

client = commands.Bot(command_prefix='!')
token = authkey.authkey

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #print(f"{message.author.name}: {message.content}")
    await client.process_commands(message)

@client.command(pass_context=True)
async def egg(ctx):
    await ctx.channel.send(f"egg")

@client.command(pass_context=True)
async def prayertimes(ctx): # !prayertimes COMMAND 
    formattedFajrTime = formatTime(fajr)
    formattedDhuhrTime = formatTime(dhuhr)
    formattedAsrTime = formatTime(asr)
    formattedMaghribTime = formatTime(maghrib)
    formattedIshaTime = formatTime(isha)
    await ctx.channel.send(f">>> **Prayer times on {date} in {loc}:** \nFajr: {formattedFajrTime} \nDhuhr: {formattedDhuhrTime} \
        \nAsr: {formattedAsrTime} \nMaghrib: {formattedMaghribTime} \nIsha: {formattedIshaTime}") 

@tasks.loop(hours = 24) # REFRESHING RESPONSE FROM API ONCE A DAY 
async def refreshResponse():    
    response = requests.get(f"https://dailyprayer.abdulrcs.repl.co/api/{city}")
    text = json.loads(response.text)
    global fajr
    global dhuhr
    global asr 
    global maghrib
    global isha
    global loc
    global date
    fajr = text["today"]['Fajr']
    dhuhr = text["today"]['Dhuhr']
    asr = text["today"]['Asr']
    maghrib = text['today']['Maghrib']
    isha = text['today']["Isha'a"]
    date = text['date']
    loc = text['city']

def formatTime(prayerTime): # GENERALIZING THE FORMAT TIME FOR PRAYERS 
    prayerTime = datetime.strptime(prayerTime, "%H:%M").time()
    formattedPrayerTime = prayerTime.strftime("%I:%M %p")
    return formattedPrayerTime

@tasks.loop(seconds = 59)
async def pollTime(): # REFRESHING EVERY MINUTE TO CHECK IF CURRENT TIME IS A PRAYER TIME
    rawTime = datetime.now().time()
    currentFormattedTime = rawTime.strftime("%I:%M %p")
    formattedFajrTime = formatTime(fajr)
    formattedDhuhrTime = formatTime(dhuhr)
    formattedAsrTime = formatTime(asr)
    formattedMaghribTime = formatTime(maghrib)
    formattedIshaTime = formatTime(isha)
    b = time(12, 55, 50)
    formattedB = b.strftime("%I:%M %p")
    #print(formattedB)
    #print(formattedFajrTime)
    #print(formattedDhuhrTime)
    #print(formattedAsrTime)
    #print(formattedMaghribTime)
    #print(formattedIshaTime)
    channel = client.get_channel(prayerChannel)
    if(currentFormattedTime == formattedFajrTime):
        await channel.send("<@&1019519460849242134> It's time to pray FAJR!")
    if(currentFormattedTime == formattedDhuhrTime):
        await channel.send("<@&1019519460849242134> It's time to pray DHUHR!")
    if(currentFormattedTime == formattedAsrTime):
        await channel.send("<@&1019519460849242134> It's time to pray ASR!")
    if(currentFormattedTime == formattedMaghribTime):
        await channel.send("<@&1019519460849242134> It's time to pray MAGHRIB!")
    if(currentFormattedTime == formattedIshaTime):
        await channel.send("<@&1019519460849242134> It's time to pray ISHA!")
    if(currentFormattedTime == formattedB):
        await channel.send("<@&1019519460849242134> It's time to pray test!")
refreshResponse.start() # START REFRESH THREAD
pollTime.start() # START POLLING THREAD 
client.run(token)