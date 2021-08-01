'''
Author: Lomnom
Lisence: MIT lisence
Description: Common actions called by every tile
'''
from RpgClass import *

def setInternalVals(aPlayer,aMap,aPrint,aFlush,aStack,aGet,aReact,aGetReact):
	global player,themap,dprint,dflush,dstack,dinput,dreact,dgetreact
	player,themap,dprint,dflush,dstack,dinput,dreact,dgetreact=aPlayer,aMap,aPrint,aFlush,aStack,aGet,aReact,aGetReact

async def pmap(reaction,message):
	dprint(themap.getProjection(player))
	await dflush(message.channel)

async def w(reaction,message):
	await themap.goto(reaction,message,player,player.x,player.y-1)
	dprint(themap.getProjection(player))
	await dflush(message.channel)

async def s(reaction,message):
	await themap.goto(reaction,message,player,player.x,player.y+1)
	dprint(themap.getProjection(player))
	await dflush(message.channel)

async def d(reaction,message):
	await themap.goto(reaction,message,player,player.x+1,player.y)
	dprint(themap.getProjection(player))
	await dflush(message.channel)

async def a(reaction,message):
	await themap.goto(reaction,message,player,player.x-1,player.y)
	dprint(themap.getProjection(player))
	await dflush(message.channel)

async def move(reaction,message):
	args=list(await dinput("enter directions to move in! eg. wwwssddsd",message.channel))
	for direction in args:
		if direction=="w":
			await themap.goto(reaction,message,player,player.x,player.y-1)
		elif direction=="a":
			await themap.goto(reaction,message,player,player.x-1,player.y)
		elif direction=="s":
			await themap.goto(reaction,message,player,player.x,player.y+1)
		elif direction=="d":
			await themap.goto(reaction,message,player,player.x+1,player.y)
		else:
			dprint("{} is not w,a,s or d".format(direction))
	dprint(themap.getProjection(player))
	await dflush(message.channel)


async def use(reaction,message):
	try:
		itemIndex=int(await dinput("enter item index to use! eg. 0",message.channel))
		item=player.items[itemIndex]
	except:
		dprint("item number not valid!")
		await dflush(message.channel)
		return
	await item.use()
	if item.durability<=0:
		dprint(player.items[itemIndex].name+" was used up!")
		player.items.pop(itemIndex)
	dprint(getbackpackstr())
	await dflush(message.channel)

def getbackpackstr():
	backpackStr="Items:\n"
	for item in range(len(player.items)):
		itemObj=player.items[item]
		backpackStr+="    {}: {}   ({}/{})\n".format(item,itemObj.name,itemObj.durability,itemObj.fullDurability)
	return backpackStr
async def backpack(reaction,message):
	dprint(getbackpackstr())
	await dflush(message.channel)

async def drop(reaction,message):
	try:
		itemIndex=int(await dinput("enter item index to drop! eg. 0",message.channel))
		item=player.items[itemIndex]
	except:
		dprint("item number not valid!")
		await dflush(message.channel)
		return
	dprint("dropped {}".format(player.items[itemIndex].name))
	player.items.pop(itemIndex)
	dprint(getbackpackstr())
	await dflush(message.channel)

async def swap(reaction,message):
	try:
		itemIndex=[
			int(await dinput("enter first item index to swap! eg. 0",message.channel)),
			int(await dinput("enter second item index to swap! eg. 1",message.channel))
		]
	except:
		dprint("item numbers not valid!")
		await dflush(message.channel)
		return
	dprint("swapped {} ({}) with {} ({})".format( player.items[itemIndex[0]].name, itemIndex[0], player.items[itemIndex[1]].name, itemIndex[1]))
	item1=player.items[itemIndex[0]]
	player.items[itemIndex[0]]=player.items[itemIndex[1]]
	player.items[itemIndex[1]]=item1
	dprint(getbackpackstr())
	await dflush(message.channel)

async def info(reaction,message):
	try:
		itemIndex=int(await dinput("enter item index to get info on! eg. 0",message.channel))
		item=player.items[itemIndex]
	except:
		dprint("item number not valid!")
		await dflush(message.channel)
		return
	dprint(item.description)
	await dflush(message.channel)

baseActions={"⬆️":w,"⬇️":s,"⬅️":a,"➡️":d,"⏭":move,"🗺":pmap,"🎒":backpack,"⚔️":use,"🗑":drop,"🔁":swap,"❓":info}
# 🍴

async def err(reaction,message,err): #invalid action
	dprint("you cant do {}".format(err))
	await dflush(message.channel)
async def errMov(reaction,message,err): #cant move
	dprint("You cant move there! ({})".format(err))
def withBase(dict1):
	return dict(dict1,**baseActions)

# Actions that happen in the empty space appended with ---E
async def startActionE(reaction,message): 
	dprint("You enter a creepy room, the place around you is devoid of color")
async def lookE(reaction,message):
	dprint("You look around and see rotting bodies")
	await dflush(message.channel)
async def touchE(reaction,message):
	dprint("the rotting body leaves a stench on your hand")
	await dflush(message.channel)

# Actions that happen in the Fruit tile appended with ---F
async def startActionF(reaction,message):
	dprint("You enter a room with suprisingly few dead bodies, and a few degrading crates of bananas")
async def lookF(reaction,message):
	dprint("You look around and see an old stash of bananas")
	await dflush(message.channel)
async def touchF(reaction,message):
	dprint("You touch some bananas, they feel powdery from the mould")
	await dflush(message.channel)
async def smellF(reaction,message):
	dprint("You smell the bananas, they smell suprisingly nice, probably because you had been starving")
	await dflush(message.channel)
async def eatF(reaction,message):
	dprint("You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")
	await dflush(message.channel)
async def takeF(reaction,message):
	dprint("You stash a disgusting banana into your backpack, to sell for barely a few chips at the almost deserted mainland")
	player.items+=[RpgItem("Disgusting Banana","a Wormy, mouldy and slimy banana",1,1,eatBanana)]
	await dflush(message.channel)

async def eatBanana(durability):
	dprint("You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")