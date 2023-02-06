import discord
from discord.ext import commands 
import schedule

#from main import bot

class MatchSchedule:  
  __monthly = False 
  __weekly = True
  __daily = False 
  __day = ""
  __time = ""

  def __init__(self):
    self.__monthly = False
    self.__weekly = True
    self.__daily = False
    self.__day = "friday"
    self.__time = "10:00"

  def setSchedule(self, frequency, time, day):

    frequency = frequency.toLowerCase()
    self.__day = day.toLowerCase()
    self.__time = time.toUpperCase()

    if frequency == "monthly":
      self.__monthly = True
      self.__weekly = False
      self.__daily = False

    elif frequency == "daily":
      self.__daily = False
      self.__weekly = False 
      self.__monthly = False

    else:
      self.__weekly = True
      self.__daily = False
      self.__monthly = False 

    self.time = time
    self.day = day
    
  def generateSchedule(self):

    if self.daily == True:
      return schedule.every().day().at(self.time)

    
      #if self.weekly == 
      
      #return schedule.every().
      