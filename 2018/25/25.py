def distance(p1, p2):
  dist = 0
  for i in range(4):
    dist += abs(p2[i] - p1[i])
  return dist

def intoConstellation(constellations, point):
  alreadyAdded = None
  for constel in constellations:
    for cPoint in constel:
      if (distance(cPoint, point) <= 3):
        if (not alreadyAdded):
          constel.append(point)
          alreadyAdded = constel
          break
        else:
          alreadyAdded.extend(constel)
          constel.clear()

  if (not alreadyAdded):
    constellations.append( [point] )
  while ([] in constellations):
    constellations.remove( [] )
  

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
    
  points = []
  for line in input:
    line = line.strip().split(",")
    point = tuple(map(int, line))
    points.append(point)

  #print(points)

  constellations = [ [points[0]] ] 

  for point in points[1:]:
    intoConstellation(constellations, point)

  print(len(constellations))


  

if (__name__ == "__main__"):
  main()