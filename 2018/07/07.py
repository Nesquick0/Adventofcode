def findPossible(steps, stepsFinished):
  possible = []
  for step in steps:
    if (step in stepsFinished):
      continue
    blockers = steps[step]
    allDone = True
    for blocker in blockers:
      if (blocker not in stepsFinished):
        allDone = False
    
    if (allDone):
      possible.append(step)
  return possible

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  # Step C must be finished before step A can begin.
  steps = {}
  for line in input:
    lineSplit = line.split(" ")
    s1, s2 = lineSplit[1], lineSplit[7]
    if (s2 not in steps):
      steps[s2] = []
    if (s1 not in steps):
      steps[s1] = []
    steps[s2].append(s1)
    
  print(steps)
  stepsFinished = []
  
  while len(steps) != len(stepsFinished):
    possible = findPossible(steps, stepsFinished)
    possible.sort()
    stepsFinished.append(possible[0])
    
  print("".join(stepsFinished))
  
  

if (__name__ == "__main__"):
  main()