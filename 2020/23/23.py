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
  # From https://github.com/StasDeep/Advent-of-Code/blob/387432fb767f152772cb9aace6ae8a6887679ab8/2020/23/solution.py
  values = values + list(range(len(values) + 1, 1_000_000 + 1))
  # Create linked list with dictionary that each value reference to next value.
  d = {c1: c2 for c1, c2 in zip(values, values[1:] + [values[0]])}
  valuesLen = len(values)
  cur = values[0]
  for r in range(10_000_000):
    x = cur
    pickup = []
    for _ in range(3):
      pickup.append(d[x])
      x = d[x]

    dest = cur - 1
    if (dest < 1):
      dest = valuesLen
    while (dest in pickup):
      dest -= 1
      if (dest < 1):
        dest = valuesLen
    # dest = next(
    #     cup for i in count(1)
    #     if (cup if (cup := cur - i) > 0 else (cup := len(values) + cup)) not in pickup
    # )

    d[cur], d[pickup[-1]], d[dest] = d[pickup[-1]], d[dest], d[cur]
    cur = d[cur]
  
  print(d[1], d[d[1]])
  return d[1] * d[d[1]]


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
  
  result = runSecond(values)
  print(result)


if (__name__ == "__main__"):
  main()
