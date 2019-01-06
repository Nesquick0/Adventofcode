# Goblin = 9, Elf = 5

class Main():
  def __init__(self):
    self.world = []
    self.worldOrig = []
    self.maxX = 0
    self.maxY = 0
    self.elves = {}
    self.goblins = {}
    self.goblinAtk = 0
    self.elfAtk = 0
    self.startHp = 0


  def findTarget(self, unit):
    start = (unit[0], unit[1])
    history = [ (start[0], start[1], -1) ]
    checked = set( (start[0], start[1]) )
    i = 0
    while (i<len(history)):
      pos = history[i]
      x, y = pos[0], pos[1]

      if (self.checkNextToEnemy((x, y, unit[2]))):
        # Found target, find first step
        firstStep = pos
        while firstStep[2] != 0:
          firstStep = history[ firstStep[2] ]
        return (firstStep[0], firstStep[1])

      if (self.world[(x) + self.maxX*(y-1)] == 1):
        if ( (x, y-1) not in checked ):
          history.append( (x, y-1, i) )
          checked.add( (x, y-1) )
      if (self.world[(x-1) + self.maxX*(y)] == 1):
        if ( (x-1, y) not in checked ):
          history.append( (x-1, y, i) )
          checked.add( (x-1, y) )
      if (self.world[(x+1) + self.maxX*(y)] == 1):
        if ( (x+1, y) not in checked ):
          history.append( (x+1, y, i) )
          checked.add( (x+1, y) )
      if (self.world[(x) + self.maxX*(y+1)] == 1):
        if ( (x, y+1) not in checked ):
          history.append( (x, y+1, i) )
          checked.add( (x, y+1) )

      i += 1

    return None


  def checkNextToEnemy(self, unit):
    x, y = unit[0], unit[1]
    if (unit[2] == 9):
      if (self.world[(x) + self.maxX*(y-1)] == 5):
        return (x, y-1)
      if (self.world[(x-1) + self.maxX*(y)] == 5):
        return (x-1, y)
      if (self.world[(x+1) + self.maxX*(y)] == 5):
        return (x+1, y)
      if (self.world[(x) + self.maxX*(y+1)] == 5):
        return (x, y+1)
    else:
      if (self.world[(x) + self.maxX*(y-1)] == 9):
        return (x, y-1)
      if (self.world[(x-1) + self.maxX*(y)] == 9):
        return (x-1, y)
      if (self.world[(x+1) + self.maxX*(y)] == 9):
        return (x+1, y)
      if (self.world[(x) + self.maxX*(y+1)] == 9):
        return (x, y+1)

    return None


  def pickEnemy(self, unit):
    minHp = self.startHp+1
    target = None

    x, y = unit[0], unit[1]
    if (unit[2] == 9):
      enemy = 5
      enemyDict = self.elves
    else:
      enemy = 9
      enemyDict = self.goblins

    tests = [ (x, y-1), (x-1, y), (x+1, y), (x, y+1) ]

    for test in tests:
      if (self.world[(test[0]) + self.maxX*(test[1])] == enemy):
        enemyHp = enemyDict[ (test[0], test[1]) ]
        if (enemyHp < minHp ):
          target = (test[0], test[1])
          minHp = enemyHp

    # Attack
    enemyDict[ target ] -= (self.goblinAtk if (unit[2] == 9) else self.elfAtk)
    if (enemyDict[ target ] <= 0): # Died
      del enemyDict[ target ]
      self.world[(target[0]) + self.maxX*(target[1])] = 1
    return target


  def printWorld(self):
    line = ""
    units = ""
    for i in range(len(self.world)):
      x = i%self.maxX
      y = i//self.maxY

      if (x == 0 and y != 0):
        print("{} {}".format(line, units))
        line = units = ""
      if (self.world[i] == 0):
        line += "#"
      elif (self.world[i] == 1):
        line += "."
      elif (self.world[i] == 9):
        line += "G"
        units += "G({}), ".format(self.goblins[ (x, y) ])
      elif (self.world[i] == 5):
        line += "E"
        units += "E({}), ".format(self.elves[ (x, y) ])


  def simulate(self, keepElves):
    self.elves = {}
    self.goblins = {}
    for i in range(len(self.world)):
      x = i%self.maxX
      y = i//self.maxY
      if (self.world[i] == 9):
        self.goblins[ (x, y) ] = self.startHp
      elif (self.world[i] == 5):
        self.elves[ (x, y) ] = self.startHp

    #self.printWorld()

    roundId = 0
    nElves = len(self.elves)

    while True:
      units = []
      fullRound = True
      for i in range(len(self.world)):
        x = i%self.maxX
        y = i//self.maxY
        if (self.world[i] == 9):
          units.append( (x, y, 9) )
          #unit = (x, y, 9)
        elif (self.world[i] == 5):
          units.append( (x, y, 5) )
          #unit = (x, y, 5)
        else:
          continue
      
      for unit in units:
        if (unit[2] != 5 and unit[2] != 9):
          continue
        if (unit[2] == 5 and (unit[0], unit[1]) not in self.elves):
          continue
        if (unit[2] == 9 and (unit[0], unit[1]) not in self.goblins):
          continue

        # Check if some enemy still exist
        if (unit[2] == 9):
          if (len(self.elves) == 0):
            fullRound = False
            break
        else:
          if (len(self.goblins) == 0):
            fullRound = False
            break

        # Attack if next to enemy.
        nextToEnemy =self.checkNextToEnemy(unit)
        if (nextToEnemy):
          self.pickEnemy(unit)
          continue # Don't move

        target = self.findTarget(unit)
        # Move
        if (target):
          self.world[(unit[0]) + self.maxX*(unit[1])] = 1
          self.world[(target[0]) + self.maxX*(target[1])] = unit[2]
          if (unit[2] == 9):
            self.goblins[ (target[0], target[1]) ] = self.goblins[ (unit[0], unit[1]) ]
            del self.goblins[ (unit[0], unit[1]) ]
          else:
            self.elves[ (target[0], target[1]) ] = self.elves[ (unit[0], unit[1]) ]
            del self.elves[ (unit[0], unit[1]) ]

          # Attack after move.
          nextToEnemy =self.checkNextToEnemy( (target[0], target[1], unit[2]) )
          if (nextToEnemy):
            self.pickEnemy( (target[0], target[1], unit[2]) )

      if (len(self.elves) != nElves): # Elf was killed
        return (roundId, False)
      if (fullRound):
        roundId += 1
      #print("")
      #print(roundId)
      #self.printWorld()
      if (len(self.elves) == 0 or len(self.goblins) == 0):
        break
    
    return (roundId, True)


  def run(self):
    with open("input.txt", "r") as file:
      input = file.readlines()

    self.goblinAtk = 3
    self.elfAtk = 3
    self.startHp = 200

    self.maxY = len(input)
    for line in input:
      line = line.strip()
      self.maxX = len(line)
      for char in line:
        if (char == "#"):
          self.world.append(0)
        elif (char == "."):
          self.world.append(1)
        elif (char == "G"):
          self.world.append(9)
        elif (char == "E"):
          self.world.append(5)
    self.worldOrig = self.world[:]

    # Part 1
    roundId, result = self.simulate(False)
    #print("")
    #self.printWorld()
    print(roundId)
    sumHp = 0
    if (len(self.elves) > 0):
      sumHp = sum(self.elves.values())
    else:
      sumHp = sum(self.goblins.values())
    print(sumHp)
    print(roundId * sumHp)

    # Part 2

    while True:
      # Reset state
      self.elfAtk += 1
      self.world = self.worldOrig[:]
      roundId, result = self.simulate(True)
      print(self.elfAtk, end=" ")
      if (result):
        break

    print(roundId)
    sumHp = sum(self.elves.values())
    print(sumHp)
    print(roundId * sumHp)
      

if (__name__ == "__main__"):
  Main().run()