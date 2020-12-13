import re

def runFirst(codeOrig):
  code = []
  for instr in codeOrig:
    code.append(instr[:])

  accum = 0
  id = 0
  while (code[id][2] == 0):
    code[id][2] += 1
    if (code[id][0] == 0): # acc
      accum += code[id][1]
    elif (code[id][0] == 1): # jmp
      id += code[id][1]-1
    elif (code[id][0] == 2): # nop
      pass
    id += 1
  return accum

def runSecond(codeOrig):
  for i in range(len(codeOrig)):
    code = []
    for instr in codeOrig:
      code.append(instr[:])
    if (code[i][0] == 1):
      code[i][0] = 2
    elif (code[i][0] == 2):
      code[i][0] = 1
      
    accum = 0
    id = 0
    while (code[id][2] == 0):
      code[id][2] += 1
      if (code[id][0] == 0): # acc
        accum += code[id][1]
      elif (code[id][0] == 1): # jmp
        id += code[id][1]-1
      elif (code[id][0] == 2): # nop
        pass
      id += 1
      if (id == len(code)):
        return accum
  return None


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  code = []
  for line in input:
    line = line.strip().split(" ")
    instr = -1
    if (line[0] == "acc"):
      instr = 0
    elif (line[0] == "jmp"):
      instr = 1
    elif (line[0] == "nop"):
      instr = 2
    code.append( [instr, int(line[1]), 0] )

  result = runFirst(code)
  print(result)
      
  result = runSecond(code)
  print(result)

if (__name__ == "__main__"):
  main()