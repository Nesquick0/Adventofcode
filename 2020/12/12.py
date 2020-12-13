def runFirst(input):
  dir = 2
  x = 0
  y = 0
  for line in input:
    line = line.strip()
    type = line[0]
    value = int(line[1:])
    if (type == "N"):
      y -= value
    elif (type == "S"):
      y += value
    elif (type == "E"):
      x += value
    elif (type == "W"):
      x -= value
    elif (type == "L"):
      dir = (dir - (value // 90)) % 4
    elif (type == "R"):
      dir = (dir + (value // 90)) % 4
    elif (type == "F"):
      if (dir == 0):
        x -= value
      elif (dir == 1):
        y -= value
      elif (dir == 2):
        x += value
      elif (dir == 3):
        y += value
    #print(line, x, y, dir)
  return abs(x) + abs(y)


def runSecond(input):
  x = 0
  y = 0
  xWay = 10
  yWay = -1
  for line in input:
    line = line.strip()
    type = line[0]
    value = int(line[1:])
    if (type == "N"):
      yWay -= value
    elif (type == "S"):
      yWay += value
    elif (type == "E"):
      xWay += value
    elif (type == "W"):
      xWay -= value
    elif (type == "L"):
      for i in range(value // 90):
        temp = -xWay
        xWay = yWay
        yWay = temp
    elif (type == "R"):
      for i in range(value // 90):
        temp = xWay
        xWay = -yWay
        yWay = temp
    elif (type == "F"):
      x += xWay * value
      y += yWay * value
    #print(line, x, y, xWay, yWay)
  return abs(x) + abs(y)


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
  
  result = runFirst(input)
  print(result)
      
  result = runSecond(input)
  print(result)

if (__name__ == "__main__"):
  main()