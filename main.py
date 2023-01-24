import discord
from discord.ext import commands 
import os
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="!",
                      case_insensitive = True,
                      intents=discord.Intents.all())

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

@bot.event
async def on_guild_channel_create(channel):
    await print('the channel has been created')
    return

@bot.command()
async def create_roles_channel(ctx):
  channel = discord.utils.get(bot.get_all_channels(), guild__name=ctx.message.guild.name, name='roles')

  if channel == None:
    bot.on_guild_channel_create('roles')

try:
    #keep_alive()
    my_secret = os.environ['DISCORD_BOT_SECRET']
    bot.run(my_secret)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e