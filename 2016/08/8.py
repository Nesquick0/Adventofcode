def drawRect(display, sizex, sizey):
  for x in xrange(sizex):
    for y in xrange(sizey):
      display[y][x] = 1
      
      
def rotateColumn(display, column, count):
  copy = []
  for y in xrange(len(display)):
    copy.append(display[y][column])
  for y in xrange(len(display)):
    display[y][column] = copy[(y - count) % len(display)]
  
 
def rotateRow(display, row, count):
  copy = display[row][:]
  for x in xrange(len(display[row])):
    display[row][x] = copy[(x - count) % len(display[row])]
      

def printDisplay(display):
  for row in display:
    line = ""
    for x in row:
      line += "#" if (x) else "." 
    print(line)
    

def main():
  with open("8.input", "r") as file:
    fileContent = file.readlines()
  
  # Y first index. X second index.
  display = [[0 for i in range(50)] for j in range(6)]
  
  for line in fileContent:
    line = line.strip().split(" ")
    if (line[0] == "rect"):
      sizes = line[1].split("x")
      drawRect(display, int(sizes[0]), int(sizes[1]))
    elif (line[0] == "rotate"):
      count = int(line[4])
      index = int(line[2][2:])
      if (line[1] == "column"):
        rotateColumn(display, index, count)
      elif (line[1] == "row"):
        rotateRow(display, index, count)
    else:
      print("wrong instruction")
  
  printDisplay(display)
  
  countOn = 0
  for row in display:
    for x in row:
      if (x):
        countOn += 1
  print(countOn)
      

if (__name__ == "__main__"):
  main()