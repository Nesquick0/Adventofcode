def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  instructions = []
  for line in input:
    if (line):
      instructions.append(int(line.strip()))
      
  print(instructions)
  
  steps = 0
  pointer = 0
  while (True):
    if (pointer >= len(instructions)):
      break
    instr = instructions[pointer]
    if (instr >= 3):
      instructions[pointer] -= 1
    else:
      instructions[pointer] += 1
    pointer = pointer + instr
    steps += 1
    
  print(steps)
  
  
if (__name__ == "__main__"):
  main()