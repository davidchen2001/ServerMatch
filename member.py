import json

class Member:

  __id = ""
  __tag = ""
  __name = ""
  __roles = []
  __introduction = ""

  def __init__(self, id, tag, name, roles):
    self.__id = id
    self.__tag = tag 
    self.__name = name

    for role in roles:
      if role.name != "@everyone":
        self.__roles.append(role.name)
    
  def getId(self):
    return self.__id

  def getTag(self):
    return self.__tag
  
  def getName(self):
    return self.__name
    
  def getRoles(self):
    return self.__roles

  def setIntroduction(self, introduction):
    self.__introduction = introduction

  def getIntroduction(self):
    return self.__introduction

  def createMessage(self, otherUser):
    
    message = "You have been matched with " + otherUser.getName() + "#" + otherUser.getTag() + ". Please message them at your earliest convienience to set up a time to chat. \n"

    if len(otherUser.getIntroduction()) > 0:
      message += "Here is their introduction: \n" + otherUser.getIntroduction()
    
    return message
     
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, 
                      sort_keys=True, indent=4)  
  
  def toDict(self):
    dict = {}

    dict["_id"] = self.__id
    dict["tag"] = self.__tag
    dict["name"] = self.__name
    dict["roles"] = self.__roles
    dict["introduction"] = self.__introduction 
    
    return dict 

  def toIntroductionDict(self):
    dict = {}

    dict["_id"] = self.__id
    dict["introduction"] = self.__introduction

    return dict