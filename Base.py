'''
Author: Lomnom
Lisence: MIT lisence
Description: Common actions called by every tile
'''
from RpgClass import *

async def pmap(game):
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

async def w(game):
	await game.map.goto(game,game.player.x,game.player.y-1)
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

async def s(game):
	await game.map.goto(game,game.player.x,game.player.y+1)
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

async def a(game):
	await game.map.goto(game,game.player.x-1,game.player.y)
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

async def d(game):
	await game.map.goto(game,game.player.x+1,game.player.y)
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

async def move(game):
	args=list(await dinput(game,"enter directions to move in! eg. wwwssddsd"))
	for direction in args:
		if direction=="w":
			await game.map.goto(game,game.player.x,game.player.y-1)
		elif direction=="a":
			await game.map.goto(game,game.player.x-1,game.player.y)
		elif direction=="s":
			await game.map.goto(game,game.player.x,game.player.y+1)
		elif direction=="d":
			await game.map.goto(game,game.player.x+1,game.player.y)
		else:
			dprint(game,"{} is not w,a,s or d".format(direction))
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

async def use(game):
	try:
		itemIndex=int(await dinput(game,"enter item index to use! eg. 0"))
		item=game.player.items[itemIndex]
	except:
		dprint(game,"item number not valid!")
		await dflush(game)
		return
	await item.use(game)
	if item.durability<=0:
		dprint(game,game.player.items[itemIndex].name+" was used up!")
		game.player.items.pop(itemIndex)
	dprint(game,getbackpackstr(game))
	await dflush(game)

def getbackpackstr(game):
	backpackStr="Items:\n"
	for item in range(len(game.player.items)):
		itemObj=game.player.items[item]
		backpackStr+="    {}: {}   ({}/{})\n".format(item,itemObj.name,itemObj.durability,itemObj.fullDurability)
	return backpackStr

async def backpack(game):
	dprint(game,getbackpackstr(game))
	await dflush(game)

async def drop(game):
	try:
		itemIndex=int(await dinput(game,"enter item index to drop! eg. 0"))
		item=game.player.items[itemIndex]
	except:
		dprint(game,"item number not valid!")
		await dflush(game)
		return
	dprint(game,"dropped {}".format(game.player.items[itemIndex].name))
	game.player.items.pop(itemIndex)
	dprint(game,getbackpackstr(game))
	await dflush(game)

async def swap(game):
	try:
		itemIndex=[
			int(await dinput(game,"enter first item index to swap! eg. 0")),
			int(await dinput(game,"enter second item index to swap! eg. 1"))
		]
	except:
		dprint(game,"item numbers not valid!")
		await dflush(game)
		return
	dprint(game,"swapped {} ({}) with {} ({})".format( game.player.items[itemIndex[0]].name, itemIndex[0], game.player.items[itemIndex[1]].name, itemIndex[1]))
	item1=game.player.items[itemIndex[0]]
	game.player.items[itemIndex[0]]=game.player.items[itemIndex[1]]
	game.player.items[itemIndex[1]]=item1
	dprint(game,getbackpackstr(game))
	await dflush(game)

async def info(game):
	try:
		itemIndex=int(await dinput(game,"enter item index to get info on! eg. 0"))
		item=game.player.items[itemIndex]
	except:
		dprint(game,"item number not valid!")
		await dflush(game)
		return
	dprint(game,item.description)
	await dflush(game)

baseActions={"⬆️":w,"⬇️":s,"⬅️":a,"➡️":d,"⏭":move,"🗺":pmap,"🎒":backpack,"⚔️":use,"🗑":drop,"🔁":swap,"❓":info}
# 🍴

async def err(game,message): #invalid action
	dprint(game,"you cant do {}".format(message))
	await dflush(game)
async def errMov(game,error): #cant move
	dprint(game,"You cant move there! ({})".format(err))
def withBase(dict1):
	return dict(dict1,**baseActions)