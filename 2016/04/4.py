def main():
  with open("4.input", "r") as file:
    fileContent = file.readlines()

  idSum = 0
  
  for line in fileContent:
    line = line.strip().split("[")
    checkSum = line[1][:-1]
    line = line[0].split("-")
    roomId = int(line[-1])
    roomCode = "".join(line[:-1])
    
    counter = {}
    for char in roomCode:
      if (char not in counter):
        counter[char] = 1
      else:
        counter[char] += 1

    def cmp(x, y):
      if (counter[x] != counter[y]):
        return counter[y] - counter[x]
      return ord(x) - ord(y)
      
    check = sorted(counter, cmp)
    checkCalc = "".join(check[:5])
    
    if (checkSum == checkCalc):
      idSum += roomId
    
  print(idSum)

if (__name__ == "__main__"):
  main()