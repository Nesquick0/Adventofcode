def printMatrix(matrix):
  for value in matrix:
    print(value, matrix[value])
    
    
def getSumAround(matrix, coord):
  sum = 0
  for x in range(coord[0]-1, coord[0]+2):
    for y in range(coord[1]-1, coord[1]+2):
      if ((x, y) in matrix):
        sum += matrix[(x, y)]
        
  return sum
  

def main():
  input = 289326
  #input = 5
  
  up, left, down, right = (0, 1), (-1, 0), (0, -1), (1, 0) # directions
  turnLeft = {up: left, left: down, down: right, right: up}
  
  number = 1
  direction = down
  matrix = { (0, 0) : number}
  coord = (0, 0)
  
  while (number <= input):
    newDirection = turnLeft[direction]
    newCoord = (coord[0] + newDirection[0], coord[1] + newDirection[1])
    if (newCoord not in matrix):
      coord = newCoord
      direction = newDirection
    else:
      coord = (coord[0] + direction[0], coord[1] + direction[1])
      
    number = getSumAround(matrix, coord)
    matrix[coord] = number
  
  #printMatrix(matrix)
  print(number)
    
  
  

if (__name__ == "__main__"):
  main()