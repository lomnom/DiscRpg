'''
Visuals and textures definition
'''
from Base import *  # Import game functions
from RpgClass import *  # Game engine

async def eatBanana(durability,game):
	dprint(game,"You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")
dBanana=RpgItem("Disgusting Banana","a Wormy, mouldy and slimy banana",1,1,eatBanana)

async def save(durability,game):
	await game.setMap(game.mapId+1)
	dprint(game,"You use the Move Token, and feel a woosh of air and a bang as a portal majically appears")
moveToken=RpgItem("Move Token","Summon a portal!",1,1,save)

shades=[" ","░","▒","▓","█"]

# Actions that happen in the empty space appended with ---E
async def startActionE(game): 
	pass
async def lookE(game):
	dprint(game,"A thick layer of dust covers every square inch of the floor and ceiling, as if the compound had been deserted.")
	await dflush(game)
async def touchE(game):
	dprint(game,"Your hands turn black with soot from touching the floor (why did you do that?)")
	await dflush(game)
path=RpgNode(startActionE,withBase({"👀":lookE,"🤚":touchE}),err,shades[0],True)  # to walk on

pathedge=RpgNode(startActionE,{},err,shades[2],False) # a different type of path that cannot walk on, used for shading
void=RpgNode(startActionE,{},err,shades[4],False) # Walls that cannot be walked on

# Actions that happen in the Fruit tile appended with ---F
async def startActionF(game):
	dprint(game,"A few old, degrading crates of bananas")
async def lookF(game):
	dprint(game,"You look around and see an old stash of bananas, with 'breakfast, lunch, dinner' childishly scribbled onto the disty crates.")
	await dflush(game)
async def touchF(game):
	dprint(game,"You touch some bananas, they feel powdery from the mould and dust that collected on them for god knows how long")
	await dflush(game)
async def smellF(game):
	dprint(game,"You smell the bananas, they smell suprisingly nice, probably because you had been starving")
	await dflush(game)
async def eatF(game):
	dprint(game,"You take a bite from the banana, recoiling in disgust as tens of worms wiggle from the exposed banana meat")
	await dflush(game)
async def takeF(game):
	dprint(game,"You stash a disgusting banana into your backpack, to sell for barely a few chips at the almost deserted mainland")
	game.player.items+=[dBanana]
	await dflush(game)
food=RpgNode(startActionF,withBase({"👀":lookF,"🤚":touchF,"🍽":eatF,"👃": smellF,"✋":takeF}),err,"F",True) # Custom tile that is food, and can take bananas

def portal(text,number,x,y):
	async def startActionP(game):
		dprint(game,"You go into a room with a big noisy portal, with the barely legible text '{}' written in cracking ancient paint".format(text))
	async def lookP(game):
		dprint(game,"You look around, seeing the barely legible text '{}' written in cracking ancient paint".format(text))
	async def touchP(game):
		dprint(game,"You touch the portal out of curiosity, the portal pulling on your hand with a overwhelming force, causing you to trip into the mouth of the portal and be transported to another room.")
		await game.setMap(number)
		game.player.x=x
		game.player.y=y
		dprint(game,game.map.getProjection(game.player))
		await dflush(game)
	return RpgNode(startActionP,withBase({"👀":lookP,"🤚":touchP}),err,"@",True)

async def startActionM(game):
	dprint(game,"You see a depressed old man with 2 children sitting on the floor.")
	await dflush(game)
	if not game.data["takenMoveToken"]:
		if (await dinput(game,"Talk to the old man? yes/no")).lower()=="yes":
			if (await dinput(game,"The old man gratefully shakes your hand, and offers a move token for a disgusting banana\nAccept the deal? yes/no")).lower()=="yes":
				dprint(game,"You accept the deal.")
				if game.player.hasremoveitem("Disgusting Banana"):
					game.player.items+=[moveToken]
					game.data["takenMoveToken"]=True
					dprint(game,"Received Move Token!")
				else:
					dprint(game,"You do not have enough Disgusting Bananas!")
			else:
				dprint(game,"You refuse the deal and walk away.")
		else:
			dprint(game,"You ignore the old man, and the man looks at you desparingly.\nYou also realise that he is holding a shiny item.")
async def lookM(game):
	dprint(game,"You look around, and you see an old man and 2 children sitting on the floor")
	await dflush(game)
async def touchM(game):
	dprint(game,"You touch the almost motionless child, his protruding bones jabbing into your hand. \nThe child weakly turns and looks at you hopelessly")
	await dflush(game)
oldMan=RpgNode(startActionM,withBase({"👀":lookM,"🤚":touchM}),err,"&",True)