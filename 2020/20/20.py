import math

class Tile():
  def __init__(self):
    self.width = 0
    self.data = []
    self.borders1 = [0, 0, 0, 0]
    self.borders2 = [0, 0, 0, 0]
    self.numBorders = 0
    self.next = [-1, -1, -1, -1] # Top, Right, Down, Left in some order
    self.id = 0
    self.rotate = 0
    self.flip = False

  def getData(self):
    # Flip
    data = []
    if (self.flip):
      data = [0]*len(self.data)
      for i in range(len(self.data)):
        x = i % self.width
        y = i // self.width
        data[i] = self.data[y + x*self.width]
    else:
      data = self.data[:]

    # Rotate
    data2 = [0]*len(self.data)
    for i in range(len(self.data)):
      x = i % self.width
      y = i // self.width
      for r in range(self.rotate):
        a = x
        b = y
        x = (-b-1)%self.width
        y = a
      data2[x+y*self.width] = data[i]

    # print("======== {}".format(self.id))
    # for i in range(self.width):
    #   print(self.data[i*self.width:(i+1)*self.width])
    # print("")
    # for i in range(self.width):
    #   print(data[i*self.width:(i+1)*self.width])
    # print("")
    # for i in range(self.width):
    #   print(data2[i*self.width:(i+1)*self.width])
    # print("========")

    return data2


  def findRotFlip(self, topId, leftId, tilesDict):
    # Just rotate
    for i in range(4):
      if ((self.next[-i:] + self.next[:-i])[0] == topId and (self.next[-i:] + self.next[:-i])[3] == leftId):
        self.rotate = i
        self.next = self.next[-i:] + self.next[:-i]
        self.borders1 = self.borders1[-i:] + self.borders1[:-i]
        self.borders2 = self.borders2[-i:] + self.borders2[:-i]
        return
    # Flip and rotate
    for i in range(4):
      if ((self.next[i:] + self.next[:i])[3] == topId and (self.next[i:] + self.next[:i])[0] == leftId):
        self.rotate = i
        self.flip = True
        self.next.reverse()
        self.next = self.next[-i:] + self.next[:-i]

        self.borders1.reverse()
        self.borders1 = self.borders1[-i:] + self.borders1[:-i]

        self.borders2.reverse()
        self.borders2 = self.borders2[-i:] + self.borders2[:-i]
        return


def runFirst(tiles):
  for tile in tiles:
    # Top, right, bottom, left and other way
    for i in range(0, tile.width):
      #print(tile.data[i], end="")
      #print(tile.data[tile.width-1 + i*tile.width], end="")
      #print(tile.data[tile.width-1-i + (tile.width-1)*tile.width], end="")
      #print(tile.data[(tile.width-1-i)*tile.width], end="")
      if (tile.data[i] == 1):
        tile.borders1[0] += 2**i
      if (tile.data[tile.width-1 + i*tile.width] == 1):
        tile.borders1[1] += 2**i
      if (tile.data[tile.width-1-i + (tile.width-1)*tile.width] == 1):
        tile.borders1[2] += 2**i
      if (tile.data[(tile.width-1-i)*tile.width] == 1):
        tile.borders1[3] += 2**i
    for i in range(0, tile.width):
      if (tile.data[i] == 1):
        tile.borders2[0] += 2**(tile.width-1-i)
      if (tile.data[tile.width-1 + i*tile.width] == 1):
        tile.borders2[1] += 2**(tile.width-1-i)
      if (tile.data[tile.width-1-i + (tile.width-1)*tile.width] == 1):
        tile.borders2[2] += 2**(tile.width-1-i)
      if (tile.data[(tile.width-1-i)*tile.width] == 1):
        tile.borders2[3] += 2**(tile.width-1-i)
    
  # Find borders in other tiles
  for tile in tiles:
    num = 0
    for border in (tile.borders1 + tile.borders2):
      for tileOther in tiles:
        if (tile != tileOther):
          if (border in (tileOther.borders1 + tileOther.borders2)):
            num += 1
            if (border in tile.borders1):
              tile.next[tile.borders1.index(border)] = tileOther.id
            elif (border in tile.borders2):
              tile.next[tile.borders2.index(border)] = tileOther.id
            break
    if (num % 2 != 0):
      print(tile.id)
    tile.numBorders = num // 2
  
  result = 1
  for tile in tiles:
    if (tile.numBorders == 2):
      result *= tile.id
  return result


