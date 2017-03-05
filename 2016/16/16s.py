def createData(data):
  newData = data[::-1]
  newData = newData.replace("0", "2").replace("1", "0").replace("2", "1")
  return data + "0" + newData
  
def generateData(sample, length):
  data = sample[:]
  while (len(data) < length):
    data = createData(data)
    
  return data[:length]

def main():
  diskLength = 35651584
  sample = "10010000000110000"
  
  data = generateData(sample, diskLength)
  
  checkSum = data[:]
  while ((len(checkSum) % 2) == 0):
    newCheckSum = ""
    for i in xrange(0, len(checkSum), 2):
      if (checkSum[i] == checkSum[i+1]):
        newCheckSum += "1"
      else:
        newCheckSum += "0"
        
    checkSum = newCheckSum
    
  print(checkSum)

if (__name__ == "__main__"):
  main()