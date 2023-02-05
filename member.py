class Member:

  id = ""
  name = ""
  roles = []

  def __init__(self, id, name, roles):
    self.id = id
    self.name = name

    for role in roles:
      if role.name != "@everyone":
        self.roles.append(role.name)
    
  def getId(self):
    return self.id
  
  def getName(self):
    return self.name
    
  def getRoles(self):
    return self.roles

  def createMessage(self, otherUser):
    message = "You have been matched with " + otherUser.name + " with ID: " + otherUser.id + ". Please message them at your earliest convienience to set up a time to chat"
    return message
     
  
  
  