def moveItem(floors, index, floorTo):
  newFloors = list(floors)
  newFloors[index] = floorTo
  return tuple(newFloors)

  
def success(floors, elevator):
  if (elevator != 3):
    return False
    
  for floor in floors:
    if (floor != 3):
      return False
      
  return True
    

def validate(floors, items, microchips, generators):
  genExist = [[], [], [], []]
  for index in generators:
    genExist[floors[index]].append(index)
          
  for index in microchips:
    floor = floors[index]
    if (not genExist[floor]):
      continue
      
    genFound = False
    for index2 in genExist[floor]:
      if (items[index][0] == items[index2][0]):
        genFound = True
        break
    if (not genFound):
      return False
      
  return True

  
def printFloors(floors, elevator, items):
  for floor in xrange(3, -1, -1):
    print("F%d" % (floor+1)),
    print("E" if (elevator == floor) else " "),
    for index, item in enumerate(items):
      if (floor == floors[index]):
        name = item[0]
        # Generator == 0, Microchip == 1.
        type = "G" if (item[1] == 0) else "M"
        print("%s%s" % (name, type)),
      
    print("")


def main():
  with open("11s.input", "r") as file:
    fileContent = file.readlines()
    
  # Items is list with description of items. It shouldn't change.
  items = []
  microchips = []
  generators = []
  itemIndex = 0
  # Floors is list of indexes where each index must have same position in floors and items. Number in floors is floor number.
  floors = []
  floorNumber = 0
  for line in fileContent:
    line = line.strip()
    words = line.split(" ")
    
    if ("nothing relevant" in line):
      continue
    else:
      for index, item in enumerate(words):
        if ("microchip" in item):
          name = words[index-1].split("-")[0][0:2].capitalize()
          items.append( (name, 1) )
          floors.append( floorNumber )
          microchips.append(itemIndex)
          itemIndex += 1
        elif ("generator" in item):
          name = words[index-1][0:2].capitalize()
          items.append( (name, 0) )
          floors.append( floorNumber )
          generators.append(itemIndex)
          itemIndex += 1
        
    floorNumber += 1
  items = tuple(items)
  floors = tuple(floors)
    
  # Test print.
  printFloors(floors, 0, items)
  print(validate(floors, items, microchips, generators))
  print(success(floors, 3))
  print("")
    
  # Try to find solution. State is (floors, elevator).
  states = [ (floors, 0, 0) ]
  visited = set( (floors, 0) )
  lastStep = 0
  
  while (len(states) > 0):
    state = states.pop(0)
    floors, elevator, steps = state
    if (lastStep < steps):
      lastStep = steps
      print(lastStep, len(states), len(visited))
      
    if (success(floors, elevator)):
      break
    
    for index, floor in enumerate(floors):
      if (floor != elevator):
        continue
        
      if (elevator < 3):
        # Create state when moving one item.
        newFloors = moveItem(floors, index, elevator+1)

        newState = (newFloors, elevator+1)
        if (validate(newFloors, items, microchips, generators) and newState not in visited):
          visited.add(newState)
          states.append( (newFloors, elevator+1, steps+1) )
          
        # Create state when moving two items.
        for index2, floor2 in enumerate(floors):
          if (floor2 != elevator):
            continue
          newFloors2 = moveItem(newFloors, index2, elevator+1)

          newState = (newFloors2, elevator+1)
          if (validate(newFloors2, items, microchips, generators) and newState not in visited):
            visited.add(newState)
            states.append( (newFloors2, elevator+1, steps+1) )
          
      if (elevator > 0):
        # Create state when moving one item.
        newFloors = moveItem(floors, index, elevator-1)

        newState = (newFloors, elevator-1)
        if (validate(newFloors, items, microchips, generators) and newState not in visited):
          visited.add(newState)
          states.append( (newFloors, elevator-1, steps+1) )
          
        # Create state when moving two items.
        for index2, floor2 in enumerate(floors):
          if (floor2 != elevator):
            continue
          newFloors2 = moveItem(newFloors, index2, elevator-1)

          newState = (newFloors2, elevator-1)
          if (validate(newFloors2, items, microchips, generators) and newState not in visited):
            visited.add(newState)
            states.append( (newFloors2, elevator-1, steps+1) )
    
    
  printFloors(floors, elevator, items)
  print("Steps: %d" % (steps))
  print("Success {}".format(success(floors, elevator)))
  print("")
  
  
if (__name__ == "__main__"):
  main()