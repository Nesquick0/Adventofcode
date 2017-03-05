def main():
  with open("20.input", "r") as file:
    fileContent = file.readlines()
  
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
  if (rangesFix[0][0] > 0):
    print(0)
  else:
    print(rangesFix[0][1]+1)
  
if (__name__ == "__main__"):
  main()