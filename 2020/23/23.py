def runFirst(values):
  minmax = (min(values), max(values))
  for r in range(100):
    curCup = values[0]
    pickup = values[1:4]
    del values[1:4]
    dest = curCup - 1
    while (dest not in values):
      dest -= 1
      if (dest < minmax[0]):
        dest = minmax[1]
    destIndex = values.index(dest)
    values = values[:destIndex+1] + pickup + values[destIndex+1:]
    values = values[1:] + values[:1]
  
  index1 = values.index(1)
  result = values[index1+1:] + values[:index1]
  result = int("".join(map(str, result)))
  return result

def runSecond(values):
  for i in range(max(values)+1, 1_000_000+1):
  #for i in range(max(values)+1, 100+1):
    values.append(i)

  minmax = (min(values), max(values))
  for r in range(10_000_000):
  #for r in range(1_000):
    curCup = values[0]
    pickup = values[1:4]
    del values[1:4]
    dest = curCup - 1
    if (dest < minmax[0]):
        dest = minmax[1]
    destIndex = len(values)-1
    while (dest in pickup):
      dest -= 1
      if (dest < minmax[0]):
        dest = minmax[1]
    while (values[destIndex] != dest):
      destIndex -= 1
    values = values[:destIndex+1] + pickup + values[destIndex+1:]
    values = values[1:] + values[:1]
    if (r % 1 == 0 and r > 100):
      print("===============================================")
      for i in range(len(values)//30-10, len(values)//30+1):
        print(" ".join(map(str, values[i*30:(i+1)*30])))
      print(r)
  print("")
  
  index1 = values.index(1)
  result = values[index1+1] * values[index1+2]
  return result


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  #input = "389125467"
  input = "364289715"
  values = []
  for char in input:
    values.append(int(char))

  result = runFirst(values[:])
  print(result)
  
  result = runSecond(values[:])
  print(result)


if (__name__ == "__main__"):
  main()
