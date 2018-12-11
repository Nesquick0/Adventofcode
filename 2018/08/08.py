def calcValue(nodes, nodeId):
  curNode = nodes[nodeId]

  # No childs, sum metadata
  if (len(curNode["childs"]) == 0):
    return sum(curNode["meta"])
  # Childs, get values from indexes
  else:
    value = 0
    for i in curNode["meta"]:
      if (i > 0 and i<=len(curNode["childs"])):
        value += calcValue(nodes, curNode["childs"][i-1])
    return value

def main():
  with open("input.txt", "r") as file:
    input = file.readline().strip().split(" ")

  input = list(map(int, input))
  #print(input)

  nodes = []
  nodeStack = []

  """
  2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
  A----------------------------------
      B----------- C-----------
                      D-----
  """

  i = 0
  while (i < len(input)):
    curNode = nodeStack[-1] if len(nodeStack) > 0 else None

    if (curNode != None and nodes[curNode]["nChilds"] == len(nodes[curNode]["childs"])):
      # Read metadata
      for m in range(nodes[curNode]["nMeta"]):
        nodes[curNode]["meta"].append(input[i])
        i += 1
      nodeStack.pop()
      if (len(nodeStack) > 0):        
        nodes[nodeStack[-1]]["childs"].append(curNode)
    else:
      nChilds = input[i]
      numMeta = input[i+1]
      nodes.append( {"nChilds": nChilds, "nMeta": numMeta, "childs": [], "meta": []} ) # Add node
      nodeStack.append(len(nodes)-1)
      i += 2

  # Part 1
  result = 0
  for node in nodes:
    #print(node)
    result += sum(node["meta"])
    #for meta in node["meta"]:
    #  result += meta
  print(result)

  # Part 2
  print(calcValue(nodes, 0))




if (__name__ == "__main__"):
  main()