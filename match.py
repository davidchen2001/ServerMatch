from heap import MaxHeap
import random

MAX_MATCHES = 4
GROUP_MATCH_LABEL = "group match"

INTRODUCTION_FORMAT = "Name: \nGroup Match: 1-4 (1 by default)\nProgram: \nYear: \n (Feel free to add more fields! Just make sure each field has a \":\" to separate the labels and that each field exists on a newline."

INTRODUCTION_EXAMPLE = "Name: David\nGroup Match: 2\nProgram: CS\nYear: 4th\nHometown: Ottawa\nFavourite Anime: Spy X Family, Demon Slayer, Your Lie In April \nFun-Fact: I created this bot!\nMessage: Hi I'm David! I'm in my 4th year studying CS. Looking forward to chatting!"

def checkIntroduction(introduction):

  introduction = introduction.lower()
  
  #Check for name
  isName = "name:" not in introduction

  return not isName

def randomMatch(users):
    matches = {}
    
    max = len(users)

    for i in range(max):
      matchedUsers = []
      
      user = users[i]
      randomIndex = random.randint(0, max-1)

      while randomIndex == i:
        randomIndex = random.randint(0, max-1)
      secondUser = users[randomIndex]
      matchedUsers.append(secondUser)
      matches[user.getId()] = matchedUsers

    #Consider case of odd number of matches
    #Consider number of desired matches
    return matches

def createMatches(users):
   matches = {}
   heaps = []

   for i in range(len(users)):
    user = users[i]
    heap = MaxHeap()
    
    keywords, labels = parseIntroduction(user.getIntroduction())

    for j in range(len(users)):

      otherUser = users[j]
      if j != i and user.getId() != otherUser.getId():
        
        otherKeywords, otherLabels = parseIntroduction(otherUser.getIntroduction())
        
        numSameKeywords = sameKeywords(keywords, otherKeywords)
        
        totalKeywords = len(keywords) + len(otherKeywords)
        
        similarity = diceCoefficient(numSameKeywords, totalKeywords)
        
        heap.add(similarity, otherUser)

    heaps.append(heap)

   for i in range(len(users)):
    matchedUsers = []
    user = users[i]

    for j in range(MAX_MATCHES+1):

      if heaps[i].isEmpty() == False:

        match = heaps[i].pop()
        matchedUsers.append(match)
    
    matches[user.getId()] = matchedUsers

   return matches

def parseIntroduction(introduction):
    userKeywords = []
    userLabels = []
          
    data = introduction.split('\n')

    for pair in data:
      label = pair.split(":")[0]
      keyword = pair.split(":")[1]

      if "," in keyword:
        keywords = keyword.split(",")

        for word in keywords:
          userKeywords.append(word.lower())
      else:
        userKeywords.append(keyword.lower())
        
      userLabels.append(label.lower())
    return userKeywords, userLabels
  
def diceCoefficient(numSame, numKeywords):
    return (2 * numSame)/numKeywords

def sameKeywords(keywords, otherKeywords):

  numSame = 0
  for keyword in keywords:

    if keyword in otherKeywords:
      numSame += 1

  return numSame 

def findGroupMatches(user):

  introduction = user.getIntroduction()
  keywords, labels = parseIntroduction(introduction)

  if GROUP_MATCH_LABEL in labels:

    index = 0
    while index < len(keywords):
      if labels[index] == GROUP_MATCH_LABEL:
        numGroupMatches = int(keywords[index])
        if numGroupMatches > 0 and numGroupMatches <= MAX_MATCHES:
          return numGroupMatches
        else:
          return 1 

      index += 1

  return 1
