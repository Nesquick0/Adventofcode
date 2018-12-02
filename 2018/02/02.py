
def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
      
  twoTimes = 0
  threeTimes = 0
      
  for line in input:
    line = line.strip()
    letterDict = {}
    for char in line:
      if (char not in letterDict):
        letterDict[char] = 1
      else:
        letterDict[char] += 1
        
    #print(line)
    #print(letterDict)
    found3 = False
    found2 = False
    for char in letterDict:
      if (letterDict[char] == 3):
        found3 = True
      elif (letterDict[char] == 2):
        found2 = True
        
    if (found3):
      threeTimes += 1
    if (found2):
      twoTimes += 1
        
  print("twoTimes", twoTimes)
  print("threeTimes", threeTimes)
  
  print(threeTimes * twoTimes)

if (__name__ == "__main__"):
  main()