def checkSlope(world, width, height, stepX, stepY):
  x = stepX
  y = stepY

  trees = 0
  while (y < height):
    index = y * width + x % width
    if (world[index] == 1):
      trees += 1
    x += stepX
    y += stepY
  return trees

def runFirst(world, width, height):
  return checkSlope(world, width, height, 3, 1)

def runSecond(world, width, height):
  result  = checkSlope(world, width, height, 1, 1)
  result *= checkSlope(world, width, height, 3, 1)
  result *= checkSlope(world, width, height, 5, 1)
  result *= checkSlope(world, width, height, 7, 1)
  result *= checkSlope(world, width, height, 1, 2)
  return result


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  world = []
  # Parse input
  width = 0
  height = 0
  for line in input:
    line = line.strip()
    width = len(line)
    for char in line:
      if (char == "."):
        world.append(0)
      else:
        world.append(1)
    height += 1
  
  result = runFirst(world, width, height)
  print(result)
      
  result = runSecond(world, width, height)
  print(result)

if (__name__ == "__main__"):
  main()