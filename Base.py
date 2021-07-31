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
	funcs={"w":w,"a":a,"s":s,"d":d}
	args=list(args[0])
	for direction in args:
		try:
			funcs[direction]([])
		except KeyError:
			dprint("{} isnt 'w' 'a' 's' or 'd'".format(direction))
			break
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
	dprint("You cant move there!")

def withBase(dict1):
	return dict(dict1,**baseActions)