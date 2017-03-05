def is_digit(n):
  try:
    int(n)
    return True
  except ValueError:
    return False
   
   
def run(origA, commands):
  registers = {"a" : origA, "b" : 0, "c" : 0, "d" : 0}
  lastValue = 1
  testOutput = []
  
  index = 0
  while (index < len(commands)):
    line = commands[index]
    instr = line[0]
    if (instr == "cpy"):
      if (not is_digit(line[2])):
        if (is_digit(line[1])):
          registers[line[2]] = int(line[1])
        else:
          registers[line[2]] = registers[line[1]]
    elif (instr == "inc"):
      registers[line[1]] += 1
    elif (instr == "dec"):
      registers[line[1]] -= 1
    elif (instr == "jnz"):
      doJump = False
      if (is_digit(line[1])):
        if (int(line[1]) != 0):
          doJump = True
      else:
        if (registers[line[1]] != 0):
          doJump = True
          
      if (doJump):
        if (is_digit(line[2])):
          index += int(line[2]) - 1
        else:
          index += registers[line[2]] - 1
          
    elif (instr == "out"):
      if (is_digit(line[1])):
        value = int(line[1])
      else:
        value = registers[line[1]]
      
      if (not ( ((value == 1) and (lastValue == 0)) or ((value == 0) and (lastValue == 1)) ) ):
        return False
      else:
        testOutput.append(value)
        
      if (len(testOutput) >= 10):
        print("")
        print(origA, testOutput)
        testOutput = []
      lastValue = value
        
    #elif (instr == "tgl"): TGL not used in this program.
    
    index += 1
  return True

def main():
  with open("25.input", "r") as file:
    fileContent = file.readlines()
  
  # Prepare data in array.
  commands = []
  for line in fileContent:
    instr = line.strip().split()
    commands.append(instr)
  print(commands)
    
  origA = 0
  
  while True:
    print(origA),
    if (run(origA, commands)):
      break
    origA += 1
      
  print(origA)
    
if (__name__ == "__main__"):
  main()