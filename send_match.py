import discord
from discord.ext import commands 
import schedule

#from main import bot

class MatchSchedule:  
  monthly = False 
  weekly = True
  daily = False 
  day = "friday"
  time = "10:00"

  def __init__(self):
    return

  def setSchedule(self, frequency, time, day):

    frequency = frequency.toLowerCase()
    day = day.toLowerCase()
    time = time.toUpperCase()

    if frequency == "monthly":
      self.monthly = True
      self.weekly = False
      self.daily = False

    elif frequency == "daily":
      self.daily = False
      self.weekly = False 
      self.monthly = False

    else:
      self.weekly = True
      self.daily = False
      self.monthly = False 

    self.time = time
    self.day = day
    
  def generateSchedule(self):

    if self.daily == True:
      return schedule.every().day().at(time)

    elif self.weekly == True:
      #if self.weekly == 
      
      #return schedule.every().
      