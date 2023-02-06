import discord
from discord.ext import commands 
import os
from os import system
from keep_alive import keep_alive
from schedule_match import MatchSchedule
from member import Member
from match import Match

bot = commands.Bot(command_prefix="!",
                      case_insensitive = True,
                      intents=discord.Intents.all())

match_schedule = MatchSchedule()
match = Match()

@bot.event
async def on_connect():
    print('We have logged in as {0.user}'.format(bot))

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
async def createRolesChannel(ctx):
  channel = discord.utils.get(bot.get_all_channels(), guild__name=ctx.message.guild.name, name='roles')

  guild = ctx.guild

  if channel == None and ctx.author.guild_permissions.manage_channels:
    await guild.create_text_channel(name="roles")
  else:
    await ctx.channel.send("roles channel already exists")

@bot.command()
async def directMessage(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)

@bot.command()
async def setMatchSchedule(ctx, message=None):
  if message != None:
    scheduleParams = message.split()
    
  if message == None or len(scheduleParams) < 2:
    await ctx.channel.send("Incorrect use of command. Format: !setMatchSchedule {frequency: monthly, weekly, daily} {time: 00:00 in 24 hour time} {day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday (optional if frequency is daily)}")
  else:
    match_schedule.setSchedule(scheduleParams[0], scheduleParams[1], scheduleParams[2])
    confirmationMessage = "Schedule has been set to " + scheduleParams[0] + " " + scheduleParams[1] + " " + scheduleParams[2]
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
  role = discord.utils.find(
    lambda r: r.name == "Coffee Chat", ctx.guild.roles)

  listOfUsers = []
  userIdMap = {}
  userToIdMap = {}
  
  for user in ctx.guild.members:
    if role in user.roles:
      newUser = Member(user.id, user.discriminator, user.name, user.roles)
      userIdMap[user.id] = newUser
      userToIdMap[user] = user.id
      listOfUsers.append(newUser)

  matches = match.randomMatch(listOfUsers)

  for user in ctx.guild.members:
    if role in user.roles:
      id = userToIdMap[user]
      firstUser = userIdMap[id]
      secondUserId = matches[id]
      secondUser = userIdMap[secondUserId]
      
      try:
        
        directMessage = firstUser.createMessage(secondUser)
        
        await user.send(directMessage)
      except:
        print("Message Not Delivered")

def parseSchedule():
  return match_schedule.generateSchedule()

try:
    #keep_alive()
    my_secret = os.environ['DISCORD_BOT_SECRET']
    bot.run(my_secret)
  
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
        print("Type {kill 1} in the shell")
    else:
        raise e