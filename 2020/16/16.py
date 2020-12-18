import re

def runFirst(rules, nearbyTickets):
  sum = 0
  invalidIds = set()
  for i in range(len(nearbyTickets)):
    ticket = nearbyTickets[i]
    for num in ticket:
      valid = False
      for name, rule in rules.items():
        if ((num >= rule[0] and num <= rule[1]) or (num >= rule[2] and num <= rule[3])):
          valid = True
          break
      if (not valid):
        sum += num
        invalidIds.add(i)
  return sum, sorted(list(invalidIds))


def runSecond(rules, nearbyTickets, yourTicket):
  ticketLen = len(nearbyTickets[0])

  rulesCount = {}
  for rule in rules:
    rulesCount[rule] = [0]*ticketLen

  for ticket in nearbyTickets:
    for i in range(ticketLen):
      num = ticket[i]
      for name, rule in rules.items():
        if ((num >= rule[0] and num <= rule[1]) or (num >= rule[2] and num <= rule[3])):
          rulesCount[name][i] += 1

  targetNum = len(nearbyTickets)
  ruleIndex = -1
  for i in range(ticketLen):
    for name, ruleCount in rulesCount.items():
      if (ruleCount.count(targetNum) == 1):
        ruleIndex = ruleCount.index(targetNum)
        rules[name].append(ruleIndex)
        if (len(rules[name]) != 5):
          print(name, rules)
        break
    for name, ruleCount in rulesCount.items():
      ruleCount[ruleIndex] = -1

  result = 1
  for name, rule in rules.items():
    if ("departure" in name):
      result *= yourTicket[rule[4]]
  return result


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
  
  rules = {}
  yourTicket = []
  nearbyTickets = []
  mode = 0
  for line in input:
    line = line.strip()
    if ("your ticket" in line):
      mode = 1
      continue
    if ("nearby tickets" in line):
      mode = 2
      continue

    if (not line):
      continue

    if (mode == 0):
      m = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
      if (m):
        rules[m.group(1)] = list(map(int, [m.group(2), m.group(3), m.group(4), m.group(5)]))
      else:
        print(line)
    elif (mode == 1):
      yourTicket = list(map(int, line.split(",")))
    elif (mode == 2):
      nearbyTickets.append(list(map(int, line.split(","))))

  result, invalidIds = runFirst(rules, nearbyTickets)
  print(result)

  for i in range(len(invalidIds)-1, -1, -1):
    nearbyTickets.pop(invalidIds[i])
  
  result = runSecond(rules, nearbyTickets, yourTicket)
  print(result)


if (__name__ == "__main__"):
  main()