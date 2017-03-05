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
  maze = {}
  moves = []
  visited = set()
  visited.add( (1, 1) )
    
  # steps, x, y.
  heapq.heappush(moves, (0, 1, 1))
  
  while (len(moves) > 0):
    steps, x, y = heapq.heappop(moves)
    
    newPositions = [ (x+1, y), (x-1, y), (x, y+1), (x, y-1) ]
    for newPos in newPositions:
      newX, newY = newPos
      if ((steps < 50) and (newPos not in visited) and checkSpace(maze, newX, newY, magicNumber)):
        heapq.heappush(moves, (steps+1, newX, newY))
        visited.add( (newX, newY) )
        
  print(len(visited))
  
  
if (__name__ == "__main__"):
  main()