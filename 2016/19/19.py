def main():
  numberOfElves = 3018458
  elves = range(1, numberOfElves+1)
  elves[-1] = 0
  print(len(elves))
  
  index = 0
  nextIndex = 1
  
  while (index != nextIndex):
    nextIndex = index + 1
    if (nextIndex >= len(elves)):
      nextIndex = 0
    while (elves[nextIndex] == -1):
      nextIndex += 1
      if (nextIndex >= len(elves)):
        nextIndex = 0
        
    elves[index] = elves[nextIndex]
    elves[nextIndex] = -1
    index = elves[index]
    nextIndex = elves[index]
    
  print(index+1)
    

if (__name__ == "__main__"):
  main()