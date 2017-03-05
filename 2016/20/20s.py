def main():
  with open("20.input", "r") as file:
    fileContent = file.readlines()
    
  maxAddress = 2**32
  
  ranges = []
  for line in fileContent:
    values = line.strip().split("-")
    ranges.append( [int(values[0]), int(values[1])] )
    
  ranges.sort(key=lambda x: x[0])
  
  rangesFix = [ranges[0]]
  for item in ranges:
    # Ranges overlap
    if (item[0] <= (rangesFix[-1][1] + 1)):
      if (item[1] > rangesFix[-1][1]):
        rangesFix[-1][1] = item[1]
    # Range don't overlap, create new range
    else:
      rangesFix.append(item)
      
  # Find lowest number
  numberOfIp = rangesFix[0][0]
  for i in xrange(1, len(rangesFix)-1):
    numberOfIp += rangesFix[i+1][0] - rangesFix[i][1] - 1
  numberOfIp += maxAddress - rangesFix[-1][1]
  print(numberOfIp)
  
if (__name__ == "__main__"):
  main()