class Train():
  def __init__(self):
    self.dir = 0
    self.lastJunc = -1

class Main():
  def __init__(self):
    self.trains = {}
    self.tracks = {}

  def printWorld(self):
    maxX = maxY = 0
    for track in self.tracks:
      maxX = max(maxX, track[0])
      maxY = max(maxY, track[1])

    for y in range(maxY+1):
      for x in range(maxX+1):
        if ( (x, y) in self.trains):
          train = self.trains[ (x, y) ]
          if (train.dir == 0):
            print("^", end="")
          elif (train.dir == 1):
            print(">", end="")
          elif (train.dir == 2):
            print("v", end="")
          elif (train.dir == 3):
            print("<", end="")
        elif ( (x, y) in self.tracks):
          print(".", end="")
        else:
          print(" ", end="")
      print("")
    print("")



  def run(self):
    with open("input.txt", "r") as file:
      input = file.readlines()

    # Load
    for y in range(len(input)):
      for x in range(len(input[y])):
        char = input[y][x]
        if ("-" == char or ">" == char or "<" == char):
          self.tracks[ (x, y) ] = [ (x-1, y), (x+1, y) ]
        elif ("|" == char or "^" == char or "v" == char):
          self.tracks[ (x, y) ] = [ (x, y-1), (x, y+1) ]
        elif ("/" == char):
          if (y>0 and (input[y-1][x] in "|+v^")):
            self.tracks[ (x, y) ] = [ (x-1, y), (x, y-1) ]
          else:
            self.tracks[ (x, y) ] = [ (x, y+1), (x+1, y) ]
        elif ("\\" == char):
          if (y>0 and (input[y-1][x] in "|+v^")):
            self.tracks[ (x, y) ] = [ (x+1, y), (x, y-1) ]
          else:
            self.tracks[ (x, y) ] = [ (x, y+1), (x-1, y) ]
        elif ("+" == char):
          self.tracks[ (x, y) ] = [ (x, y-1), (x, y+1), (x-1, y), (x+1, y) ]

        if (">" == char or "<" == char or "^" == char or "v" == char):
          train = Train()
          if (">" == char):
            train.dir = 1
          elif ("v" == char):
            train.dir = 2
          elif ("<" == char):
            train.dir = 3
          self.trains[ (x, y) ] = train

    #self.printWorld()

    # Move
    while True:
      trains = list(self.trains.keys())
      trains.sort(key=lambda x: x[0])
      trains.sort(key=lambda x: x[1])
      
      for trainPos in trains:
        train = self.trains[trainPos]
        if (train.dir == 0):
          nextPos = (trainPos[0], trainPos[1]-1)
        elif (train.dir == 1):
          nextPos = (trainPos[0]+1, trainPos[1])
        elif (train.dir == 2):
          nextPos = (trainPos[0], trainPos[1]+1)
        elif (train.dir == 3):
          nextPos = (trainPos[0]-1, trainPos[1])
        dirs = self.tracks[ nextPos ]

        # Move train to new pos
        if (nextPos in self.trains):
          print(nextPos)
          return
        del self.trains[trainPos]
        self.trains[ nextPos ] = train

        # Set new direction
        if (len(dirs) == 4): # Junction
          train.lastJunc = (train.lastJunc+1) % 3
          if (train.lastJunc == 0): # Left
            train.dir -= 1
            if (train.dir < 0):
              train.dir = 3
          elif (train.lastJunc == 2): # Right
            train.dir += 1
            if (train.dir > 3):
              train.dir = 0
          elif (train.lastJunc == 1): # Straight
            pass
        else:
          direction = dirs[1] if (dirs[0] == trainPos) else dirs[0]
          if (direction[0] < nextPos[0]):
            train.dir = 3
          elif (direction[0] > nextPos[0]):
            train.dir = 1
          elif (direction[1] < nextPos[1]):
            train.dir = 0
          elif (direction[1] > nextPos[1]):
            train.dir = 2

      #self.printWorld()
            
        


  

if (__name__ == "__main__"):
  Main().run()