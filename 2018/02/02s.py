
def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
      
  for i in range(len(input)):
    input[i] = input[i].strip()
    
  for iLine in range(len(input)):
    line = input[iLine]
    
    for jLine in range(iLine):
      otherLine = input[jLine]
      foundDiff = False
      
      for i in range(len(line)):
        if (line[i] != otherLine[i]):
          if (not foundDiff):
            foundDiff = True
          else:
            foundDiff = False
            break
            
      if (foundDiff):
        print(line)
        print(otherLine)
        
        for i in range(len(line)):
          if (line[i] != otherLine[i]):
            print(line[:i] + line[i+1:])


if (__name__ == "__main__"):
  main()