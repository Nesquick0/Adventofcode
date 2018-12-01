
def runFirst(input):
  freq = 0

  for line in input:
    if (line[0] == "+"):
      freq += int(line[1:])
    elif (line[0] == "-"):
      freq -= int(line[1:])
    else:
      print("Error", line)
      
  return freq

def runSecond(input):
  freq = 0
  freqSet = set([freq])

  while True:
    for line in input:
      if (line[0] == "+"):
        freq += int(line[1:])
      elif (line[0] == "-"):
        freq -= int(line[1:])
      else:
        print("Error", line)
        
      if (freq in freqSet):
        return freq
      else:
        freqSet.add(freq)


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
      
  freq = runFirst(input)
  print(freq)
      
  freq = runSecond(input)
  print(freq)

if (__name__ == "__main__"):
  main()