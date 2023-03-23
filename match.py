from heap import MaxHeap
import random

DEFAULT = "RANDOM"
RECOMMEND = "RECOMMENDER"

INTRODUCTION_FORMAT = "Name: \nGroup Match: 1-4 (1 by default)\nProgram: \nYear: \n (Feel free to add more fields! Just make sure each field has a \":\" to separate the labels and that each field exists on a newline."

INTRODUCTION_EXAMPLE = "Name: David\nGroup Match: 2\nProgram: CS\nYear: 4th\nHometown: Ottawa\nFavourite Anime: Spy X Family, Demon Slayer, Your Lie In April \nFun-Fact: I created this bot!\nMessage: Hi I'm David! I'm in my 4th year studying CS. Looking forward to chatting!"

def checkIntroduction(introduction):

  introduction = introduction.lower()
  
  #Check for name
  isName = "name:" not in introduction

  return not isName

class Match:

  __algorithm = ""

  def __init__(self):
    self.__algorithm = DEFAULT

  def randomMatch(self, users):
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

  def recommenderMatch(self, users):

    #For every pair of users - (2 x number of same keywords)/total_keywords

    matches = {}

    for i in range(len(users)):

      max_coefficient = 0
      max_coefficient_index = 0
      introduction = users[i].getIntroduction()
      userKeywords = self.__parseIntroduction__(introduction)

      for j in range(len(users)):

        otherIntroduction = users[j].getIntroduction()
        otherKeywords = self.__parseIntroduction__(otherIntroduction)

        for keyword in userKeywords:

          num_same = 0
          if keyword in otherKeywords:
            num_same += 1

        total_keywords = len(userKeywords) + len(otherKeywords)
        dice_coefficient = self.__dice_coefficient__(num_same, total_keywords)

        if max_coefficient < dice_coefficient:
          max_coefficient = dice_coefficient
          max_coefficient_index = j 

      firstUser = users[i].getId()
      secondUser = users[max_coefficient_index].getId()
      matches[firstUser.getId()] = secondUser.getId()
      
    return matches
          
  def __dice_coefficient__(self, num_same, num_keywords):
    return (2 * num_same)/num_keywords

  def __parseIntroduction__(self, introduction):
    userKeywords = []
          
    data = introduction.split('\n')

    for pair in data:
      label = pair.split(":")[0]
      keywords = pair.split(":")[1]

    for keyword in keywords:
      userKeywords.append(keyword.lower())

    return userKeywords
    