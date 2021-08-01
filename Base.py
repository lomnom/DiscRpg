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

async def err(game,error): #invalid action
	dprint(game,"you cant do {}".format(error))
	await dflush(game)
async def errMov(game,error): #cant move
	dprint(game,"You cant move there! ({})".format(err))
def withBase(dict1):
	return dict(dict1,**baseActions)

# Actions that happen in the empty space appended with ---E
async def startActionE(game): 
	dprint(game,"You enter a creepy room, the place around you is devoid of color")
async def lookE(game):
	dprint(game,"You look around and see rotting bodies")
	await dflush(game)
async def touchE(game):
	dprint(game,"the rotting body leaves a stench on your hand")
	await dflush(game)

# Actions that happen in the Fruit tile appended with ---F
async def startActionF(game):
	dprint(game,"You enter a room with suprisingly few dead bodies, and a few degrading crates of bananas")
async def lookF(game):
	dprint(game,"You look around and see an old stash of bananas")
	await dflush(game)
async def touchF(game):
	dprint(game,"You touch some bananas, they feel powdery from the mould")
	await dflush(game)
async def smellF(game):
	dprint(game,"You smell the bananas, they smell suprisingly nice, probably because you had been starving")
	await dflush(game)
async def eatF(game):
	dprint(game,"You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")
	await dflush(game)
async def takeF(game):
	dprint(game,"You stash a disgusting banana into your backpack, to sell for barely a few chips at the almost deserted mainland")
	game.player.items+=[RpgItem("Disgusting Banana","a Wormy, mouldy and slimy banana",1,1,eatBanana)]
	await dflush(game)

async def eatBanana(durability,game):
	dprint(game,"You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")