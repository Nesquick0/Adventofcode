import heapq

def checkSpace(maze, x, y, magicNumber):
  if ((x < 0) or (y < 0)):
    return False
  if (x not in maze):
    maze[x] = {}
  mazeX = maze[x]
  if (y not in mazeX):
    value = (bin(x*x + 3*x + 2*x*y + y + y*y + magicNumber).count("1") % 2) == 0
    mazeX[y] = value
    return value
  else:
    return mazeX[y]

def main():
  magicNumber = 1358
  targetPos = (31, 39)
  maze = {}
  moves = []
  visited = set()
  
  # for y in xrange(0, 40):
    # for x in xrange(0, 40):
      # if (x == 1 and y == 1):
        # print("s"),
      # elif (x == targetPos[0] and y == targetPos[1]):
        # print("x"),
      # else:
        # print("." if (checkSpace(maze, x, y, magicNumber)) else "#"),
    # print("")
    
  # steps, distance, x, y.
  dist = abs(targetPos[0] - 1) + abs(targetPos[1] - 1)
  heapq.heappush(moves, (0, dist, 1, 1))
  
  while (len(moves) > 0):
    steps, dist, x, y = heapq.heappop(moves)
    
    if (x == targetPos[0] and (y == targetPos[1])):
      print(steps)
      break
    
    newPositions = [ (x+1, y), (x-1, y), (x, y+1), (x, y-1) ]
    for newPos in newPositions:
      newX, newY = newPos
      if ((newPos not in visited) and checkSpace(maze, newX, newY, magicNumber)):
        dist = abs(targetPos[0] - newX) + abs(targetPos[1] - newY)
        heapq.heappush(moves, (steps+1, dist, newX, newY))
        visited.add( (newX, newY) )
  
  
if (__name__ == "__main__"):
  main()