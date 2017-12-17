def redistr(memory):
  nValues = len(memory)
  maxValue = max(memory)
  index = memory.index(maxValue)
  if ((maxValue % nValues) == 0):
    adder = maxValue // nValues
  else:
    adder = (maxValue // nValues) + 1
    
  newMemory = list(memory)
  newMemory[index] = 0
  index = (index+1)%nValues
  while (maxValue > 0):
    newMemory[index] += min(adder, maxValue)
    index = (index+1)%nValues
    maxValue -= adder
  
  return tuple(newMemory)
  

def main():
  with open("input", "r") as file:
    input = file.readline()
    input = tuple(map(int, input.strip().split("\t")))
    
  states = set()
  statesList = []
  counter = 0
    
  print(input)
  states.add(input)
  statesList.append(input)
  while (True):
    input = redistr(input)
    #print(input)
    counter += 1
    if (input in states):
      break
    else:
      states.add(input)
      statesList.append(input)
    
  # Part1
  print(counter)
  # Part2
  print(statesList.index(input))
  print(len(statesList) - statesList.index(input))
    
    
if (__name__ == "__main__"):
  main()