import re

def runFirst(bags):
  result = {"shiny gold" : 1}
  lastCount = -1
  while len(result) != lastCount:
    lastCount = len(result)
    for bag, bagIns in bags.items():
      for bagIn in bagIns:
        if (bagIn in result):
          result[bag] = 1
  return len(result)-1

def runSecond(bags):
  numBags = 0
  resolve = {"shiny gold" : 1}
  while resolve:
    resolveNew = {}
    for bag, bagNum in resolve.items():
      numBags += bagNum
      if (bag in bags):
        bagIns = bags[bag]
        for bagIn in bagIns:
          if (bagIn not in resolveNew):
            resolveNew[bagIn] = 0
          resolveNew[bagIn] += bagIns[bagIn] * bagNum
    resolve = resolveNew
  return numBags - 1


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  bags = {}
  bagPattern = re.compile(r"(\d+ [\w ]+) bags?")
  for line in input:
    lineSplit = line.strip().split(" contain ")
    name1 = lineSplit[0][:-5]
    m = bagPattern.findall(lineSplit[1])
    for r in m:
      name2 = r[r.index(" ")+1:]
      if (name1 not in bags):
        bags[name1] = {}
      bags[name1][name2] = int(r[:r.index(" ")])

  # for bag in bags:
  #   print(bag, bags[bag])
  result = runFirst(bags)
  print(result)
      
  result = runSecond(bags)
  print(result)

if (__name__ == "__main__"):
  main()