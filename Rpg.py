import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from time import sleep
import asyncio

from Base import *
from RpgClass import *

replies=[]
def dprint(thing):
	global replies
	replies+=["```\n"+thing+"```"]

def startActionE():
	dprint("You enter a creepy room, the place around you is devoid of color")
def lookE(args):
	dprint("You look around and see rotting bodies")
def touchE(args):
	dprint("the rotting body leaves a stench on your hand")

def startActionF():
	dprint("You enter a room with suprisingly few dead bodies, and a few degrading crates of bananas")
def lookF(args):
	dprint("You look around and see an old stash of bananas")
def touchF(args):
	dprint("You touch some bananas, they feel powdery from the mould")
def smellF(args):
	dprint("You smell the bananas, they smell suprisingly nice, probably because you had been starving")
def eatF(args):
	dprint("You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")
def takeF(args):
	dprint("You stash a disgusting banana into your backpack, to sell for barely a few chips at the almost deserted mainland")
	player.items+=[RpgItem("Disgusting Banana","a Wormy, mouldy and slimy banana",1,1,eatF)]

shades=[" ","░","▒","▓","█"]

path=RpgNode(startActionE,withBase({"look":lookE,"touch":touchE}),err,shades[0],True)
pathedge=RpgNode(startActionE,{},err,shades[2],False)
void=RpgNode(startActionE,{},err,shades[4],False)

food=RpgNode(startActionF,withBase({"look":lookF,"touch":touchF,"eat":eatF,"smell": smellF,"take":takeF}),err,"F",True)

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
	errMov
)

player=RpgPlayer(4,0,[],"O")

setInternalVals(player,themap,dprint)

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

log("started!")

channelMessages={}

@bot.event
async def on_message(message):
	loop = asyncio.get_event_loop()
	if (not (message.author == bot.user)) and ((message.channel.name=="rpg") or (message.channel.name=="spammy-or-test-please-mute")):
		themap.node(player).handleAction(message.content)
		global replies
		if not "\n".join(replies)=="":
			try:
				loop.create_task( channelMessages[message.channel].edit(content="\n".join(replies)) )
			except KeyError:
				channelMessages[message.channel]=await message.channel.send("\n".join(replies))
			except:
				loop.create_task(channelMessages[message.channel].edit(content="```\ncommand output failed to send!!??\n```"))
		replies=[]
		loop.create_task(message.delete())

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
    
bot.run(open("key.txt","r").read())