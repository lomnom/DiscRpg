'''
Visuals and textures definition
'''

from Base import *  # Import game functions
from RpgClass import *  # Game engine

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

path=RpgNode(startActionE,withBase({"👀":lookE,"🤚":touchE}),err,shades[0],True)  # to walk on
pathedge=RpgNode(startActionE,{},err,shades[2],False) # a different type of path that cannot walk on, used for shading

void=RpgNode(startActionE,{},err,shades[4],False) # Walls that cannot be walked on

food=RpgNode(startActionF,withBase({"👀":lookF,"🤚":touchF,"🍽":eatF,"👃": smellF,"✋":takeF}),err,"F",True) # Custom tile that is food, and can take bananas

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

shades=[" ","░","▒","▓","█"]