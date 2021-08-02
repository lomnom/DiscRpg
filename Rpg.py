'''
Author: Lomnom
Lisence: MIT lisence
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime

from Base import *  # Import game functions
from RpgClass import *  # Game engine
from Maps import *

def log(message): #define logging function to prevent repeated code
	logFile=open("log.log",'a')
	currentTime = str(datetime.now().time())
	logFile.write("\n["+currentTime+"] "+message)
	print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

setbot(bot)

'''
Logging starts
'''

log("started!")

games={}

@bot.command(pass_context=True)
async def rpg(ctx):
	if isinstance(ctx.channel, discord.channel.DMChannel):
		await ctx.send("You cant use $rpg in a dm!")
		return
	try:
		games[ctx.message.author.id]
		try:
			await games[ctx.message.author.id].message.delete()
		except:
			log("could not delete old gamewindow")
		await ctx.message.delete()
		await games[ctx.message.author.id].createMessage(ctx.channel)
	except KeyError:
		try:
			games[ctx.message.author.id]=RpgSave(ctx.message.author.id).load(levels)
			await games[ctx.message.author.id].createMessage(ctx.channel)
		except ValueError:
			games[ctx.message.author.id]=RpgGame(RpgPlayer(4,0,[],"O"),levels,0,ctx.message.author.id)
			await ctx.message.delete()
			await games[ctx.message.author.id].createMessage(ctx.channel)
		await games[ctx.message.author.id].run()

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
	
bot.run(open("key.txt","r").read())  # pulls your token from key.txt and runs the bot

log("saving games...")
for game in games:
	RpgSave(games[game].user).store(games[game])
log("saved!")