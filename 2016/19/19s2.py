def main():
  numberOfElves = 3018458
  elves = range(1, numberOfElves+1)
  elves[-1] = 0
  print(len(elves))
  
  elvesRest = numberOfElves
  index = 0
  lastIndex = index
  nextIndex = elves[index]
  for i in xrange(elvesRest / 2 - 1):
    lastIndex = nextIndex
    nextIndex = elves[nextIndex]

  while (elvesRest > 1):    
    elves[lastIndex] = elves[nextIndex]
    elves[nextIndex] = -1
    elvesRest -= 1
    index = elves[index]
    
    nextIndex = elves[lastIndex]
    if ((elvesRest % 2) == 0):
      lastIndex = nextIndex
      nextIndex = elves[lastIndex]
      
    #print(elves, index, lastIndex, nextIndex)
    
  print(index + 1)
    

if (__name__ == "__main__"):
  main()