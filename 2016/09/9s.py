def decompress(text, level):
  output = 0
  index = 0
  
  while (index < len(text)):
    char = text[index]
    # Beginning of marker.
    if (char == "("):
      numberBuffer = ""
      repeatAmount = 0
      repeatCounter = 0
    
      # Read ammount of repeated chars.
      index += 1
      while (text[index] != "x"):
        numberBuffer += text[index]
        index += 1
      repeatAmount = int(numberBuffer)
      numberBuffer = ""
        
      # Read how much are chars repeated.
      index += 1
      while (text[index] != ")"):
        numberBuffer += text[index]
        index += 1
      repeatCounter = int(numberBuffer)
      
      index += 1
      output += decompress(text[index:index+repeatAmount], level + 1) * repeatCounter
      index += repeatAmount - 1
      
    else:
      output += 1
    index += 1
    
    if (level == 0):
      print(index, output)
  
  return output

def main():
  with open("9.input", "r") as file:
    fileContent = file.readline().strip()
    
  output = 0
  output = decompress(fileContent, 0)
  print(output)
  

if (__name__ == "__main__"):
  main()