import heapq

class PriorityQueue:
    def __init__(self):
        self.__heap = []

    def add(self, val, key=0):
        heapq.heappush(self.__heap, (key, val))
    
    def pop(self):
        key, val = heapq.heappop(self.__heap)
        return val

    def findNode(self, node):

        for item in self.__heap:
            if str(node) == str(item):
                return True
        
        return False

    def __len__(self):
        return len(self.heap)

    def isEmpty(self):

      return self.__len__(self) == 0

class MaxHeap(PriorityQueue):

  def __init__(self):
    PriorityQueue.__init__(self)
  
  def add(self, val, key=0):
    heapq.heappush(self.__heap, (-1 * key, val))