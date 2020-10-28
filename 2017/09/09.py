def main():
  with open("input", "r") as file:
    input = file.readline().strip()
    
  score = 0
  level = 0
  garbage = False
  garbageCount = 0
  i = 0
  while (i < len(input)):
    char = input[i]
    i += 1
    
    if (char == "!"):
        i += 1
        continue 
        
    if (garbage):
      if (char == ">"):
        garbage = False
      else:
        garbageCount += 1
    else:      
      if (char == "<"):
        garbage = True
      elif (char == "{"):
        level += 1
        score += level
      elif (char == "}"):
        level -= 1
      
  # Part 1
  print(score)
  # Part 2
  print(garbageCount)
    
    
if (__name__ == "__main__"):
  main()