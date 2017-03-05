def is_digit(n):
  try:
    int(n)
    return True
  except ValueError:
    return  False

def main():
  with open("23.input", "r") as file:
    fileContent = file.readlines()
    
  registers = {"a" : 12, "b" : 0, "c" : 0, "d" : 0}
  
  # Prepare data in array.
  commands = []
  for line in fileContent:
    instr = line.strip().split()
    commands.append(instr)
  print(commands)
  
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
        
    elif (instr == "tgl"):
      if (is_digit(line[1])):
        offset = int(line[1])
      else:
        offset = registers[line[1]]
        
      # Convert instruction.
      tglIndex = index + offset
      if ((tglIndex >= 0) and (tglIndex < len(commands))):
        if (len(commands[tglIndex]) == 2):
          if (commands[tglIndex][0] == "inc"):
            commands[tglIndex][0] = "dec"
          else:
            commands[tglIndex][0] = "inc"
        elif (len(commands[tglIndex]) == 3):
          if (commands[tglIndex][0] == "jnz"):
            commands[tglIndex][0] = "cpy"
          else:
            commands[tglIndex][0] = "jnz"
      print("tgl", tglIndex)
      print(commands)
      print(registers)
      print("")
    
    index += 1
      
      
  print(registers)
  # Looks like program calculate "factorial of number" + 6643 (don't know why this number).
    
if (__name__ == "__main__"):
  main()