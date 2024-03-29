import discord
from discord.ext import commands, tasks
import os
import pymongo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import time

from schedule_match import MatchSchedule
from schedule_match import DAILY, WEEKLY
from member import Member
from match import randomMatch, INTRODUCTION_EXAMPLE, INTRODUCTION_FORMAT, checkIntroduction, createMatches, findGroupMatches
from config import mongoURI

INTRODUCTION_KEY = "introduction"

bot = commands.Bot(command_prefix="!",
                      case_insensitive = True,
                      intents=discord.Intents.all())

match_schedule = MatchSchedule()

client = pymongo.MongoClient(mongoURI)
db = client.get_database("comp4905")

scheduler = AsyncIOScheduler()
SCHEDULE_NAME = "Bot Schedule"

@bot.event
async def on_connect():
    print('We have logged in as {0.user}'.format(bot))
    scheduler.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, exception):
  #When a command 
  print("Command Failed")
  await ctx.send(f"Error: {exception}", reference = ctx.message)
  
@bot.command()
async def hello(ctx):
  print("Sending command")
  await ctx.channel.send("Hello World!")

@bot.command()
async def createBotChannel(ctx):
  channel = discord.utils.get(bot.get_all_channels(), guild__name=ctx.message.guild.name, name='roles')

  guild = ctx.guild

  if channel == None and ctx.author.guild_permissions.manage_channels:
    await guild.create_text_channel(name="server-match-bot")
  else:
    await ctx.channel.send("server-match-bot channel already exists")

@bot.command()
async def getCoffeeChatRole(ctx):
  member = ctx.message.author
  role = discord.utils.get(member.guild.roles, name="Coffee Chat")
  await member.add_roles(role)

@bot.command()
async def removeCoffeeChatRole(ctx):
  member = ctx.message.author
  role = discord.utils.get(member.guild.roles, name="Coffee Chat")
  await member.remove_roles(role)

@bot.command()
async def directMessage(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)

@bot.command()
async def setMatchSchedule(ctx, frequency=None, time=None, day=None):
    
  if frequency == None and time == None:
    await ctx.channel.send("Incorrect use of command. Format: !setMatchSchedule {frequency: daily, weekly} {time: 00:00 in 24 hour time} {day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday (optional if frequency is daily)}")
    
  else:

    hour_min = str(time).split(":")
    hour = int(hour_min[0])
    min = int(hour_min[1])

    if match_schedule.getInitialized() == True:
      scheduler.remove_all_jobs()
      
    if frequency == DAILY:
      
      job = scheduler.add_job(matchUsers, "cron", name = "schedule", args=[ctx], hour=hour, minute=min)
      print(job)

    elif frequency == WEEKLY:
      
      day = day.lower()[:3]
      job = scheduler.add_job(matchUsers, "cron", args=[ctx], day_of_week=day, hour=hour, minute = min)
      print(job)

  confirmationMessage = "Schedule has been set to " + frequency + " " + time

  if day != None:
    confirmationMessage += " "
    confirmationMessage += day

  match_schedule.setSchedule(frequency, time, day)
  await ctx.channel.send(confirmationMessage)

@bot.command()
async def getUsersWithChatRole(ctx):
  role = discord.utils.find(
    lambda r: r.name == "Coffee Chat", ctx.guild.roles)

  message = "Users with Coffee Chat role include:\n "

  for user in ctx.guild.members:
    if role in user.roles:
      message += user.name
      message += "\n"
  
  await ctx.send(message)

@bot.command()
async def sendMatch(ctx):
  await matchUsers(ctx)

async def matchUsers(ctx):
  role = discord.utils.find(
    lambda r: r.name == "Coffee Chat", ctx.guild.roles)

  listOfUsers = []
  userIdMap = {}
  userToIdMap = {}

  members = db.members
  
  for user in ctx.guild.members:
    if role in user.roles:
      newUser = Member(user.id, user.discriminator, user.name, user.roles)
      #If user exists in db, retrieve so you can retrieve their introduction
      member = members.find_one({"_id": user.id})
      if member != None:
        newUser.setIntroduction(member["introduction"])

      userIdMap[user.id] = newUser
      userToIdMap[user] = user.id
      listOfUsers.append(newUser)

  matches = createMatches(listOfUsers)

  for user in ctx.guild.members:
    if role in user.roles:
      id = userToIdMap[user]
      firstUser = userIdMap[id]

      matchedUsers = matches[id]
      
      directMessage = ""
      groupMatches = findGroupMatches(firstUser)
      groupCount = 0

      for match in matchedUsers:
        if groupCount < groupMatches:
          secondUser = userIdMap[match.getId()]
          directMessage += firstUser.createMessage(secondUser)
          directMessage += "\n"
          groupCount += 1
      
      try:
        await user.send(directMessage)
        
      except:
        
        print("Message Not Delivered")

@bot.command()
async def getIntroduction(ctx):
  member = ctx.message.author
  members = db.members
  findMember = members.find_one({"_id": member.id})
  await ctx.channel.send(str(findMember[INTRODUCTION_KEY]))

def parseSchedule():
  return match_schedule.generateSchedule()

@bot.command()
async def introductionFormat(ctx):
  message = INTRODUCTION_FORMAT
  message += "\n **Here is an example:** \n"
  message += INTRODUCTION_EXAMPLE
  await ctx.channel.send(message)
  
@bot.command()
async def setIntroduction(ctx, *, introduction):

  if checkIntroduction(introduction) == True:
    members = db.members
    
    for user in ctx.guild.members:
      
      if user.id == ctx.author.id:
  
        member = members.find_one({"_id": user.id})
  
        if member != None:
          update = { "$set" : {"introduction": introduction} }
          members.update_one(member, update)
          
        else:
          newUser = Member(user.id, user.discriminator, user.name, user.roles)
          newUser.setIntroduction(introduction)
          
          members.insert_one(newUser.toIntroductionDict())
  else:
    message = "Introduction needs to follow format:\n"
    message += INTRODUCTION_FORMAT
    message += "\n Run command **!introductionFormat** for more info."
    await ctx.channel.send(message)

try:
    my_secret = os.environ['DISCORD_BOT_SECRET']
    bot.run(my_secret)
  
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
        print("Type {kill 1} in the shell")
    else:
        raise e