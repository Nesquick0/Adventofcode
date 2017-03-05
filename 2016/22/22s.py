import heapq

def drawGrid(targetPos, wantedPos, freePos, disabled, maxX, maxY):
  for y in xrange(maxY+1):
    text = ""
    for x in xrange(maxX+1):
      if (x == targetPos[0] and y == targetPos[1]):
        text += "("
      else:
        text += " "
        
      if (x == wantedPos[0] and y == wantedPos[1]):
        text += "G"
      elif (x == freePos[0] and y == freePos[1]):
        text += "_"
      elif (disabled[x][y]):
        text += "#"
      else:
        text += "."
        
      if (x == targetPos[0] and y == targetPos[1]):
        text += ")"
      else:
        text += " "
      
    print(text)

    
def main():
  with open("22.input", "r") as file:
    fileContent = file.readlines()
    
  values = fileContent[-1].strip().split(" ")
  name = values[0].split("-")
  maxX, maxY = int(name[1][1:]), int(name[2][1:])
  print(maxX, maxY)
  
  nodes = {}
  targetPos = (0, 0)
  wantedPos = (maxX, 0)
    
  for i in xrange(2, len(fileContent)):
    line = fileContent[i].strip()
    values = line.split()
    name = values[0].split("-")
    x, y = int(name[1][1:]), int(name[2][1:])
    if (x not in nodes):
      nodes[x] = {}
    # Size, Used, Avail
    nodes[x][y] = [ int(values[1][:-1]), int(values[2][:-1]), int(values[3][:-1]) ]
    if (nodes[x][y][1] == 0):
      freePos = (x, y)
  
  disabled = {}
  for x in nodes:
    disabled[x] = {}
    for y in nodes[x]:
      largePos = True
      used = nodes[x][y][1]
      # Size of neighbour smaller than used.
      if ((x > 0) and (nodes[x-1][y][0] >= used)):
        largePos = False
      if ((x < maxX) and (nodes[x+1][y][0] >= used)):
        largePos = False
      if ((y > 0) and (nodes[x][y-1][0] >= used)):
        largePos = False
      if ((y < maxY) and (nodes[x][y+1][0] >= used)):
        largePos = False
      if (used > 100):
        largePos = True # HACKED
        
      disabled[x][y] = largePos
      
  
  drawGrid(targetPos, wantedPos, freePos, disabled, maxX, maxY)
  print("")
  
  moves = []
  visited = set()
  #A* in 13.py
  #BFS in 11s2.py
  
  # steps, distance, distance free to wanted, wantedPos, freePos.
  dist = abs(wantedPos[0] - targetPos[0]) + abs(wantedPos[1] - targetPos[1])
  distFree = abs(wantedPos[0] - freePos[0]) + abs(wantedPos[1] - freePos[1])
  heapq.heappush(moves, (0, dist, distFree, wantedPos, freePos))
  visited.add( (wantedPos, freePos) )
  
  while (len(moves) > 0):
    steps, dist, distFree, wantedPos, freePos = heapq.heappop(moves)
    
    if (wantedPos[0] == targetPos[0] and (wantedPos[1] == targetPos[1])):
      drawGrid(targetPos, wantedPos, freePos, disabled, maxX, maxY)
      print(steps)
      break
    
    x, y = freePos
    
    newPositions = []
    if ((x > 0) and (not disabled[x-1][y])):
      newPositions.append( (x-1, y) )
    if ((x < maxX) and (not disabled[x+1][y])):
      newPositions.append( (x+1, y) )
    if ((y > 0) and (not disabled[x][y-1])):
      newPositions.append( (x, y-1) )
    if ((y < maxY) and (not disabled[x][y+1])):
      newPositions.append( (x, y+1) )
    
    for newPos in newPositions:
      newX, newY = newPos
      wantedX, wantedY = wantedPos
      if (wantedX == newX and wantedY == newY):
        wantedX, wantedY = x, y
      
      newState = ( (wantedX, wantedY), (newX, newY) )
      if (newState not in visited):
        wantedNew = (wantedX, wantedY)
        freeNew = (newX, newY)
        dist = abs(wantedNew[0] - targetPos[0]) + abs(wantedNew[1] - targetPos[1])
        distFree = abs(wantedNew[0] - freeNew[0]) + abs(wantedNew[1] - freeNew[1])
        
        heapq.heappush(moves, (steps+1, dist, distFree, wantedNew, freeNew))
        visited.add(newState)

  
if (__name__ == "__main__"):
  main()