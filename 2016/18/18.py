def isTrap(index, row):
  left = 0 if (index == 0) else row[index - 1]
  center = row[index]
  right = 0 if (index == (len(row) - 1)) else row[index + 1]
  
  if (left and center and (not right)):
    return 1
  if ((not left) and center and right):
    return 1
  if (left and (not center) and (not right)):
    return 1
  if ((not left) and (not center) and right):
    return 1
    
  return 0

def main():
  with open("18.input", "r") as file:
    firstLine = file.readline().strip()
    
  firstLine = map(int, list(firstLine.replace(".", "0").replace("^", "1")))
  
  rows = [firstLine]
  for i in xrange(1, 400000):
    newRow = rows[i-1][:]
    for x in xrange(len(newRow)):
      newRow[x] = isTrap(x, rows[i-1])
    rows.append(newRow)
    
  safeTiles = 0
  for row in rows:
    for pos in row:
      if (pos == 0):
        safeTiles += 1
    #print(row)
    
  print(safeTiles)

if (__name__ == "__main__"):
  main()