def main():
  with open("12.input", "r") as file:
    fileContent = file.readlines()
    
  registers = {"a" : 0, "b" : 0, "c" : 1, "d" : 0}
  
  index = 0
  while (index < len(fileContent)):
    line = fileContent[index].split()
    instr = line[0]
    if (instr == "cpy"):
      if (line[1].isdigit()):
        registers[line[2]] = int(line[1])
      else:
        registers[line[2]] = registers[line[1]]
    elif (instr == "inc"):
      registers[line[1]] += 1
    elif (instr == "dec"):
      registers[line[1]] -= 1
    elif (instr == "jnz"):
      doJump = False
      if (line[1].isdigit()):
        if (int(line[1]) != 0):
          doJump = True
      else:
        if (registers[line[1]] != 0):
          doJump = True
          
      if (doJump):
        index += int(line[2]) - 1
    
    index += 1
      
      
  print(registers)
    
if (__name__ == "__main__"):
  main()