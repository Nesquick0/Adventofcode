def processInput(origInput):
  input = []
  for cmd in origInput:
    if (cmd[0] == "s"):
      value = int(cmd[1:])
      input.append( (1, value) )
    elif (cmd[0] == "x"):
      values = list(map(int, cmd[1:].split("/")))
      input.append( (2, values[0], values[1]) )
    elif (cmd[0] == "p"):
      names = cmd[1:].split("/")
      input.append( (3, names[0], names[1]) )
  return input

  
def dance(progs, input):
  for cmd in input:
    if (cmd[0] == 1):
      progs = progs[-cmd[1]:] + progs[:-cmd[1]]
    elif (cmd[0] == 2):
      swappers = (progs[cmd[1]], progs[cmd[2]])
      progs[cmd[1]], progs[cmd[2]] = swappers[1], swappers[0]
    elif (cmd[0] == 3):
      indices = (progs.index(cmd[1]), progs.index(cmd[2]))
      progs[indices[0]], progs[indices[1]] = progs[indices[1]], progs[indices[0]]
        
  return progs
  

def main():
  with open("input", "r") as file:
    input = file.readline().strip().split(",")
    
  input = processInput(input)
    
  count = 16
  progs = []
  for i in range(count):
    progs.append(chr(ord("a")+i))
    
  print("".join(progs))
  
  # Part 1
  progs1 = dance(progs[:], input)
  print("".join(progs1))
  
  # Part 2
  # progs2 = progs1[:]
  # targetIndices = progs[:]
  # for i in range(count):
    # targetIndices[i] = progs1.index(targetIndices[i])
  
  # # Repeat dances.
  # for nDances in range(1):
    # progs2New = progs2[:]
    # for i in range(count):
      # progs2New[i] = progs2[targetIndices[i]]
    # print(targetIndices)
    # progs2 = progs2New
    
  # print("".join(progs2))
  # progs3 = dance(progs1[:], input)
  # print("".join(progs3))
  
  progs2 = progs[:]
  for i in range(50):
    progs2 = dance(progs2[:], input)
    
  print("".join(progs2))
  
    
    
if (__name__ == "__main__"):
  main()