class Node():
  def __init__(self, data):
    self.data = data
    self.next = self
    self.prev = self
    
  def __str__(self):
    return "%d %d %d" % (self.data, self.next.data, self.prev.data)


class Main():
  def __init__(self):
    self.firstNode = None
    self.elves = []

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

  def run(self):
    input = 306281
    self.firstNode = Node(3)
    lastNode = Node(7)
    self.firstNode.next = lastNode
    self.firstNode.prev = lastNode
    lastNode.next = self.firstNode
    lastNode.prev = self.firstNode

    self.elves = [ self.firstNode, lastNode]

    #self.printList()
    created = 2
    while (created < (input + 10)):
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

      newNode = Node(newRec % 10)
      newNode.next = self.firstNode
      self.firstNode.prev = newNode
      newNode.prev = lastNode
      lastNode.next = newNode
      lastNode = newNode
      created += 1

      # Move elves
      for i in range(len(self.elves)):
        curValue = self.elves[i].data + 1
        for c in range(curValue):
          self.elves[i] = self.elves[i].next

      #self.printList()

    printNode = lastNode
    if (created > input + 10):
      printNode = printNode.prev
    values = []
    for i in range(10):
      values.append(printNode.data)
      printNode = printNode.prev
    print("".join(list(map(str, reversed(values)))))
      



if (__name__ == "__main__"):
  Main().run()