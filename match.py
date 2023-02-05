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

      firstIndex = random.randint(0, max)
      secondIndex = random.randint(0, max)

      firstUser = users[firstIndex]
      secondUser = users[secondIndex]

      matches[firstUser.id] = secondUser.id
      matches[secondUser.id] = firstUser.id

      users.pop(firstIndex)
      users.pop(secondIndex)

      n += 2

    return matches

    