import discord
from discord.ext import commands
from discord.ext.commands import Bot

class RpgNode:
	def __init__(self,startAction,actions,errorAction,icons):
		self.startAction=startAction
		self.icon=icons
		self.actions=actions
		self.errorAction=errorAction

	def handleAction(self,actionMessage):
		action=actionMessage.split(" ")
		try:
			self.actions[action[0]] (action[1:])
		except KeyError:
			self.errorAction(action[0],action[1:])

class RpgItem:
	def __init__(self,name,description,fullDurability,durability,useFunc):
		self.name=name
		self.description=description
		self.fullDurability=fullDurability
		self.durability=durability
		self.useFunc=useFunc

	def use(self):
		self.useFunc(self.durability)
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

	def goto(self,player,x,y):
		if x<0 or y<0:
			self.failFunc("OutOfRange")
			return
		try:
			if not self.nodes[y][x]==None:
				player.x=x
				player.y=y
				self.nodes[y][x].startAction()
				return
		except IndexError:
			self.failFunc("OutOfRange")
		self.failFunc("Nothing")

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