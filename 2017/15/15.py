def genNew(oldValues):
  genFactor = [16807, 48271]
  values = [0,0]
  values[0] = oldValues[0] * genFactor[0] % 2147483647
  values[1] = oldValues[1] * genFactor[1] % 2147483647
  return values
  

def main():
  #startGen = [65, 8921]
  startGen = [699, 124]
  
  values = startGen[:]
  validPairs = 0
  for i in range(40000000):
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