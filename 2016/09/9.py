def main():
  with open("9.input", "r") as file:
    fileContent = file.readline().strip()
    
  output = ""
  index = 0
  
  while (index < len(fileContent)):
    char = fileContent[index]
    # Beginning of marker.
    if (char == "("):
      numberBuffer = ""
      repeatAmount = 0
      repeatCounter = 0
    
      # Read ammount of repeated chars.
      index += 1
      while (fileContent[index] != "x"):
        numberBuffer += fileContent[index]
        index += 1
      repeatAmount = int(numberBuffer)
      numberBuffer = ""
        
      # Read how much are chars repeated.
      index += 1
      while (fileContent[index] != ")"):
        numberBuffer += fileContent[index]
        index += 1
      repeatCounter = int(numberBuffer)
      
      index += 1
      for i in xrange(repeatCounter):
        output += fileContent[index:index+repeatAmount]
      index += repeatAmount - 1
      
    else:
      output += char
    index += 1
    
  print(len(output))
  

if (__name__ == "__main__"):
  main()