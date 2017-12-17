def maxNumberInLayer(layer):
  sizeOfSquare = (layer*2) + 1
  return (sizeOfSquare*sizeOfSquare)

def main():
  input = 289326
  #input = 23
  
  layer = 0
  # Find in what layer number is.
  while (maxNumberInLayer(layer) <= input):
    layer += 1
  print(layer)
  print(maxNumberInLayer(layer))
  
  if (layer == 0):
    print(0)
    return
    
  # Find where number is.
  maxInLayer = maxNumberInLayer(layer)
  nInLayer = (layer*2)
  closestNumbers = [maxInLayer, maxInLayer-nInLayer]
  while ((closestNumbers[0] >= input) and (closestNumbers[1] >= input)):
    closestNumbers[0] -= nInLayer
    closestNumbers[1] -= nInLayer
    
  print(closestNumbers)
  
  # Get number of steps needed.
  steps = layer+layer
  steps -= min(closestNumbers[0]-input, input-closestNumbers[1])
  print(steps)
  

if (__name__ == "__main__"):
  main()