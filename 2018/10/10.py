import re

def minmax(lights):
  minX = minY = 10000
  maxX = maxY = 0
  for light in lights:
    minX = min(minX, light[0])
    minY = min(minY, light[1])
    maxX = max(maxX, light[0])
    maxY = max(maxY, light[1])
  return (minX, maxX, minY, maxY)

def printWorld(lights):
  minX, maxX, minY, maxY = minmax(lights)

  for y in range(minY, maxY+1):
    for x in range(minX, maxX+1):
      found = False
      for light in lights:
        if (light[0] == x and light[1] == y):
          found = True
          break
      print("#" if found else ".", end="")
    print("")
    
def simulate(lights):
  for light in lights:
    light[0] += light[2]
    light[1] += light[3]

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
    
  lights = []
    
  pattern = re.compile(r"position=<([ \-\d]+),([ \-\d]+)> velocity=<([ \-\d]+),([ \-\d]+)>.*")
  for line in input:
    m = pattern.match(line)
    if (m):
      x, y, vx, vy = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
      lights.append( [x, y, vx, vy] )
  
  minX, maxX, minY, maxY = minmax(lights)
  minSize = (maxX - minX) * (maxY - minY)
  #printWorld(lights)
  
  for i in range(1, 12000):
    simulate(lights)
    
    minX, maxX, minY, maxY = minmax(lights)
    size = (maxX - minX) * (maxY - minY)
    if ((maxX - minX) < 300 and size < minSize):
      minSize = size
      print(i, size, minSize)
      printWorld(lights)
      print("")
  

if (__name__ == "__main__"):
  main()