import heapq
import time 

class PriorityQueue:
    def __init__(self):
        self.__heap = []

    def add(self, key, val):
        seconds = time.time()
        heapq.heappush(self.__heap, (key, seconds, val))
    
    def pop(self):
        key, time, val = heapq.heappop(self.__heap)
        return val

    def findNode(self, node):

        for item in self.__heap:
            if str(node) == str(item):
                return True
        
        return False

    def __len__(self):
        return len(self.__heap)

    def isEmpty(self):

      return self.__len__() == 0

class MaxHeap(PriorityQueue):

  def __init__(self):
    super().__init__()
  
  def add(self, key, val):
    super().add(-1 * key, val)
    