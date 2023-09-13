import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime as dt
import random
import os
import sys
import random
import csv

intents = discord.Intents.all()
client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix='&',intents=intents)

picfile = open('Data.txt', 'r')
Collection = []
Original = []
for row in picfile.readlines():
    Collection.append(row)
    Original.append(row)
picfile.close()

bans = open('Banned.txt','r')
rb = csv.reader(bans)
banpeeps = []
for line in rb:
    banpeeps.append(line)
bans.close()

third = open('thirdwarn.txt', 'r+')
reader3 = csv.reader(third)
third.truncate(0)
warn3 =[]
for row in reader3:
    if row not in banpeeps:
        warn3.append(row)
with open('thirdwarn.txt','w') as t:
    for e in warn3:
        t.write('%s,'%e)
t.close()

second = open('seconwarn.txt', 'r+')
reader2 = csv.reader(second)
second.truncate(0)
warn2 = []
for line in reader2:
    if line not in warn3 and line not in banpeeps:
        warn2.append(line)
with open('seconwarn.txt','w') as s:
    for o in warn2:
        s.write('%s,'%o)
s.close()

first = open('firstwarn.txt', 'r+')
reader1 = csv.reader(first)
first.truncate(0)
warn1 = []
for line in reader1:
    if line not in warn1 and line not in banpeeps and line not in warn2:
        warn1.append(line)
with open('firstwarn.txt','w') as f:
    for k in warn1:
        f.write('%s,'%k)
f.close()

def lol(file,arg):
    l = open(file,'a')
    l.write('%s,'%arg)
    l.close()


@bot.event
async def on_ready():
    print("Hello World!!")

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("**YO PEEPS**,This bot completely runs on the discord community and its people.\n"
        +"There are only **3 commands** for this bot: \n"
        +"1) ~new: attatch a image with this image an send (attatch max upto 5 image at a time, even if u add more it wont work ehe)\n"
        +"2) ~img: randomly gives Drawing/Artwork from its ***Collection*** (you can add a number after this command for that many pics. *PS: max is 5*\n"
        +"3) ~helpme: ehe :rofl:\n"
        +"**PS**: Pls do add a spoiler tag when adding nsfw :pray: , *not that I can do anythign about it ehe.. well, as I said, dependent on the people* \n"
        +"**I BELEIVE ART SHOULD BE SPREAD, WHETHER THEY ARE GOOD OR BAD AND THATS WHY I MADE THIS BOT** *||idc about about ur opinion||*")
        break

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**STILL ON COOLDOWN MF**, pls try again in {:.0f}s'.format(error.retry_after)
        await ctx.channel.send(msg)


@bot.command(name = 'img', aliases= ['i','im'])
@commands.cooldown(1,5,commands.BucketType.user)
async def img(ctx, lawl=1):
    ida = ctx.author.id
    if ida not in banpeeps:
        num = int(lawl)
        if num > 5:
            await ctx.channel.send("Calm Dowm MF, maximum 5 at a time")
        elif 6>num and num>0:
            for j in range(0,num):
                damn = (str(random.choice(Collection)))
                if 'SPOILER_' in damn:
                    await ctx.channel.send('|| '+damn+' ||')
                else:
                    await ctx.channel.send(damn)
        else:
            await ctx.channel.send(str(random.choice(Collection)))

@bot.command(name = 'new', aliases= ['n','ew'])
@commands.cooldown(1,5,commands.BucketType.user)
async def new(ctx):
    ida = ctx.author.id
    if ida not in banpeeps:
        length = len(ctx.message.attachments)
        if length > 5:
            await ctx.channel.send("Maximum is 5 attatchments dude")
        else:
            for k in range(0,length):
                mess = ctx.message.attachments[k]
                if mess.content_type in ('image/jpeg', 'image/jpg', 'image/png'):
                    ima = str(mess)
                    if ima in Collection:
                        await ctx.channel.send("Initializing.....")
                        await ctx.channel.send("MF DONE ALREADY")
                    else:
                        await ctx.channel.send("Initializing.....")
                        Collection.append(ima)
                        for i in Collection:
                            if i not in Original:
                                pro = str(i)
                                lol('Data.txt',pro)
                                Original.append(ima)
                        await ctx.channel.send("Added")
                else:
                    await ctx.channel.send("DONT BE SMART MF, SEND ONLY IMAGES OR IMMA BAN U FROM THIS BOT.")
                    if ida in warn3:
                        await ctx.channel.send("Congrats!! You got urself banned on this bot, now get lost and comprehend ur life choices.")
                        warn3.remove(ida)
                        banpeeps.append(ida)
                        lol('Banned.txt',ida)
                    elif ida in warn2:
                        warn2.remove(ida)
                        warn3.append(ida)
                        lol('thirdwarn.txt',ida)
                        await ctx.channel.send("You have no warns left. Be sensible and post only images.")
                    elif ida in warn1:
                        warn1.remove(ida)
                        warn1.append(ida)
                        lol('seconwarn.txt',ida)
                        await ctx.channel.send("You have only one warn laft. Be carefull, dont send anythign other than an image")
                    else:
                        warn1.append(ida)
                        lol('firstwarn.txt',ida)
                        await ctx.channel.send("Congrats!! You got ur first warn, u got 2 warns left b4 u get banned from this bot")


bot.run('TOKEN HERE')
