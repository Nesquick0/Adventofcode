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
        
        
def reset(layers, save):
  for pos in layers:
    layer = layers[pos]
    if (save):
      layer[3] = layer[1]
      layer[4] = layer[2]
    else:
      layer[1] = layer[3]
      layer[2] = layer[4]
    
    
def tryRun(layers, maxPos):
  for pos in range(maxPos+1):
    if (pos in layers):
      if (layers[pos][1] == 0):
        return False # Caught.

    moveScan(layers)
    
  return True
  

def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  layers = {}
  maxPos = 0
  for line in input:
    line = line.strip().split(":")
    layer, size = int(line[0]), int(line[1])
    layers[layer] = [size, 0, 1, 0, 1] # Range, current pos, direction, start pos, start dir.
    maxPos = max(maxPos, layer)
    
  
  waitTime = 1
  while (True):
    reset(layers, False)
    moveScan(layers)
    reset(layers, True)
    
    if (tryRun(layers, maxPos)):
      break
    waitTime += 1
    #print(waitTime, end=" ")
    
  print(waitTime)
  
 
if (__name__ == "__main__"):
  main()