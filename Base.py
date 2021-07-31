def setInternalVals(aPlayer,aMap,aprint):
	global player,themap,dprint
	player,themap,dprint=aPlayer,aMap,aprint

def pmap(args):
	dprint(themap.getProjection(player))
def w(args):
	themap.goto(player,player.x,player.y-1)
	pmap([])
def s(args):
	themap.goto(player,player.x,player.y+1)
	pmap([])
def d(args):
	themap.goto(player,player.x+1,player.y)
	pmap([])
def a(args):
	themap.goto(player,player.x-1,player.y)
	pmap([])
def move(args):
	args=list(args[0])
	for direction in args:
		if direction=="w":
			themap.goto(player,player.x,player.y-1)
		elif direction=="a":
			themap.goto(player,player.x-1,player.y)
		elif direction=="s":
			themap.goto(player,player.x,player.y+1)
		elif direction=="d":
			themap.goto(player,player.x+1,player.y)
		else:
			dprint("{} is not w,a,s or d".format(direction))
	pmap([])

def actions(args):
	string="available actions: "
	for aAction in themap.node(player).actions:
		string+=aAction+", "
	dprint(string[:-2])
def use(args):
	try:
		itemIndex=int(args[0])
		item=player.items[itemIndex]
	except:
		dprint("item number not valid!")
		return
	item.use()
	if item.durability<=0:
		dprint(player.items[itemIndex].name+" was used up!")
		player.items.pop(itemIndex)
	backpack([])
def backpack(args):
	backpackStr="Items:\n"
	for item in range(len(player.items)):
		itemObj=player.items[item]
		backpackStr+="    {}: {}   ({}/{})\n".format(item,itemObj.name,itemObj.durability,itemObj.fullDurability)
	dprint(backpackStr)
def drop(args):
	try:
		itemIndex=int(args[0])
		item=player.items[itemIndex]
	except:
		dprint("item number not valid!")
		return
	dprint("dropped {}".format(player.items[itemIndex].name))
	player.items.pop(itemIndex)
	backpack([])
def swap(args):
	try:
		itemIndex=[int(args[0]),int(args[1])]
	except:
		dprint("item numbers not valid!")
		return
	dprint("swapped {} ({}) with {} ({})".format( player.items[itemIndex[0]].name, itemIndex[0], player.items[itemIndex[1]].name, itemIndex[1]))
	item1=player.items[itemIndex[0]]
	player.items[itemIndex[0]]=player.items[itemIndex[1]]
	player.items[itemIndex[1]]=item1
	backpack([])
def info(args):
	try:
		itemIndex=int(args[0])
		item=player.items[itemIndex]
	except:
		dprint("item number not valid!")
		return
	dprint(item.name+":\n"+item.description)

baseActions={"w":w,"a":a,"s":s,"d":d,"move":move,"map":pmap,"actions":actions,"backpack":backpack,"use":use,"drop":drop,"swap":swap,"info":info}

def err(thing,args):
	# dprint("you cant do that")
	pass
def errMov(err):
	dprint("You cant move there! ({})".format(err))

def withBase(dict1):
	return dict(dict1,**baseActions)