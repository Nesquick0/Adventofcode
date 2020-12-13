def decode(code):
  r = 0
  c = 0
  for i in range(0, 7):
    if (code[i] == "B"):
      r += 2**(6-i)
  for i in range(0, 3):
    if (code[i+7] == "R"):
      c += 2**(2-i)

  id = r * 8 + c
  return (r, c, id)


def runFirst(input):
  maxId = 0
  for line in input:
    r, c, id = decode(line.strip())
    maxId = max(maxId, id)
    #print(r, c, id)
  return maxId

def runSecond(input):
  ids = []
  for line in input:
    r, c, id = decode(line.strip())
    ids.append(id)
  ids.sort()
  for i in range(1, len(ids)-1):
    if ((ids[i] + 2) == ids[i+1]):
      return ids[i]+1
  return 0


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
  
  result = runFirst(input)
  print(result)
      
  result = runSecond(input)
  print(result)

if (__name__ == "__main__"):
  main()