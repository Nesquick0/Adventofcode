def runFirst(input):
  forms = {}
  sum = 0
  for line in input:
    line = line.strip()
    if (not line):
      sum += len(forms)
      forms = {}
    else:
      for char in line:
        forms[char] = 1
  sum += len(forms)

  return sum

def runSecond(input):
  forms = {}
  count = 0
  sum = 0
  for line in input:
    line = line.strip()
    if (not line):
      for char in forms:
        if (forms[char] == count):
          sum += 1
      forms = {}
      count = 0
    else:
      count += 1
      for char in line:
        if (char not in forms):
          forms[char] = 1
        else:
          forms[char] += 1

  for char in forms:
    if (forms[char] == count):
      sum += 1

  return sum


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  result = runFirst(input)
  print(result)
      
  result = runSecond(input)
  print(result)

if (__name__ == "__main__"):
  main()