
def main():
  direction = 0
  posx = 0
  posy = 0
  
  with open("1.input", "r") as file:
    fileContent = file.readline()
    
  instructions = fileContent.strip().split(", ")
  
  for instr in instructions:
    rotate, distance = instr[0], int(instr[1:])
    if (rotate == "R"):
      direction = (direction + 1) % 4
    elif (rotate == "L"):
      direction = (direction - 1) % 4
    else:
      print("wrong rotation")
      
    if (direction == 0):
      posy += distance
    elif (direction == 1):
      posx += distance
    elif (direction == 2):
      posy -= distance
    elif (direction == 3):
      posx -= distance
    else:
      print("wrong direction")
      
  print(posx)
  print(posy)
  print(abs(posx) + abs(posy))

if (__name__ == "__main__"):
  main()