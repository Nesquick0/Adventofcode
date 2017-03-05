def main():
  with open("3.input", "r") as file:
    fileContent = file.readlines()
    
  triangles = 0
  columns = [[], [], []]
  
  for line in fileContent:
    line = line.strip().split()
    columns[0].append(int(line[0]))
    columns[1].append(int(line[1]))
    columns[2].append(int(line[2]))
    
  columns = columns[0] + columns[1] + columns[2]
  
  for index in xrange(0, len(columns), 3):
    x, y, z = columns[index], columns[index + 1], columns[index + 2]
    if ((x + y > z) and (x + z > y) and (y + z > x)):
      triangles += 1
      
  print(triangles)

if (__name__ == "__main__"):
  main()