class Node():
  def __init__(self, data):
    self.data = data
    self.next = self
    self.prev = self


class Main():
  def __init__(self):
    self.firstNode = None
    self.elves = []
    self.input = None

  def printNode(self, node):
    if (node == self.elves[0]):
      print("(%d)" % (node.data), end="")
    elif (node == self.elves[1]):
      print("[%d]" % (node.data), end="")
    else:
      print(" %d " % (node.data), end="")

  def printList(self):
    node = self.firstNode
    self.printNode(node)
    node = node.next
    while (node != self.firstNode):
      self.printNode(node)
      node = node.next
    print("")

  def checkInput(self, lastNode):
    checkNode = lastNode
    if (checkNode.data != self.input[-1]):
      return False
    for i in range(len(self.input)-2, -1, -1):
      checkNode = checkNode.prev
      if (checkNode.data != self.input[i]):
        return False
    return True



  def run(self):
    #self.input = [5,1,5,8,9]
    #self.input = [5,9,4,1,4]
    self.input = [3,0,6,2,8,1]
    self.firstNode = Node(3)
    lastNode = Node(7)
    self.firstNode.next = lastNode
    self.firstNode.prev = lastNode
    lastNode.next = self.firstNode
    lastNode.prev = self.firstNode

    self.elves = [self.firstNode, lastNode]

    #self.printList()
    created = 2
    while True:
      # Create new recipe
      newRec = self.elves[0].data + self.elves[1].data
      if (newRec >= 10):
        newNode = Node(newRec // 10)
        newNode.next = self.firstNode
        self.firstNode.prev = newNode
        newNode.prev = lastNode
        lastNode.next = newNode
        lastNode = newNode
        created += 1
        if (self.checkInput(lastNode)):
          break

      newNode = Node(newRec % 10)
      newNode.next = self.firstNode
      self.firstNode.prev = newNode
      newNode.prev = lastNode
      lastNode.next = newNode
      lastNode = newNode
      created += 1
      if (self.checkInput(lastNode)):
        break

      # Move elves
      for i in range(len(self.elves)):
        curValue = self.elves[i].data + 1
        for c in range(curValue):
          self.elves[i] = self.elves[i].next

    #self.printList()
    print(created)
    print(created - len(self.input))
      



if (__name__ == "__main__"):
  Main().run()