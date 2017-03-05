def main():
  with open("6.input", "r") as file:
    fileContent = file.readlines()

  msgLength = len(fileContent[0].strip())
  msgArray = []
  for i in xrange(0, msgLength):
    msgArray.append(dict())
  
  for line in fileContent:
    for i, char in enumerate(line.strip()):
      if (char not in msgArray[i]):
        msgArray[i][char] = 1
      else:
        msgArray[i][char] += 1
        
  result = ""
  for msgChar in msgArray:
    result += sorted(msgChar, lambda x, y: msgChar[y] - msgChar[x])[-1]
    
  print(result)

if (__name__ == "__main__"):
  main()