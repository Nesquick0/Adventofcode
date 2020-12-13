import itertools

def runFirst(code):
  lastNums = code[:25]
  for i in range(len(lastNums), len(code)):
    num = code[i]

    perms = list(map(sum, itertools.permutations(lastNums, 2)))
    if (num not in perms):
      return num
    lastNums.pop(0)
    lastNums.append(num)
  return None

def runSecond(code, target):
  for i in range(0, len(code)):
    lastSum = 0
    iSum = i
    listSum = []
    while (lastSum < target):
      lastSum += code[iSum]
      listSum.append(code[iSum])
      iSum += 1
    if (lastSum == target):
      return listSum
  return None

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  code = []
  for line in input:
    code.append(int(line.strip()))

  result = runFirst(code)
  print(result)
      
  result = runSecond(code, result)
  print(min(result) + max(result))

if (__name__ == "__main__"):
  main()