def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
      
  claims = {}
  for line in input:
    # #1 @ 1,3: 4x4
    line = line.strip()
    lineSplit = line.split("@")
    id = int(lineSplit[0][1:-1])
    coordSplit = lineSplit[1].split(":")
    coordSplit[0] = list(map(str.strip, coordSplit[0].split(",")))
    coordSplit[1] = list(map(str.strip, coordSplit[1].split("x")))
    claims[id] = [coordSplit[0][0], coordSplit[0][1], coordSplit[1][0], coordSplit[1][1], False]
    
  pos = []
  for i in range(1000*1000):
    pos.append( [0, 0] )
  
  for id in claims:
    x, y, w, h, overlap = list(map(int, claims[id]))
    
    for ix in range(x, x+w):
      for iy in range(y, y+h):
        square = pos[ix + iy*1000]
        square[0] += 1
        if (square[1] > 0):
          claims[square[1]][4] = True
          claims[id][4] = True
        else:
          square[1] = id
    
  count = 0    
  for i in range(len(pos)):
    if (pos[i][0] > 1):
      count += 1
      
  print(count)
  
  for id in claims:
    x, y, w, h, overlap = claims[id]
    if (not overlap):
      print(id)
  

if (__name__ == "__main__"):
  main()