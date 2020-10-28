def distance(posX, posY):
  steps = abs(posX)
  restY = abs(posY) - (abs(posX) * 0.5)
  if (restY > 0):
    steps += restY
  steps = round(steps)
  return steps

def main():
  with open("input", "r") as file:
    input = file.readline().strip().split(",")
    
  posX = 0.0
  posY = 0.0
  
  maxDistance = 0
  for dir in input:
    if (dir == "n"):
      posY += 1
    elif (dir == "s"):
      posY -= 1
    elif (dir == "ne"):
      posX += 1
      posY += 0.5
    elif (dir == "se"):
      posX += 1
      posY -= 0.5
    elif (dir == "nw"):
      posX -= 1
      posY += 0.5
    elif (dir == "sw"):
      posX -= 1
      posY -= 0.5
      
    maxDistance = max(maxDistance, distance(posX, posY))
      
  print(posX, posY)
  print(distance(posX, posY))
  print(maxDistance)
    
 
if (__name__ == "__main__"):
  main()