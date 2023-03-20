import random

DEFAULT = "RANDOM"
RECOMMEND = "RECOMMENDER"

INTRODUCTION_FORMAT = "Name: \nGroup Match: 1-4 (1 by default)\nProgram: \nYear: \n (Feel free to add more fields! Just make sure each field has a \":\" to separate the labels and that each field exists on a newline."

INTRODUCTION_EXAMPLE = "Name: David\nGroup Match: 2\nProgram: CS\nYear: 4th\nHometown: Ottawa\nFavourite Anime: Spy X Family, Demon Slayer, Your Lie In April \nFun-Fact: I created this bot!\nMessage: Hi I'm David! I'm in my 4th year studying CS. Looking forward to chatting!"

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

  