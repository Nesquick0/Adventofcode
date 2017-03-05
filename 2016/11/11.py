def copyState(floors):
  newFloors = []
  for floor in floors:
    newFloors.append(frozenset(floor))
  return tuple(newFloors)
  
  
def moveItem(floors, floorFrom, floorTo, item):
  newFloors = []
  for index, floor in enumerate(floors):
    if (index == floorFrom):
      newFloor = set(floor)
      newFloor.remove(item)
      newFloors.append(frozenset(newFloor))
    elif (index == floorTo):
      newFloor = set(floor)
      newFloor.add(item)
      newFloors.append(frozenset(newFloor))
    else:
      newFloors.append(frozenset(floor))
  
  return tuple(newFloors)

  
def success(floors, elevator):
  if (elevator != 3):
    return False
    
  for index in range(0, len(floors) - 1):
    if (floors[index]):
      return False
      
  return True
    

def validate(floors):
  for floor in floors:
    genExist = False
    for item in floor:
      if (item[1] == 0):
        genExist = True
        break
        
    # If there isn't any generator no need to check.
    if (not genExist):
      continue
      
    # Check that every microchip has generator connected.
    for item in floor:
      if (item[1] == 1):
        genFound = False
        for item2 in floor:
          if ((item2[1] == 0) and (item[0] == item2[0])):
            genFound = True
            break
            
        if (not genFound):
          return False
      
  return True

  
def printFloors(floors, elevator):
  for index, floor in reversed(list(enumerate(floors))):
    print("F%d" % (index+1)),
    print("E" if (elevator == index) else " "),
    for item in floor:
      name = item[0]
      # Generator == 0, Microchip == 1.
      type = "G" if (item[1] == 0) else "M"
      print("%s%s" % (name, type)),
      
    print("")


def main():
  with open("11.input", "r") as file:
    fileContent = file.readlines()
    
  floors = []
  for line in fileContent:
    line = line.strip()
    words = line.split(" ")
    floor = set()
    
    if ("nothing relevant" in line):
      floors.append(frozenset(floor))
      continue
      
    for index, item in enumerate(words):
      if ("microchip" in item):
        name = words[index-1].split("-")[0]
        floor.add( (name[0:2].capitalize(), 1) )
      elif ("generator" in item):
        floor.add( (words[index-1][0:2].capitalize(), 0) )
        
    floors.append(frozenset(floor))
  floors = tuple(floors)
    
  # Test print.
  printFloors(floors, 0)
  print(validate(floors))
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
    
    for item in floors[elevator]:
      if (elevator < 3):
        # Create state when moving one item.
        newFloors = moveItem(floors, elevator, elevator+1, item)

        newState = (newFloors, elevator+1)
        if (validate(newFloors) and newState not in visited):
          visited.add(newState)
          states.append( (newFloors, elevator+1, steps+1) )
          
        # Create state when moving two items.
        for item2 in newFloors[elevator]:
          newFloors2 = moveItem(newFloors, elevator, elevator+1, item2)

          newState = (newFloors2, elevator+1)
          if (validate(newFloors2) and newState not in visited):
            visited.add(newState)
            states.append( (newFloors2, elevator+1, steps+1) )
          
      if (elevator > 0):
        # Create state when moving one item.
        newFloors = moveItem(floors, elevator, elevator-1, item)

        newState = (newFloors, elevator-1)
        if (validate(newFloors) and newState not in visited):
          visited.add(newState)
          states.append( (newFloors, elevator-1, steps+1) )
          
        # Create state when moving two items.
        for item2 in newFloors[elevator]:
          newFloors2 = moveItem(newFloors, elevator, elevator-1, item2)

          newState = (newFloors2, elevator-1)
          if (validate(newFloors2) and newState not in visited):
            visited.add(newState)
            states.append( (newFloors2, elevator-1, steps+1) )
    
    
  printFloors(state[0], state[1])
  print("Steps: %d" % (state[2]))
  print("Success {}".format(success(floors, elevator)))
  print("")
  
  
if (__name__ == "__main__"):
  main()