def runSecond(tiles):
  monsterImg =  "                  # \n"
  monsterImg += "#    ##    ##    ###\n"
  monsterImg += " #  #  #  #  #  #   "
  monster = []
  monsterImg = monsterImg.split("\n")
  for y in range(len(monsterImg)):
    for x in range(len(monsterImg[y])):
      if (monsterImg[y][x] == "#"):
        monster.append([x, y])
  monsterMaxY = len(monsterImg)
  monsterMaxX = len(monsterImg[0])

  tilesDict = {}
  for tile in tiles:
    tilesDict[tile.id] = tile

  # Find corner.
  cornerId = 0
  for tile in tiles:
    if (tile.numBorders == 2):
      cornerId = tile.id

  gridSize = int(math.sqrt(len(tiles)))
  grid = [0]*(gridSize*gridSize)
  if (len(tiles) != gridSize*gridSize):
    print("Error!")

  grid[0] = cornerId
  for i in range(gridSize*gridSize):
    topId = -1
    leftId = -1
    x = i % gridSize
    y = i // gridSize
    if (x > 0):
      leftId = grid[(x-1) + y*gridSize]
    if (y > 0):
      topId = grid[x + (y-1)*gridSize]
    tileId = grid[i]
    tilesDict[tileId].findRotFlip(topId, leftId, tilesDict)
    if (x < (gridSize-1)):
      grid[(x+1) + y*gridSize] = tilesDict[tileId].next[1]
    if (y < (gridSize-1)):
      grid[x + (y+1)*gridSize] = tilesDict[tileId].next[2]

  # Prepare data to whole image (without borders).
  tileWidthWB = tilesDict[cornerId].width-2
  imgWidth = tileWidthWB*gridSize
  img = [0]*(imgWidth*imgWidth)
  for i in range(len(grid)):
    x = i % gridSize
    y = i // gridSize
    tile = tilesDict[grid[i]]
    data = tile.getData()
    for datay in range(0, tileWidthWB):
      for datax in range(0, tileWidthWB):
        img[x*tileWidthWB+datax + (y*tileWidthWB+datay)*imgWidth] = data[datax+1+(datay+1)*tile.width]

  # Draw
  # for y in range(imgWidth):
  #   # if (y % 10 == 0 and y != 0):
  #   #   print("")
  #   for x in range(imgWidth):
  #     # if (x % 10 == 0 and x != 0):
  #     #   print(" ", end="")
  #     if (img[x+y*imgWidth] == 1):
  #       print("#", end="")
  #     else:
  #       print(".", end="")
  #   print("")

  # Try to find monster for 4 rotations before and after flip.
  imgTile = Tile()
  imgTile.data = img[:]
  imgTile.width = imgWidth

  maxMonsters = 0
  for i in range(8):
    if (i < 4):
      imgTile.rotate = i
      imgTile.flip = False
    else:
      imgTile.rotate = i - 4
      imgTile.flip = True

    data = imgTile.getData()
    # Count monsters.
    monstersCount = 0
    for y in range(imgTile.width-monsterMaxY):
      for x in range(imgTile.width-monsterMaxX):
        found = True
        for m in monster:
          if (data[(x+m[0])+(y+m[1])*imgTile.width] != 1):
            found = False
            break
        if (found):
          monstersCount += 1
    maxMonsters = max(maxMonsters, monstersCount)
    print(monstersCount, end=" ")
  print(maxMonsters)

  notMonsterCount = 0
  for i in range(len(imgTile.data)):
    if (imgTile.data[i] == 1):
      notMonsterCount += 1
  notMonsterCount -= maxMonsters * len(monster)
    # Draw
    # print("\n============================================ {}".format(i))
    # for y in range(imgTile.width):
    #   for x in range(imgTile.width):
    #     if (data[x+y*imgTile.width] == 1):
    #       print("#", end="")
    #     else:
    #       print(".", end="")
    #   print("")
  return notMonsterCount


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  tiles = []
  tile = None
  for line in input:
    line = line.strip()
    if (not line):
      continue

    if ("Tile" in line):
      tile = Tile()
      tiles.append(tile)
      tile.id = int(line[5:-1])
    else:
      tile.width = len(line)
      for char in line:
        if (char == "#"):
          tile.data.append(1)
        else:
          tile.data.append(0)

  result = runFirst(tiles)
  print(result)
  
  result = runSecond(tiles)
  print(result)


if (__name__ == "__main__"):
  main()