def findDivision(line):
  for i in range(len(line)-1, 0, -1):
    for j in range(0, i):
      if (line[i] % line[j] == 0):
        return (line[i] // line[j])
        
  print(line)
  return -1


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
  
  #Part 1
  sum = 0
  for line in input:
    line = line.strip().split()
    line = list(map(int, line))
    sum += max(line) - min(line)
  
  print(sum)
  
  # Part 2
  sum = 0
  for line in input:
    line = line.strip().split()
    line = list(map(int, line))
    line = sorted(line)
    result = findDivision(line)
    sum += result
    
  print(sum)
    
  
  
if (__name__ == "__main__"):
  main()