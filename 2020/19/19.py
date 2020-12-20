def translate(rule, rules):
  # Already done.
  ruleStr = rules[rule]
  if ("a" == ruleStr[0] or "b" == ruleStr[0]):
    return

  result = ""
  resultDone = ""
  partSplits = ruleStr.split(" ")
  for num in partSplits:
    if ("a" in num or "b" in num):
      result += num
    elif ("|" in num):
      result += " "
      resultDone += result
      result = ""
    else:
      translate(num, rules)
      newResult = []
      for y in result.split(" "):
        for x in rules[num].split(" "):
          newResult.append(y + x)
      result = " ".join(newResult)
  rules[rule] = resultDone + result


def runFirst(rules, messages):
  valid = 0
  translate("0", rules)
  checkSet = set(rules["0"].split())
  for msg in messages:
    if (msg in checkSet):
      valid += 1
      #print(msg)
  return valid


def runSecond(rules, messages):
  valid = 0
  translate("42", rules)
  translate("31", rules)
  check42 = set(rules["42"].split())
  check42Len = len(list(check42)[0])
  check31 = set(rules["31"].split())
  check31Len = len(list(check31)[0])
  if (check42Len != check31Len):
    print("Error!")
    
  for msg in messages:
    num42 = 0
    num31 = 0
    chunks = [(msg[i:i+check42Len]) for i in range(0, len(msg), check42Len)]
    mode = 1
    validMsg = True
    for chunk in chunks:
      if (mode == 1):
        if (chunk in check42):
          num42 += 1
        elif (chunk in check31):
          num31 += 1
          mode = 2
        else:
          validMsg = False
          break
      else: # Already 31 chunk
        if (chunk in check31):
          num31 += 1
        else:
          validMsg = False
          break
    if (num42 < 2):
      validMsg = False
    if (num31 < 1):
      validMsg = False
    if (num42 <= num31):
      validMsg = False

    if (validMsg):
      valid += 1
  return valid


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  rules = {}
  messages = []
  i = 0
  while (i < len(input)):
    line = input[i].strip()
    if (not line):
      break
    lineSplit = line.split(": ")
    rules[lineSplit[0]] = lineSplit[1].replace("\"", "")
    i += 1
  while (i < len(input)):
    line = input[i].strip()
    if (line):
      messages.append(line)
    i += 1
    
  rules2 = dict(rules)

  result = runFirst(rules, messages)
  print(result)
  
  result = runSecond(rules2, messages)
  print(result)


if (__name__ == "__main__"):
  main()