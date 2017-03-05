def main():
  with open("15.input", "r") as file:
    fileContent = file.readlines()
    
  currPos = []
  maxPos = []
  for line in fileContent:
    parts = line.strip().split(" ")
    maxPos.append(int(parts[3]))
    currPos.append(int(parts[11].split(".")[0]))
    
  print(currPos)
  print(maxPos)
  
  targetPos = []
  for i in xrange(len(currPos)):
    target = (-1 - i) % maxPos[i]
    targetPos.append(target)
  
  print(targetPos)
  startTime = 0
  while True:
    targetFound = True
    for i in xrange(len(currPos)):
      pos = (currPos[i] + startTime) % maxPos[i]
      if (pos != targetPos[i]):
        targetFound = False
        break
        
    if (targetFound):
      break
      
    startTime += 1
    
  print(startTime)

if (__name__ == "__main__"):
  main()