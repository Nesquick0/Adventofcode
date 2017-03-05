import itertools

def main():
  with open("24.input", "r") as file:
    fileContent = file.readlines()
    
  maze = []
  for line in fileContent:
    line = line.strip()
    values = list(line)
    values = map(lambda x: int(x) if x.isdigit() else x, values)
    values = map(lambda x: -9 if x == "#" else x, values)
    values = map(lambda x: -1 if x == "." else x, values)
    maze.append(values)
  
  # Find special positions in maze.
  positions = {}
  for y in xrange(len(maze)):
    for x in xrange(len(maze[y])):
      if (maze[y][x] >= 0):
        positions[maze[y][x]] = (x, y)
        
  print(positions)
  
  distances = {}
  # From each positions find shortest distance to each other position.
  for pos in positions:
    distances[pos] = {}
    start = positions[pos]
    
    # x, y, steps
    states = [(start[0], start[1], 0)]
    # Create copy of maze.
    mazeCopy = []
    for line in maze:
      mazeCopy.append(list(line))
    
    while (len(states) > 0):
      x, y, steps = states.pop(0)
      
      if (mazeCopy[y][x] <= -2):
        continue
      
      if (mazeCopy[y][x] >= 0):
        distances[pos][mazeCopy[y][x]] = steps
        
      mazeCopy[y][x] = -2
      
      if (mazeCopy[y][x-1] >= -1):
        states.append( (x-1, y, steps+1) )
      if (mazeCopy[y][x+1] >= -1):
        states.append( (x+1, y, steps+1) )
      if (mazeCopy[y-1][x] >= -1):
        states.append( (x, y-1, steps+1) )
      if (mazeCopy[y+1][x] >= -1):
        states.append( (x, y+1, steps+1) )
        
  #for pos in distances:
  #  print(pos, distances[pos])
  
  # Find shortest path between all positions. Always start at 0.
  minDistance = 10**10
  nItems = len(positions)-1
  for perm in itertools.permutations(range(1, len(positions))):
    dist = distances[0][perm[0]]
    for i in xrange(nItems-1):
      dist += distances[perm[i]][perm[i+1]]
    if (dist < minDistance):
      minDistance = dist
  
  print(minDistance)

if (__name__ == "__main__"):
  main()