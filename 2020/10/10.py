def runFirst(powers):
  diffs = [0, 0, 0]
  for i in range(1, len(powers)):
    diff = powers[i] - powers[i-1] - 1
    diffs[diff] += 1
  return diffs[0] * diffs[2]

def runSecond(powers):
  curOpt = [0]
  options = 1
  while (len(curOpt) > 0):
    i = curOpt.pop(0)
    base = powers[i]

    for j in range(i+1, i+4):
      if (j < len(powers) and powers[j] <= base+3):
        curOpt.append(j)

    if (len(curOpt) > 0 and max(curOpt) == min(curOpt)):
      options *= len(curOpt)
      curOpt = [max(curOpt)]
    curOpt.sort()

  return options

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  powers = []
  for line in input:
    powers.append(int(line.strip()))
  powers.append(0)
  powers.sort()
  powers.append(max(powers)+3)

  result = runFirst(powers)
  print(result)
      
  result = runSecond(powers)
  print(result)

if (__name__ == "__main__"):
  main()