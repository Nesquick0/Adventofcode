class Tower(object):
  def __init__(self):
    self.weight = 0
    self.parent = None
    self.children = []
    
  def __str__(self):
    return "%d, %s, %s" % (self.weight, self.parent, self.children)
    
def SumOfWeights(towers, name):
  sum = towers[name].weight
  for childName in towers[name].children:
    sum += SumOfWeights(towers, childName)
    
  return sum
  
  
def FindWrong(towers):
  wrongTower = None
  wrongWeight = 10**9
  for tower in towers:
    if (len(towers[tower].children) > 0):
      weight = SumOfWeights(towers, towers[tower].children[0])
      for childName in towers[tower].children:
        if (weight != SumOfWeights(towers, childName)):
          if (wrongWeight > weight):
            wrongTower = tower
            wrongWeight = weight
            
  return wrongTower


def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  towers = {}
  
  for line in input:
    line = line.strip().split(" ")
    name = line[0]
    weight = int(line[1][1:-1])
    if (name not in towers):
      towers[name] = Tower()
      
    towers[name].weight = weight
    
    if (len(line) > 2):
      for i in range(3, len(line)):
        childName = line[i] if line[i][-1] != "," else line[i][:-1]
        if (childName not in towers):
          towers[childName] = Tower()
          
        towers[childName].parent = name
        towers[name].children.append(childName)
    
  # Part1. Top most tower
  for name, tower in towers.items():
    if (tower.parent == None):
      print("No parent: %s" % (name))
      break
    
  # for tower in towers:
    # print("%s, %s, %d" % (tower, towers[tower], SumOfWeights(towers, tower)))
    
  # Find wrong tower
  wrong = FindWrong(towers)
  print(wrong)

  # for childName in towers[wrong].children:
    # print("Sum: %d, Weight: %d, Name: %s" % (SumOfWeights(towers, childName), towers[childName].weight, childName))
  
  # Find most common weight.
  weightDict = {}
  for childName in towers[wrong].children:
    sumWeight = SumOfWeights(towers, childName)
    if (sumWeight not in weightDict):
      weightDict[sumWeight] = 1
    else:
      weightDict[sumWeight] += 1
      
  # Sort weights and calculate wanted difference.
  sortedWeights = ([key for key in sorted(weightDict, key=weightDict.get, reverse=True)])
  weightDiff = sortedWeights[0] - sortedWeights[1]
  
  # Find which tower has wrong weight and subtract.
  for childName in towers[wrong].children:
    if (SumOfWeights(towers, childName) == sortedWeights[1]):
      print(towers[childName].weight + weightDiff)
      break
  
    
if (__name__ == "__main__"):
  main()