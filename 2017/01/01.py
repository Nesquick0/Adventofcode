def main():
  with open("input.txt", "r") as file:
    input = file.readline().strip()
    nItems = len(input)
    
  # Part 1
  sum = 0
  for i in range(0, nItems):
    if (input[i] == input[(i+1)%nItems]):
      sum += int(input[i])
      
  print(sum)
  
  # Part 2
  sum = 0
  for i in range(0, nItems):
    if (input[i] == input[(i+(nItems//2))%nItems]):
      sum += int(input[i])
      
  print(sum)
  
if (__name__ == "__main__"):
  main()