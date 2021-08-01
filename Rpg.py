'''
Author: Lomnom
Lisence: MIT lisence
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from time import sleep
import asyncio

from Base import *  # Import game functions
from RpgClass import *  # Game engine

replies=[]  # Queue of replies to send back to user
def dprint(message):  # Discord print
	global replies
	replies+=["```\n"+message+"```"]
async def dflush(channel):
	global replies
	if not "\n".join(replies)=="":
		try: # Edits the old message if there is one
			await channelMessages[channel].edit(content="\n".join(replies))
		except KeyError: # Create a new message if it does not exist
			channelMessages[channel]=await channel.send("\n".join(replies))
			messageReactions[channelMessages[channel]]=[]
		except: # Sends an error message if reply cannot be sent for example > 6000 chars
			await channelMessages[channel].edit(content="```\ncommand output failed to send!!??\n```")
	replies=[]

async def dinput(message,channel):
	message=await channel.send("```\n"+message+"\n```")
	def check(message):
		return message.channel==channel and not message.author == bot.user
	reply= await bot.wait_for('message', check= check)
	contents=reply.content
	await reply.delete()
	await message.delete()
	return contents

async def dreactOne(channel,emoji):
	if not emoji in messageReactions[channelMessages[channel]]:
		messageReactions[channelMessages[channel]]+=[emoji]
		try:
			await channelMessages[channel].add_reaction(emoji)
		except:
			log("unknown emoji {} encountered at {} {}".format(emoji,player.x,player.y))
async def dreact(channel,emojis):
	global messageReactions
	loop = asyncio.get_event_loop()
	tasks=[]
	for emoji in emojis:
		tasks+=[loop.create_task(dreactOne(channel,emoji))]
	for emoji in messageReactions[channelMessages[channel]]: #remove other emojis
		if not emoji in emojis:
			tasks+=[loop.create_task( channelMessages[channel].remove_reaction(emoji,bot.user) )]
	for task in tasks:
		await task
	messageReactions[channelMessages[channel]]=list(emojis)

async def dgetreact(channel):
	def check(reaction,user):
		try:
			return reaction.message==channelMessages[reaction.message.channel] and not (user==bot.user)
		except:
			return False
	reaction= await bot.wait_for('reaction_add', check= check)
	emoji=str(reaction[0])
	await reaction[0].remove(reaction[1])
	return emoji
	
'''
Visuals and textures definition
'''

shades=[" ","░","▒","▓","█"]

path=RpgNode(startActionE,withBase({"👀":lookE,"🤚":touchE}),err,shades[0],True)  # to walk on
pathedge=RpgNode(startActionE,{},err,shades[2],False) # a different type of path that cannot walk on, used for shading
void=RpgNode(startActionE,{},err,shades[4],False) # Walls that cannot be walked on

food=RpgNode(startActionF,withBase({"👀":lookF,"🤚":touchF,"🍽":eatF,"👃": smellF,"✋":takeF}),err,"F",True) # Custom tile that is food, and can take bananas

# current map definition
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

player=RpgPlayer(4,0,[],"O") # defines the starting position, texture and items: see other file

setInternalVals(player,themap,dprint,dflush,replies,dinput,dreact,dgetreact)

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

'''
Logging starts
'''

log("started!")

channelMessages={}
messageReactions={}

@bot.command(pass_context=True)
async def rpg(ctx):
	dprint("RPG hath been summoned! loading...")
	await dflush(ctx.channel)
	await dreact(ctx.channel,themap.node(player).actions.keys())
	dprint("RPG hath been summoned! loaded!")
	await dflush(ctx.channel)
	while True:
		await dreact(ctx.channel,themap.node(player).actions.keys())
		reaction=await dgetreact(ctx.channel)
		await themap.node(player).handleAction(reaction,channelMessages[ctx.channel])

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
	
bot.run(open("key.txt","r").read())  # pulls your token from key.txt and runs the bot
