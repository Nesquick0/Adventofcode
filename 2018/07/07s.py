def findPossible(steps, stepsFinished, workers):
  possible = []
  for step in steps:
    if (step in stepsFinished):
      continue
      
    workOn = False
    for worker in workers:
      if (worker and step == worker[0]):
        workOn = True
        break
    if (workOn):
      continue
      
    blockers = steps[step][1]
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
    
  print(ord("Z"))

  steps = {}
  for line in input:
    lineSplit = line.split(" ")
    s1, s2 = lineSplit[1], lineSplit[7]
    duration1 = ord(s1) - ord("A") + 1 + 60
    duration2 = ord(s2) - ord("A") + 1 + 60
    if (s1 not in steps):
      steps[s1] = [duration1, []]
    if (s2 not in steps):
      steps[s2] = [duration2, []]
    steps[s2][1].append( s1 )
    
  print(steps)
  stepsFinished = []
  
  seconds = 0
  workers = 5*[None]
  while len(steps) != len(stepsFinished):
    # Check if job finished
    for i in range(len(workers)):
      if (workers[i]):
        step, start = workers[i]
        if (seconds - start >= steps[step][0]):
          stepsFinished.append(step)
          workers[i] = None
  
    # Check avail workers
    workerAvail = []
    for i in range(len(workers)):
      if (not workers[i]):
        workerAvail.append(i)
        
    if (len(workerAvail) > 0):
      possible = findPossible(steps, stepsFinished, workers)
      possible.sort()
      while (len(workerAvail) > 0 and len(possible) > 0):
        step = possible.pop(0)
        worker = workerAvail.pop(0)
        workers[worker] = [step, seconds]
    
    print("% 5d - %40s - %s" % (seconds, workers, "".join(stepsFinished)))
    seconds += 1
    
  print("".join(stepsFinished))
  
  

if (__name__ == "__main__"):
  main()