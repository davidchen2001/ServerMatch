from heap import MaxHeap
import random

MAX_MATCHES = 4

INTRODUCTION_FORMAT = "Name: \nGroup Match: 1-4 (1 by default)\nProgram: \nYear: \n (Feel free to add more fields! Just make sure each field has a \":\" to separate the labels and that each field exists on a newline."

INTRODUCTION_EXAMPLE = "Name: David\nGroup Match: 2\nProgram: CS\nYear: 4th\nHometown: Ottawa\nFavourite Anime: Spy X Family, Demon Slayer, Your Lie In April \nFun-Fact: I created this bot!\nMessage: Hi I'm David! I'm in my 4th year studying CS. Looking forward to chatting!"

def checkIntroduction(introduction):

  introduction = introduction.lower()
  
  #Check for name
  isName = "name:" not in introduction

  return not isName

def randomMatch(users):
    matches = {}

    n = 0 

    while n < len(users):

      max = len(users)

      firstIndex = random.randint(0, max-1)
      firstUser = users[firstIndex]

      users.pop(firstIndex)

      max = len(users)
      secondIndex = random.randint(0, max-1)
      secondUser = users[secondIndex]

      users.pop(secondIndex)

      matches[firstUser.getId()] = secondUser.getId()
      matches[secondUser.getId()] = firstUser.getId()

      n += 2

    #Consider case of odd number of matches
    #Consider number of desired matches
    return matches

def createMatches(users):
   matches = {}

   for i in range(len(users)):
    user = users[i]
    heap = MaxHeap()
    keywords = parseIntroduction(user.getIntroduction())

    for j in range(len(users)):

      if j != i:
        otherUser = users[j]
        otherKeywords = parseIntroduction(otherUser.getIntroduction())

        numSameKeywords = sameKeywords(keywords, otherKeywords)
        totalKeywords = len(keywords) + len(otherKeywords)
        similarity = diceCoefficient(numSameKeywords, totalKeywords)
        heap.add(similarity, otherUser)

   for i in range(len(users)):
    matchedUsers = []
    user = users[i]

    for j in range(MAX_MATCHES):

      if heap.isEmpty() == False:

        match = heap.pop()
        matchedUsers.append(match)
    
    matches[user.getId()] = matchedUsers

   return matches

def parseIntroduction(introduction):
    userKeywords = []
          
    data = introduction.split('\n')

    for pair in data:
      label = pair.split(":")[0]
      keywords = pair.split(":")[1]

    for keyword in keywords:
      userKeywords.append(keyword.lower())

    return userKeywords
  
def diceCoefficient(numSame, numKeywords):
    return (2 * numSame)/numKeywords

def sameKeywords(keywords, otherKeywords):

  numSame = 0
  for keyword in keywords:

    if keyword in otherKeywords:
      numSame += 1

  return numSame 