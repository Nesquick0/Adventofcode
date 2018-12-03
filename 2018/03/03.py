def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
      
  claims = []
  for line in input:
    # #1 @ 1,3: 4x4
    line = line.strip()
    lineSplit = line.split("@")
    id = int(lineSplit[0][1:-1])
    coordSplit = lineSplit[1].split(":")
    coordSplit[0] = list(map(str.strip, coordSplit[0].split(",")))
    coordSplit[1] = list(map(str.strip, coordSplit[1].split("x")))
    claims.append( [id, coordSplit[0][0], coordSplit[0][1], coordSplit[1][0], coordSplit[1][1]] )
    
  pos = [0]*1000000
  
  for claim in claims:
    id, x, y, w, h = list(map(int, claim))
    
    for ix in range(x, x+w):
      for iy in range(y, y+h):
        pos[ix + iy*1000] += 1
    
  count = 0    
  for i in range(len(pos)):
    if (pos[i] > 1):
      count += 1
      
  print(count)
  

if (__name__ == "__main__"):
  main()