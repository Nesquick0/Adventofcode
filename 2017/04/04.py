def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  # Part1
  validSum = 0
  for line in input:
    words = {}
    line = line.strip().split()
    valid = True
    for word in line:
      if (word not in words):
        words[word] = 1
      else:
        valid = False
        
    if (valid):
      validSum += 1
      
  print(validSum)
  
  # Part2
  validSum = 0
  for line in input:
    words = {}
    line = line.strip().split()
    valid = True
    for word in line:
      word = str(sorted(word))
      if (word not in words):
        words[word] = 1
      else:
        valid = False
        
    if (valid):
      validSum += 1
      
  print(validSum)
  

if (__name__ == "__main__"):
  main()