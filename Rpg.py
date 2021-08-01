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

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

setbot(bot)

'''
Visuals and textures definition
'''

shades=[" ","░","▒","▓","█"]

path=RpgNode(startActionE,withBase({"👀":lookE,"🤚":touchE}),err,shades[0],True)  # to walk on
pathedge=RpgNode(startActionE,{},err,shades[2],False) # a different type of path that cannot walk on, used for shading
void=RpgNode(startActionE,{},err,shades[4],False) # Walls that cannot be walked on

food=RpgNode(startActionF,withBase({"👀":lookF,"🤚":touchF,"🍽":eatF,"👃": smellF,"✋":takeF}),err,"F",True) # Custom tile that is food, and can take bananas

themap=RpgMap(
	[
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,path, pathedge, void,void,void],
		[void,void,void,void, path,path,path,food, pathedge, void,void,void],
	],
	errMov # when moved out of bounds
)


'''
Logging starts
'''

log("started!")

games={}

@bot.command(pass_context=True)
async def rpg(ctx):
	try:
		games[ctx.message.author]
		try:
			await games[ctx.message.author].message.delete()
		except:
			log("could not delete old gameWindow")
		await games[ctx.message.author].createMessage(ctx.channel)
	except KeyError:
		games[ctx.message.author]=RpgGame(RpgPlayer(4,0,[],"O"),themap,ctx.message.author)
		await games[ctx.message.author].createMessage(ctx.channel)
		await games[ctx.message.author].run()

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
	
bot.run(open("key.txt","r").read())  # pulls your token from key.txt and runs the bot
