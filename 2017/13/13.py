from collections import defaultdict


def moveScan(layers):
  for pos in layers:
    layer = layers[pos]
    if (layer[2] == 1):
      if (layer[1] >= layer[0]-1):
        layer[2] = -1
        layer[1] -= 1
      else:
        layer[1] += 1
    else:
      if (layer[1] <= 0):
        layer[2] = 1
        layer[1] += 1
      else:
        layer[1] -= 1


def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  layers = {}
  maxPos = 0
  for line in input:
    line = line.strip().split(":")
    layer, size = int(line[0]), int(line[1])
    layers[layer] = [size, 0, 1]
    maxPos = max(maxPos, layer)
    
  
  severity = 0
  for pos in range(maxPos+1):
    if (pos in layers):
      if (layers[pos][1] == 0):
        severity += pos * layers[pos][0]
        
    moveScan(layers)
    
  print(severity)
  
 
if (__name__ == "__main__"):
  main()