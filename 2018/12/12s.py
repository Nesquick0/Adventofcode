def grow(plants, rules, pos):
  info = [0, 0, 0, 0, 0]
  for i in range(0, 5):
    if (pos + i - 2 in plants):
      info[i] = 1
  info = tuple(info)
  if (info in rules):
    return 1
  else:
    return 0


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
    
  initState = input[0].strip().split(": ")[1]

  plants = {}
  for i in range(len(initState)):
    if (initState[i] == "#"):
      plants[i] = 1

  rules = {}
  for line in input[2:]:
    rule, result = line.strip().split(" => ")
    if (result != "#"):
      continue
    rule = tuple(map(int, list(rule.replace(".", "0").replace("#", "1"))))
    rules[rule] = 1

  # Check for same pattern.
  oldStates = {}
  oldStates[tuple(sorted(plants.keys()))] = 1
  for gen in range(1, 50000000000+1): # Part 2
    checks = set()
    for pos in plants.keys():
      for j in range(5):
        checks.add(pos + j - 2)

    newPlants = {}
    for pos in checks:
      if (grow(plants, rules, pos)):
        newPlants[pos] = 1

    plants = newPlants

    # Print state
    minPos = min(plants.keys())
    maxPos = max(plants.keys())
    print("%d (%d):" % (gen, minPos))
    for pos in range(minPos, maxPos+1):
      print("#" if pos in plants else ".", end="")
    print("")

    state = tuple( map(lambda x: x-minPos, sorted(plants.keys())) )
    if (state in oldStates):
      # State never changes from this point. Just move to the right.
      restGen = 50000000000 - gen
      newPlants = {}
      for pos in plants:
        newPlants[pos + restGen] = 1
      plants = newPlants
      break
    else:
      oldStates[state] = 1

  result = 0
  for pos in plants:
    result += pos
  print(result)

  

if (__name__ == "__main__"):
  main()