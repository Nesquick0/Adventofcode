
def main():
  direction = 0
  posx = 0
  posy = 0
  
  visited = {} # key is posx, value is set of posy
  
  with open("1.input", "r") as file:
    fileContent = file.readline()
    
  instructions = fileContent.strip().split(", ")
  
  for instr in instructions:
    rotate, distance = instr[0], int(instr[1:])
    if (rotate == "R"):
      direction = (direction + 1) % 4
    elif (rotate == "L"):
      direction = (direction - 1) % 4
    else:
      print("wrong rotation")
    
    for i in xrange(1, distance + 1):
      if (direction == 0):
        posy += 1
      elif (direction == 1):
        posx += 1
      elif (direction == 2):
        posy -= 1
      elif (direction == 3):
        posx -= 1
      else:
        print("wrong direction")
      
      if (posx in visited):
        if (posy in visited[posx]):
          print(posx)
          print(posy)
          print(abs(posx) + abs(posy))
          return
        else:
          # Position hasn't been already visited, add to the set.
          visited[posx].add(posy)
      else:
        # posx hasn't been already visited, add to the set.
        visited[posx] = set()
        visited[posx].add(posy)
  
  print("no position visited twice")

if (__name__ == "__main__"):
  main()