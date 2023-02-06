import random

DEFAULT = "RANDOM"
RECOMMEND = "RECOMMENDER"

class Match:

  algorithm = ""

  def __init__(self):
    self.algorithm = DEFAULT

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

    return matches

    