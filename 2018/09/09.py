class Node():
  def __init__(self, data):
    self.data = data
    self.next = self
    self.prev = self
    
  def __str__(self):
    return "%d %d %d" % (self.data, self.next.data, self.prev.data)
    
    
def printList(node, curNode):
  firstNode = node
  print(node.data, end=" ")
  node = node.next
  while (node != firstNode):
    if (curNode == node):
      print("(%d)" % (node.data), end=" ")
    else:
      print(node.data, end=" ")
    node = node.next
  print("")

def main():
  players = [0]*463
  #marbles = 71787 # Part 1
  marbles = 71787*100 # Part 2
  
  player = 0
  curNode = Node(0)
  firstNode = curNode
  #printList(firstNode, curNode)
  
  for n in range(1, marbles+1):
    if (n%23 == 0):
      players[player] += n
      for i in range(7):
        curNode = curNode.prev
      players[player] += curNode.data
      # Remove node
      curNode.prev.next = curNode.next
      curNode.next.prev = curNode.prev
      curNode = curNode.next
    else:
      curNode = curNode.next
      # Add node
      newNode = Node(n)
      curNode.next.prev = newNode
      newNode.next = curNode.next
      newNode.prev = curNode
      curNode.next = newNode
      
      curNode = curNode.next
      
    #printList(firstNode, curNode)
    player = (player+1)%(len(players))
  
  print(players)
  print(max(players))
  

if (__name__ == "__main__"):
  main()