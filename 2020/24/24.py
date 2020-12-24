def runFirst(paths):
  blacks = {}
  for path in paths:
    pos = [0, 0]
    for dir in path:
      if (dir == "e"):
        pos[0] += 1
      elif (dir == "w"):
        pos[0] -= 1
      elif (dir == "se"):
        pos[0] += 1
        pos[1] -= 1
      elif (dir == "sw"):
        pos[1] -= 1
      elif (dir == "ne"):
        pos[1] += 1
      elif (dir == "nw"):
        pos[0] -= 1
        pos[1] += 1
    pos = tuple(pos)
    if (pos not in blacks):
      blacks[pos] = 0
    blacks[pos] += 1
  
  count = 0
  for pos in blacks:
    if (blacks[pos] % 2 == 1):
      count += 1
  return count, set(filter(lambda x: blacks[x] % 2 == 1, blacks))


def getNear(pos):
  near = []
  near.append( (pos[0]+1, pos[1]  ) )
  near.append( (pos[0]+1, pos[1]-1) )
  near.append( (pos[0]  , pos[1]-1) )
  near.append( (pos[0]-1, pos[1]  ) )
  near.append( (pos[0]-1, pos[1]+1) )
  near.append( (pos[0]  , pos[1]+1) )
  return near


def countNear(pos, tiles):
  count = 0
  for near in getNear(pos):
    if (near in tiles):
      count += 1
  return count

def runSecond(blacksOrig):
  blacks = set(blacksOrig)
  for i in range(100):
    blacksNew = set()
    for pos in blacks:
      for near in getNear(pos) + [pos]:
        if (near in blacks): # is black
          count = countNear(near, blacks)
          if (count == 1 or count == 2):
            blacksNew.add(near)
        else: # is white
          count = countNear(near, blacks)
          if (count == 2):
            blacksNew.add(near)

    blacks = set(blacksNew)

  return len(blacks)


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  paths = []
  for line in input:
    line = line.strip()
    # e, se, sw, w, nw, ne
    path = []
    lastDir = ""
    for char in line:
      if (char == "e"):
        lastDir += "e"
        path.append(lastDir)
        lastDir = ""
      elif (char == "w"):
        lastDir += "w"
        path.append(lastDir)
        lastDir = ""
      elif (char == "n"):
        lastDir = "n"
      elif (char == "s"):
        lastDir = "s"
      else:
        print(char)
    paths.append(path)

  result = runFirst(paths)
  print(result[0])
  
  result = runSecond(result[1])
  print(result)


if (__name__ == "__main__"):
  main()
