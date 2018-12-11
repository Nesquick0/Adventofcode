class Cell():
  def __init__(self, x, y, serial):
    self.x = x
    self.y = y
    self.serial = serial
    self.pl = 0
    
  def rackId(self):
    return self.x + 10
    
  def powerLevel(self):
    pl = self.rackId() * self.y
    pl += self.serial
    pl *= self.rackId()
    pl = ((pl//100)%10) - 5
    self.pl = pl # Cached
    return pl

def main():
  serial = 5177
  #print(Cell(122, 79, serial).powerLevel())
  
  cells = [None] * 300 * 300
  for y in range(0, 300):
    for x in range(0, 300):
      cell = Cell(x+1, y+1, serial)
      cell.powerLevel()
      cells[x + (y*300)] = cell
      
  #squareSize = 3 # Part 1, squareSize = 3
  #squareSize = 3
  squareSize = 300
      
  maxPL = -10000
  maxPos = [0, 0, 0]
  for s in range(1, squareSize+1):
    minS = (s//2)
    maxS = (s//2 + s%2)
    print(s, -minS, maxS)
    
    for y in range(minS, 300-(maxS-1)):
      # Get first square in row
      pl = 0
      x = minS
      for ys in range(-minS, maxS):
        for xs in range(-minS, maxS):
          pl += cells[x+xs + ((y+ys)*300)].pl
      if (pl > maxPL):
        maxPL = pl
        maxPos = [x+1-minS, y+1-minS, s]
      
      for x in range(minS+1, 300-(maxS-1)):
        xs = -minS-1
        for ys in range(-minS, maxS):
          pl -= cells[x+xs + ((y+ys)*300)].pl
        xs = maxS-1
        for ys in range(-minS, maxS):
          pl += cells[x+xs + ((y+ys)*300)].pl
        if (pl > maxPL):
          maxPL = pl
          maxPos = [x+1-minS, y+1-minS, s]
        
  print(maxPL, maxPos)

if (__name__ == "__main__"):
  main()