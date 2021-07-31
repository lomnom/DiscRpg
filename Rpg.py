import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from time import sleep

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

def err(thing,args):
	# dprint("you cant do that")
	pass
def errMov(err):
	dprint("You cant move there!")

empty=RpgNode(startActionE,withBase({"look":lookE,"touch":touchE}),err,".")
food=RpgNode(startActionF,withBase({"look":lookF,"touch":touchF,"eat":eatF,"smell": smellF,"take":takeF}),err,"F")

themap=RpgMap(
	[
		[empty,empty],
		[None ,empty,empty],
		[None ,None ,empty,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,empty],
		[None ,None ,None ,food ],
	],
	errMov
)

player=RpgPlayer(0,0,[],"O")

setInternalVals(player,themap,dprint)

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

log("started!")

lock=False

@bot.event
async def on_message(message):
	if not (message.author == bot.user): #makesure its not receiving own message 
		themap.node(player).handleAction(message.content)
		global replies
		if not "\n".join(replies)=="":
			try:
				await message.channel.send("\n".join(replies))
			except:
				await message.channel.send("```\ncommand output failed to send!!??\n```")
		replies=[]

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
    
bot.run(open("key.txt","r").read())