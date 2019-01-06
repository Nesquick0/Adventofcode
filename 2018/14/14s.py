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

  def checkInput(self):
    if (self.input != self.nodes[-len(self.input):]):
      return False
    return True


  def run(self):
    #self.input = [5,1,5,8,9]
    #self.input = [5,9,4,1,4]
    self.input = [3,0,6,2,8,1]
    self.nodes = [3, 7]

    self.elves = [0, 1]

    #self.printList()
    while True:
      # Create new recipe
      newRec = self.nodes[self.elves[0]] + self.nodes[self.elves[1]]
      if (newRec >= 10):
        self.nodes.append(newRec // 10)
        if (self.checkInput()):
          break

      self.nodes.append(newRec % 10)
      if (self.checkInput()):
        break

      # Move elves
      for i in range(len(self.elves)):
        curValue = self.nodes[self.elves[i]] + 1
        self.elves[i] = (self.elves[i] + curValue) % len(self.nodes)

    #self.printList()
    print(len(self.nodes))
    print(len(self.nodes) - len(self.input))
      



if (__name__ == "__main__"):
  Main().run()