'''
Author: Lomnom
Lisence: MIT lisence
Description: Defines the game internals
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot

class RpgNode:
	def __init__(self,startAction,actions,errorAction,icons,passable):
		self.passable=passable
		self.startAction=startAction
		self.icon=icons
		self.actions=actions
		self.errorAction=errorAction

	async def handleAction(self,actionReaction,mapMessage):
		try:
			await self.actions[str(actionReaction)] (actionReaction,mapMessage)
		except KeyError:
			await self.errorAction(actionReaction,mapMessage,actionReaction)

class RpgItem:
	def __init__(self,name,description,fullDurability,durability,useFunc):
		self.name=name
		self.description=description
		self.fullDurability=fullDurability
		self.durability=durability
		self.useFunc=useFunc

	async def use(self):
		await self.useFunc(self.durability)
		self.durability-=1

class RpgPlayer:
	def __init__(self,x,y,items,icon):
		self.x=x
		self.y=y
		self.items=items
		self.icon=icon
	def use(self,index):
		items[index].use()
		if items[index].durability<=0:
			items.pop(index)

class RpgMap:
	def __init__(self,nodes,failFunc):
		self.failFunc=failFunc
		self.nodes=nodes

	async def goto(self,reaction,message,player,x,y):
		if x<0 or y<0:
			await self.failFunc(reaction,message,"OutOfRange")
			return
		try:
			if not self.nodes[y][x].passable:
				await self.failFunc(reaction,message,"Unpassable")
				return
			if not self.nodes[y][x]==None:
				player.x=x
				player.y=y
				await self.nodes[y][x].startAction(reaction,message)
				return
			else:
				await self.failFunc(reaction,message,"Nothing")
		except IndexError:
			await self.failFunc(reaction,message,"OutOfRange")

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
