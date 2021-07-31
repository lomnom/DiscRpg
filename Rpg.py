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

from Base import *  # Import simple game functions
from RpgClass import *  # Game engine

replies=[]  # Queue of replies to send back to user
def dprint(message):  # Discord print
	global replies
	replies+=["```\n"+message+"```"]

# Actions that happen in the empty space appended with ---E
def startActionE(): 
	dprint("You enter a creepy room, the place around you is devoid of color")
def lookE():
	dprint("You look around and see rotting bodies")
def touchE():
	dprint("the rotting body leaves a stench on your hand")

# Actions that happen in the Fruit tile appended with ---F
def startActionF():
	dprint("You enter a room with suprisingly few dead bodies, and a few degrading crates of bananas")
def lookF():
	dprint("You look around and see an old stash of bananas")
def touchF():
	dprint("You touch some bananas, they feel powdery from the mould")
def smellF():
	dprint("You smell the bananas, they smell suprisingly nice, probably because you had been starving")
def eatF():
	dprint("You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")
def takeF():
	dprint("You stash a disgusting banana into your backpack, to sell for barely a few chips at the almost deserted mainland")
	player.items+=[RpgItem("Disgusting Banana","a Wormy, mouldy and slimy banana",1,1,eatF)]

	
'''
Visuals and textures definition
'''

shades=[" ","░","▒","▓","█"]

path=RpgNode(startActionE,withBase({"look":lookE,"touch":touchE}),err,shades[0],True)  # to walk on
pathedge=RpgNode(startActionE,{},err,shades[2],False) # a different type of path that cannot walk on, used for shading
void=RpgNode(startActionE,{},err,shades[4],False) # Walls that cannot be walked on

food=RpgNode(startActionF,withBase({"look":lookF,"touch":touchF,"eat":eatF,"smell": smellF,"take":takeF}),err,"F",True) # Custom tile that is food, and can take bananas

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

setInternalVals(player,themap,dprint) # to synchronise

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

'''
Logging starts
'''

log("started!")

channelMessages={}

@bot.event
async def on_message(message):
	loop = asyncio.get_event_loop()
	if (not (message.author == bot.user)) and ((message.channel.name=="rpg") or (message.channel.name=="spammy-or-test-please-mute")):  # define custom channels to read from
		themap.node(player).handleAction(message.content)
		global replies
		if not "\n".join(replies)=="":
			try: # Edits the old message if there is one
				loop.create_task(channelMessages[message.channel].edit(content="\n".join(replies)))
			except KeyError: # Create a new message if it does not exist
				channelMessages[message.channel]=await message.channel.send("\n".join(replies))
			except: # Sends an error message if reply cannot be sent for example > 6000 chars
				loop.create_task(channelMessages[message.channel].edit(content="```\ncommand output failed to send!!??\n```"))
		replies=[]
		loop.create_task(message.delete()) # delete user commands

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
	
bot.run(open("key.txt","r").read())  # pulls your token from key.txt and runs the bot
