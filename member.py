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
  
     
  
  
  