def main():
  with open("3.input", "r") as file:
    fileContent = file.readlines()
    
  triangles = 0
  
  for line in fileContent:
    line = line.strip().split()
    x, y, z = int(line[0]), int(line[1]), int(line[2])
    if ((x + y > z) and (x + z > y) and (y + z > x)):
      triangles += 1
      
  print(triangles)

if (__name__ == "__main__"):
  main()