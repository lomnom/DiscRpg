'''
Author: Lomnom
Lisence: MIT lisence
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime

from Base import *  # Import game functions
from RpgClass import *  # Game engine
from Maps import *

def log(message): #define logging function to prevent repeated code
	logFile=open("log.log",'a')
	currentTime = str(datetime.now().time())
	logFile.write("\n["+currentTime+"] "+message)
	print("["+currentTime+"] "+message)

bot = commands.Bot(command_prefix='$')

'''
Logging starts
'''

log("started!")

games={}
data={
	"takenMoveToken":False
}

setbot(bot)
setGames(games)

@bot.command(pass_context=True)
async def rpg(ctx):
	if isinstance(ctx.channel, discord.channel.DMChannel):
		await ctx.send("You cant use $rpg in a dm!")
		return
	try:
		games[ctx.message.author.id]
		try:
			await games[ctx.message.author.id].message.delete()
		except:
			log("could not delete old gamewindow")

		await ctx.message.delete()
		await games[ctx.message.author.id].createMessage(ctx.channel)
	except KeyError:
		try:
			games[ctx.message.author.id]=RpgSave(ctx.message.author.id).load(levels)
			await ctx.message.delete()
			await games[ctx.message.author.id].createMessage(ctx.channel)
		except ValueError:
			games[ctx.message.author.id]=RpgGame(RpgPlayer(4,0,[],"O"),levels,0,ctx.message.author.id,data.copy())
			await ctx.message.delete()
			await games[ctx.message.author.id].createMessage(ctx.channel)

		await games[ctx.message.author.id].run()

async def load(args):
	try:
		game=games[int(args[0][3:-1])]
	except KeyError:
		try:
			games[int(args[0][3:-1])]=RpgSave(int(args[0][3:-1])).load(levels)
		except ValueError:
			games[int(args[0][3:-1])]=RpgGame(RpgPlayer(4,0,[],"O"),levels,0,int(args[0][3:-1]),data.copy())

async def tp(args):
	game=games[int(args[0][3:-1])]
	await game.setMap(int(args[1]))
	await game.map.goto(game,int(args[2]),int(args[3]))
	await updateReact([args[0]])
	dprint(game,game.map.getProjection(game.player))
	await dflush(game)

items={"dbanana":dBanana,"mToken":moveToken}
async def give(args):
	game=games[int(args[0][3:-1])]
	game.player.items+=[items[args[1]]]*int(args[2])

async def delete(args):
	game=games[int(args[0][3:-1])]
	game.player.items.pop(int(args[1]))

async def updateReact(args):
	game=games[int(args[0][3:-1])]
	await dreact(game,game.map.node(game.player).actions.keys())

commands={"tp":tp,"give":give,"🗑":delete,"updateReact":updateReact,"load":load}

@bot.command(pass_context=True)
async def sudo(ctx,*args):
	channel=ctx.message.channel
	await ctx.message.delete()
	if not ctx.message.author.id==756685684999192576: #me
		await channel.send("Only our rpg overlord Dalithop can run this!")
	else:
		try:
			await commands[args[0]](args[1:])
		except Exception as e:
			if hasattr(e,"message"):
				await channel.send("```\nsudo failed with \n{} {}\n```".format(e,e.message))
			else:
				await channel.send("```\nsudo failed with \n{}\n```".format(e))
		log("dalithop sudo'd '{}'".format(" ".join(args)))

@bot.event
async def on_ready():
	log('RPGBOT logged in as {0.user}'.format(bot))
	
bot.run(open("key.txt","r").read())  # pulls your token from key.txt and runs the bot

log("saving games...")
for game in games:
	RpgSave(games[game].user).store(games[game])
log("saved!")