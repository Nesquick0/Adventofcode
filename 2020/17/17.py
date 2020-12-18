class World():
  def __init__(self):
    self.world = {}

  def getNear(self, xs, ys, zs):
    near = 0
    for x in range(-1, 2):
      for y in range(-1, 2):
        for z in range(-1, 2):
          if (x != 0 or y != 0 or z != 0):
            pos = (xs + x, ys + y, zs + z)
            if (pos in self.world):
              near += 1
    return near

  def draw(self):
    minmax = [0, 0, 0, 0, 0, 0]
    for pos in self.world:
      minmax[0] = min(minmax[0], pos[0])
      minmax[1] = max(minmax[1], pos[0])
      minmax[2] = min(minmax[2], pos[1])
      minmax[3] = max(minmax[3], pos[1])
      minmax[4] = min(minmax[4], pos[2])
      minmax[5] = max(minmax[5], pos[2])
    
    for z in range(minmax[4], minmax[5]+1):
      print("\nz={}".format(z))
      for y in range(minmax[2], minmax[3]+1):
        for x in range(minmax[0], minmax[1]+1):
            pos = (x, y, z)
            if (pos in self.world):
              print("#", end="")
            else:
              print(".", end="")
        print("")


class World4D():
  def __init__(self):
    self.world = {}

  def getNear(self, xs, ys, zs, ws):
    near = 0
    for w in range(-1, 2):
      for x in range(-1, 2):
        for y in range(-1, 2):
          for z in range(-1, 2):
            if (x != 0 or y != 0 or z != 0 or w != 0):
              pos = (xs + x, ys + y, zs + z, ws + w)
              if (pos in self.world):
                near += 1
    return near


def runFirst(world):
  for c in range(6):
    newWorld = {}

    for pos in world.world:
      for x in range(-1, 2):
        for y in range(-1, 2):
          for z in range(-1, 2):
            checkPos = (pos[0] + x, pos[1] + y, pos[2] + z)
            if (checkPos not in newWorld):
              near = world.getNear(checkPos[0], checkPos[1], checkPos[2])
              if (checkPos in world.world): # Active
                if (near == 2 or near == 3):
                  newWorld[checkPos] = 1
                else:
                  newWorld[checkPos] = 0
              else: # Inactive
                if (near == 3):
                  newWorld[checkPos] = 1
                else:
                  newWorld[checkPos] = 0

    world.world = dict(filter(lambda x: x[1] == 1, newWorld.items()))
    #print("\nAfter cycle {}".format(c+1))
    #world.draw()
  return len(world.world)


def runSecond(world4D):
  for c in range(6):
    newWorld = {}

    for pos in world4D.world:
      for w in range(-1, 2):
        for x in range(-1, 2):
          for y in range(-1, 2):
            for z in range(-1, 2):
              checkPos = (pos[0] + x, pos[1] + y, pos[2] + z, pos[3] + w)
              if (checkPos not in newWorld):
                near = world4D.getNear(checkPos[0], checkPos[1], checkPos[2], checkPos[3])
                if (checkPos in world4D.world): # Active
                  if (near == 2 or near == 3):
                    newWorld[checkPos] = 1
                  else:
                    newWorld[checkPos] = 0
                else: # Inactive
                  if (near == 3):
                    newWorld[checkPos] = 1
                  else:
                    newWorld[checkPos] = 0

    world4D.world = dict(filter(lambda x: x[1] == 1, newWorld.items()))
  return len(world4D.world)


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  world = World()
  world4D = World4D()
  for y in range(len(input)):
    if (input[y]):
      for x in range(len(input[y].strip())):
        if (input[y][x] == "#"):
          world.world[(x, y, 0)] = 1
          world4D.world[(x, y, 0, 0)] = 1

  #world.draw()

  result = runFirst(world)
  print(result)
  
  result = runSecond(world4D)
  print(result)


if (__name__ == "__main__"):
  main()