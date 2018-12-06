def distance(x, y, x2, y2):
  return abs(x2 - x) + abs(y2 - y)
  
  
def distanceToAll(x, y, positions):
  distances = {}
  for pos in positions:
    distances[pos] = distance(x, y, pos[0], pos[1])
  return distances

  
def printWorld(positions):
  for y in range(sizeY):
    for x in range(sizeX):
      value = world[y*sizeX + x]
      print(value if (value >= 0) else ".", end=" ")
    print("")
    

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  positions = {}
  for line in input:
    lineSplit = line.strip().split(", ")
    positions[(int(lineSplit[0]), int(lineSplit[1]))] = [0, True]

  minPos = list(list(positions.keys())[0])
  maxPos = list(list(positions.keys())[0])
  for pos in positions:
    minPos[0] = min(minPos[0], pos[0])
    minPos[1] = min(minPos[1], pos[1])
    maxPos[0] = max(maxPos[0], pos[0])
    maxPos[1] = max(maxPos[1], pos[1])
  
  #print(positions)
  print(minPos, maxPos)
  sizeX, sizeY = maxPos[0] - minPos[0] + 1, maxPos[1] - minPos[1] + 1
  
  for y in range(sizeY):
    for x in range(sizeX):
      distances = distanceToAll(x + minPos[0], y + minPos[0], positions)
      
      minDist = 9999999
      for pos in distances:
        if (distances[pos] < minDist):
          minDist = distances[pos]
      
      closestPos = None
      for pos in distances:
        if (distances[pos] == minDist):
          if (closestPos): # Already taken
            closestPos = None
            break
          closestPos = pos
          
      value = -1
      if (closestPos):
        positions[closestPos][0] += 1
        # Border
        #if ((x==0 and y==0) or (x==sizeX-1 and y==sizeY-1) or
        #  (x==0 and y==sizeY-1) or (x==sizeX-1 and y==0)):
        if (x==0 or y==0 or x==sizeX-1 or y==sizeY-1):  
          positions[closestPos][1] = False
        value = list(positions.keys()).index(closestPos)
        
      #print(value if (value >= 0) else ".", end=" ")
    #print("")
        
  maxArea = 0
  maxAreaPos = ()
  for pos in positions:
    if (positions[pos][1] and positions[pos][0] > maxArea):
      maxArea = positions[pos][0]
      maxAreaPos = pos
    print(pos, positions[pos])
  print(maxAreaPos, positions[maxAreaPos], maxArea)

if (__name__ == "__main__"):
  main()