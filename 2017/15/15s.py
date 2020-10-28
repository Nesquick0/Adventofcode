def genNew(oldValues):
  genFactor = [16807, 48271]
  values = oldValues[:]
  while (True):
    values[0] = values[0] * genFactor[0] % 2147483647
    if (values[0] % 4 == 0):
      break
  while (True):
    values[1] = values[1] * genFactor[1] % 2147483647
    if (values[1] % 8 == 0):
      break
  return values
  

def main():
  #startGen = [65, 8921]
  startGen = [699, 124]
  
  values = startGen[:]
  validPairs = 0
  for i in range(5000000):
    values = genNew(values)
    # print(values)
    # print(values[0] & (0xffff))
    # print(values[1] & (0xffff))
    if ((values[0] & (0xffff)) == (values[1] & (0xffff))):
      validPairs += 1
    if (i % 1000000 == 0):
      print(i)
      
  print(validPairs)
  
 
if (__name__ == "__main__"):
  main()