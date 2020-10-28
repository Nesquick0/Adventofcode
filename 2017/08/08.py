from collections import defaultdict

def doAction(registers, register, action, value):
  if (action == "inc"):
    registers[register] += value
  elif (action == "dec"):
    registers[register] -= value
  else:
    print("Unknown actions {}".format(action))
    

def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  registers = defaultdict(int)
  maxValue = 0
  for line in input:
    line = line.strip().split(" ")
    
    testReg = line[4]
    operator = line[5]
    value = int(line[6])
    if (operator == ">"):
      if (registers[testReg] > value):
        doAction(registers, line[0], line[1], int(line[2]))
    elif (operator == ">="):
      if (registers[testReg] >= value):
        doAction(registers, line[0], line[1], int(line[2]))
    elif (operator == "<"):
      if (registers[testReg] < value):
        doAction(registers, line[0], line[1], int(line[2]))
    elif (operator == "<="):
      if (registers[testReg] <= value):
        doAction(registers, line[0], line[1], int(line[2]))
    elif (operator == "!="):
      if (registers[testReg] != value):
        doAction(registers, line[0], line[1], int(line[2]))
    elif (operator == "=="):
      if (registers[testReg] == value):
        doAction(registers, line[0], line[1], int(line[2]))
    else:
      print("ERROR unknown operator {}".format(operator))
      
    maxValue = max(maxValue, max(registers.values()))
      
  print(registers)
  print(max(registers.values()))
  print(maxValue)
  
  
if (__name__ == "__main__"):
  main()