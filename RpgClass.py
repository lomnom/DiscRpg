import discord
from discord.ext import commands
from discord.ext.commands import Bot

class RpgIcon:
	def __init__(self,onIcon,offIcon):
		self.onIcon=onIcon
		self.offIcon=offIcon

class RpgNode:
	def __init__(self,startAction,actions,errorAction,icons):
		self.icon=icon
		self.actions=actions
		self.errorAction=errorAction
		startAction()

	def handleAction(self,actionMessage):
		action=actionMessage.split(" ")
		try:
			self.actions[action[0]] (action[1:])
		except KeyError:
			self.errorAction(action,action[1:])

class RpgMap:
	def __init__(self,nodes,x,y):
		self.nodes=nodes
		self.x=x
		self.y=y

	def goto(self,x,y,failFunc):
		if not nodes[y][x]==none:
			self.x=x
			self.y=y
			return
		failFunc()

	def getProjection(self):
		projection=[]
		

def startAction():
	print("You enter a creepy room, the place around you is devoid of color")

def look(args):
	print("You look around and see rotting bodies")

def touch(args):
	print("the rotting body leaves a stench on your hand")

def err(thing,args):
	print("you cant do that")

node=\
RpgNode(
	startAction,
	{
		"look":look,
		"touch":touch
	},
	err
)

while True:
	try:
		node.handleAction(input("> "))
	except KeyboardInterrupt:
		break