# MSABOT v0.94
# TO DO LIST
    # Make refresh system more efficient 
    # Quran and Duas? 
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

global prayerChannel
prayerChannel = 1019028813390303273

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
async def joe(ctx):
    await ctx.channel.send(f"mama")

@client.command(pass_context=True)
async def prayertimes(ctx, loc = "pomona"): # !prayertimes COMMAND 
    response = requests.get(f"https://dailyprayer.abdulrcs.repl.co/api/{loc}")
    text = json.loads(response.text)
    fajr = text["today"]['Fajr']
    dhuhr = text["today"]['Dhuhr']
    asr = text["today"]['Asr']
    maghrib = text['today']['Maghrib']
    isha = text['today']["Isha'a"]
    date = text['date']
    loc = text['city']
    formattedFajrTime = formatTime(fajr)
    formattedDhuhrTime = formatTime(dhuhr)
    formattedAsrTime = formatTime(asr)
    formattedMaghribTime = formatTime(maghrib)
    formattedIshaTime = formatTime(isha)
    await ctx.channel.send(f">>> **Prayer times on {date} in {loc}:** \nFajr: {formattedFajrTime} \nDhuhr: {formattedDhuhrTime} \nAsr: {formattedAsrTime} \nMaghrib: {formattedMaghribTime} \nIsha: {formattedIshaTime}") 

@tasks.loop(hours = 4) # REFRESHING RESPONSE FROM API ONCE A DAY 
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
    #b = time(16, 34, 50)
    #formattedB = b.strftime("%I:%M %p")
    channel = client.get_channel(prayerChannel)
    if(currentFormattedTime == formattedFajrTime):
        await channel.send("<@&1019221959260778546> Rise and shine! It’s time to pray Fajr. Have a blessed day inShaaAllah!")
    if(currentFormattedTime == formattedDhuhrTime):
        await channel.send("<@&1019221959260778546> It’s Dhur time! Time to strengthen your imaan and get closer to Allah!")
    if(currentFormattedTime == formattedAsrTime):
        await channel.send("<@&1019221959260778546> It’s Asr time! Take a break from what you're doing and make sure your pray!!")
    if(currentFormattedTime == formattedMaghribTime):
        await channel.send("<@&1019221959260778546> It’s Maghrib time! It’s also better to pray in congregation. So pray together with your brothers/sisters!")
    if(currentFormattedTime == formattedIshaTime):
        await channel.send("<@&1019221959260778546> Make sure you pray Isha before you head to bed. Hope you all had a great day!")

refreshResponse.start() # START REFRESH THREAD
pollTime.start() # START POLLING THREAD 

client.run(token)