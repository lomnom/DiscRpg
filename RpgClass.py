'''
Author: Lomnom
Lisence: MIT lisence
Description: Defines the game internals
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from yaml import load, dump
from os.path import exists
from os import mkdir
import pickle 

def setbot(abot):
	global bot
	bot=abot

def dprint(game,message):  # Discord print
	game.replies+=["```\n"+message+"```"]

async def dflush(game):
	if not "\n".join(game.replies)=="":
		try: # Edits the old message if there is one
			await game.message.edit(content="\n".join(game.replies))
		except: # Sends an error message if reply cannot be sent for example > 6000 chars
			await game.message.edit(content="```\ncommand output failed to send!!??\n```")
	game.replies=[]

async def dinput(game,message):
	message=await game.message.channel.send("```\n"+message+"\n```")
	def check(message):
		return message.channel==game.message.channel and message.author.id==game.user and not message.author == bot.user
	reply= await bot.wait_for('message', check= check)
	contents=reply.content
	await reply.delete()
	await message.delete()
	return contents

#await game.message.add_reaction(emojis[emoji]) 
#game.message.clear_reaction(game.reactions[emoji])

async def dreact(game,emojis):
	global messageReactions
	loop = asyncio.get_event_loop()
	emojis=list(emojis)

	for emoji in range(len(emojis)):
		if len(game.reactions)-1 >= emoji and emojis[emoji] == game.reactions[emoji]:
			continue
		else:
			#delete till equal
			while (not len(game.reactions)-1 <= emoji) and (not emojis[emoji] == game.reactions[emoji]): 
				await game.message.clear_reaction(game.reactions[emoji])
				game.reactions.pop(emoji)
			#if all deleted but no emoji, add emoji
			if len(game.reactions)-1 <= emoji or emojis[emoji] == game.reactions[emoji]:
				await game.message.add_reaction(emojis[emoji]) 
				if len(game.reactions)-1 <= emoji:
					game.reactions+=[emojis[emoji]]
				else:
					game.reactions[emoji]=emojis[emoji]

	if not game.reactions == emojis:
		for n in range( len(game.reactions) - len(emojis) ):
			await game.message.clear_reaction(game.reactions[-1])
			game.reactions.pop(-1)

async def dgetreact(game):
	def check(reaction,user):
		return reaction.message==game.message and user.id==game.user and not (user==bot.user)
	reaction=await bot.wait_for('reaction_add', check= check)
	emoji=str(reaction[0])
	await reaction[0].remove(reaction[1])
	return emoji

class RpgGame:
	def __init__(self,player,maps,map,user,data):
		self.player=player
		self.maps=maps
		self.mapId=map
		self.map=maps[map]
		self.user=user
		self.data=data

	async def setMap(self,mapId):
		self.map=self.maps[mapId]
		self.mapId=mapId

	async def createMessage(self,channel):
		self.reactions=[]
		self.replies=[]
		self.message=await channel.send("```\nRPG hath been summoned! loading...\n```")
		await dreact(self,self.map.node(self.player).actions.keys())
		await self.message.edit(content="```\nRPG hath been summoned! loaded!\n```")

	async def handleAction(self,actionReaction):
		await self.map.node(self.player).handleAction(actionReaction,self)

	async def run(self):
		while True:
			await dreact(self,self.map.node(self.player).actions.keys())
			reaction=await dgetreact(self)
			await self.handleAction(reaction)

class RpgSave:
	def __init__(self,user):
		self.user=user

	def store(self,game):
		self.player=game.player
		self.map=game.mapId
		self.data=game.data
		try:
			mkdir("saves")
		except OSError:
			pass
		filehandler = open("saves/{}.pickle".format(self.user), 'wb') 
		pickle.dump(self,filehandler)

	def load(self,maps):
		try:
			try:
				mkdir("saves")
			except OSError:
				pass
			filehandler = open("saves/{}.pickle".format(self.user), 'rb')
			self=pickle.load(filehandler)
			return RpgGame(self.player,maps,self.map,self.user,self.data)
		except FileNotFoundError:
			raise ValueError

class RpgNode:
	def __init__(self,startAction,actions,errorAction,icons,passable):
		self.passable=passable
		self.startAction=startAction
		self.icon=icons
		self.actions=actions
		self.errorAction=errorAction

	async def handleAction(self,actionReaction,game):
		try:
			await self.actions[str(actionReaction)] (game)
		except KeyError:
			await self.errorAction(game,str(actionReaction))

class RpgItem:
	def __init__(self,name,description,fullDurability,durability,useFunc):
		self.name=name
		self.description=description
		self.fullDurability=fullDurability
		self.durability=durability
		self.useFunc=useFunc

	async def use(self,game):
		await self.useFunc(self.durability,game)
		self.durability-=1

class RpgPlayer:
	def __init__(self,x,y,items,icon):
		self.x=x
		self.y=y
		self.items=items
		self.icon=icon
	def use(self,index):
		items[index].use()
		items[index].durability-=1
		if items[index].durability<=0:
			items.pop(index)
	def hasitem(self,itemName):
		for item in self.items:
			if item.name==itemName:
				return True
		return False
	def hasremoveitem(self,itemName):
		for item in range(len(self.items)):
			if self.items[item].name==itemName:
				self.items.pop(item)
				return True
		return False

class RpgMap:
	def __init__(self,nodes,failFunc):
		self.failFunc=failFunc
		self.nodes=nodes

	async def goto(self,game,x,y):
		if x<0 or y<0:
			await self.failFunc(game,"OutOfRange")
			return
		try:
			if not self.nodes[y][x].passable:
				await self.failFunc(game,"Unpassable")
				return
			if not self.nodes[y][x]==None:
				game.player.x=x
				game.player.y=y
				await self.nodes[y][x].startAction(game)
				return
			else:
				await self.failFunc(game,"Nothing")
		except IndexError:
			await self.failFunc(game,"OutOfRange")

	def getProjection(self,player):
		projection=""
		for row in range(len(self.nodes)):
			projection+="\n"
			for col in range(len(self.nodes[row])):
				try:
					if row==player.y and col==player.x:
						projection+=player.icon
					else:
						projection+=self.nodes[row][col].icon
				except AttributeError:
					projection+=" "
		return projection[1:]

	def node(self,player):
		return self.nodes[player.y][player.x]
