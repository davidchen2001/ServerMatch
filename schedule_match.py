DAILY = "daily"
WEEKLY = "weekly"

MONDAY = "monday"
TUESDAY = "tuesday"
WEDNESDAY = "wednesday"
THURSDAY = "thursday"
FRIDAY = "friday"
SATURDAY = "saturday"
SUNDAY = "sunday"

class MatchSchedule:  
  __frequency = ""
  __day = ""
  __time = ""

  def __init__(self):
    self.__frequency = WEEKLY
    self.__day = FRIDAY
    self.__time = "10:00"
    self.__initialized = False 

  def getFrequency(self):
    return self.__frequency

  def getDay(self):
    return self.__day

  def getTime(self):
    return self.__time 

  def getInitialized(self):
    return self.__initialized
  
  def setSchedule(self, frequency, time, day):

    self.__frequency = frequency.toLowerCase()
    self.__day = day.toLowerCase()
    self.__time = time.toUpperCase()
    self.__initialized = True

  