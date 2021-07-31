import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from RpgClass import *

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

log("started!")

@bot.event
async def on_message(message):
	if not (message.author == bot.user): #makesure its not receiving own message 
		ctx = await bot.get_context(message)
		await ctx.send("testMessage")

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
    
bot.run('ODQwNzkzOTkyMDUxNjg3NDQ1.YJdYbA.QcOXmCygMH8xSgBg6BJyUe3B1WM')