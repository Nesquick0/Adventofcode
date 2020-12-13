class World:
  def __init__(self):
    self.world = []
    self.width = 0
    self.height = 0

  def getPos(self, x, y):
    if (x >= 0 and x < self.width and y >= 0 and y < self.height):
      return self.world[x + y * self.width]
    return -1

  def getVisible(self, x, y, dx, dy):
    value = self.getPos(x, y)
    if (value == 1 or value == 2):
      return value
    elif (value == -1):
      return -1
    else:
      return self.getVisible(x + dx, y + dy, dx, dy)

  def countAround(self, x, y):
    num = 0
    num += 1 if (self.getPos(x-1, y-1) == 2) else 0
    num += 1 if (self.getPos(x  , y-1) == 2) else 0
    num += 1 if (self.getPos(x+1, y-1) == 2) else 0

    num += 1 if (self.getPos(x-1, y  ) == 2) else 0
    num += 1 if (self.getPos(x+1, y  ) == 2) else 0

    num += 1 if (self.getPos(x-1, y+1) == 2) else 0
    num += 1 if (self.getPos(x  , y+1) == 2) else 0
    num += 1 if (self.getPos(x+1, y+1) == 2) else 0
    return num

  def countVisible(self, x, y):
    num = 0
    num += 1 if (self.getVisible(x-1, y-1, -1, -1) == 2) else 0
    num += 1 if (self.getVisible(x  , y-1,  0, -1) == 2) else 0
    num += 1 if (self.getVisible(x+1, y-1,  1, -1) == 2) else 0

    num += 1 if (self.getVisible(x-1, y  , -1,  0) == 2) else 0
    num += 1 if (self.getVisible(x+1, y  , +1,  0) == 2) else 0

    num += 1 if (self.getVisible(x-1, y+1, -1,  1) == 2) else 0
    num += 1 if (self.getVisible(x  , y+1,  0,  1) == 2) else 0
    num += 1 if (self.getVisible(x+1, y+1,  1,  1) == 2) else 0
    return num
    
  
  def draw(self):
    for pos in range(len(self.world)):
      if (pos % self.width == 0):
        print("")
      if (self.world[pos] == 2):
        print("#", end="")
      elif (self.world[pos] == 1):
        print("L", end="")
      else:
        print(".", end="")
    print("")

  def reset(self):
    for pos in range(len(self.world)):
      if (self.world[pos] == 2):
        self.world[pos] = 1

def runFirst(world):
  run = True
  while (run):
    run = False
    worldNew = world.world[:]
    for pos in range(len(world.world)):
      x = pos % world.width
      y = pos // world.width

      if (world.world[pos] == 1 and world.countAround(x, y) == 0):
        worldNew[x + y * world.width] = 2
        run = True
      elif (world.world[pos] == 2 and world.countAround(x, y) >= 4):
        worldNew[x + y * world.width] = 1
        run = True
    world.world = worldNew
    #world.draw()

  count = 0
  for pos in range(len(world.world)):
    if (world.world[pos] == 2):
      count += 1
  return count


def runSecond(world):
  run = True
  while (run):
    run = False
    worldNew = world.world[:]
    for pos in range(len(world.world)):
      x = pos % world.width
      y = pos // world.width

      if (world.world[pos] == 1 and world.countVisible(x, y) == 0):
        worldNew[x + y * world.width] = 2
        run = True
      elif (world.world[pos] == 2 and world.countVisible(x, y) >= 5):
        worldNew[x + y * world.width] = 1
        run = True
    world.world = worldNew
    #world.draw()

  count = 0
  for pos in range(len(world.world)):
    if (world.world[pos] == 2):
      count += 1
  return count


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  world = World()
  for line in input:
    line = line.strip()
    world.width = len(line)
    for char in line:
      if (char == "L"):
        world.world.append(1)
      else:
        world.world.append(0)
    world.height += 1

  # result = runFirst(world)
  # print(result)
      
  world.reset()
  result = runSecond(world)
  print(result)

if (__name__ == "__main__"):
  main()