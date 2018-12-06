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
    
  totalDistance = 10000

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
  
  validPos = 0
  
  for y in range(sizeY):
    for x in range(sizeX):
      distances = distanceToAll(x + minPos[0], y + minPos[0], positions)
      
      sumDist = 0
      for pos in distances:
        sumDist += distances[pos]
      
      if (sumDist < totalDistance):
        validPos += 1
        
  print(validPos)

if (__name__ == "__main__"):
  main()