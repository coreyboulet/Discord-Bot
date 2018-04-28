import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import os
import re



#import test for the googlespreadsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet=client.open('GroupMeBot').worksheet("discordbot")



TOKEN = os.getenv('BOTTOKEN')

client = discord.Client()

@client.event
async def on_message(message):
  
  	#Put it in lower to be sure caps dont matter
    inmess=message.content.lower()

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #here i split the messages in string so we checked if they are names for raids in the dedicated sheet.
    strings=inmess.split()
    text=""
    for string in strings:
    	try:
    		if sheet.find(string):
    			ref = sheet.find(string)
    			row = ref.row
    			output = sheet.cell(row,2).value
    		text= text + " " + output
    	#this is to avoid the formula to crash when the word is not in the excel list
    	except:
    		pass	
    #Here I'm looking for something that looks like a time xx:xx or x:xx
    searchtime=re.findall(r'\d{1,2}\S\d{1,2}', inmess)
    #I'm takin the first (and probably only time in the list created)
    time=searchtime[0]
    finaltext= " {0.author.mention} announced ".format(message) + text +" at " + time +" who's in ?"
    await client.send_message(client.get_channel('426815579891040258'), finaltext)





        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
