def runFirst(instr):
  memory = {}
  lastMask = ""
  for ins in instr:
    if (ins[0] == -1):
      lastMask = ins[1]
    else:
      value = ins[1]
      for i in range(len(lastMask)):
        if (lastMask[-i-1] == "0"):
          value = ~(2**i) & value
        elif (lastMask[-i-1] == "1"):
          value = 2**i | value
      memory[ins[0]] = value

  sum = 0
  for value in memory:
    sum += memory[value]
  return sum


def generateBits(randomBits):
  if (not randomBits):
    return []
  
  if (len(randomBits) > 1):
    result = []
    for gen in generateBits(randomBits[1:]):
      result.append(gen + [[randomBits[0], 0]])
      result.append(gen + [[randomBits[0], 1]])
    return result
  else:
    return [[[randomBits[0], 0]], [[randomBits[0], 1]]]

def runSecond(instr):
  memory = {}
  lastMask = ""
  lastMaskLen = 0
  randomBits = []
  for ins in instr:
    if (ins[0] == -1):
      lastMask = ins[1]
      lastMaskLen = len(lastMask)
      randomBits = []
      for i in range(lastMaskLen):
        if (lastMask[-i-1] == "X"):
          randomBits.append(i)
    else:
      value = ins[1]
      addr = ins[0]
      for i in range(lastMaskLen):
        if (lastMask[-i-1] == "1"):
          addr = 2**i | addr
      for bits in generateBits(randomBits):
        #print(bits)
        newAddr = addr
        for bit in bits:
          if (bit[1] == 0):
            newAddr = ~(2**bit[0]) & newAddr
          else:
            newAddr = 2**bit[0] | newAddr
        memory[newAddr] = value

  sum = 0
  for value in memory:
    sum += memory[value]
  return sum

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
  
  instr = []
  for line in input:
    line = line.strip().split(" = ")
    if (line[0] == "mask"):
      instr.append([-1, line[1]])
    else:
      instr.append([int(line[0][4:-1]), int(line[1])])

  result = runFirst(instr)
  print(result)
  
  result = runSecond(instr)
  print(result)


if (__name__ == "__main__"):
  main()