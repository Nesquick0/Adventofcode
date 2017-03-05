def main():
  with open("22.input", "r") as file:
    fileContent = file.readlines()
    
  values = fileContent[-1].strip().split(" ")
  name = values[0].split("-")
  maxX, maxY = int(name[1][1:]), int(name[2][1:])
  print(maxX, maxY)
  
  nodes = {}
    
  for i in xrange(2, len(fileContent)):
    line = fileContent[i].strip()
    values = line.split()
    name = values[0].split("-")
    x, y = int(name[1][1:]), int(name[2][1:])
    if (x not in nodes):
      nodes[x] = {}
    # Size, Used, Avail
    nodes[x][y] = [ int(values[1][:-1]), int(values[2][:-1]), int(values[3][:-1]) ]
  
  #for node in nodes:
  #  print(node, nodes[node])
  
  countViable = 0
  for x in nodes:
    for y in nodes[x]:
      node = nodes[x][y]
      if (node[1] > 0):
        for x2 in nodes:
          for y2 in nodes[x2]:
            if (node[1] <= nodes[x2][y2][2]):
              countViable += 1
              
  print(countViable)
  
if (__name__ == "__main__"):
  main()