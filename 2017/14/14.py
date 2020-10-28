# Code from 10s
def hash(input):
  input = list(map(ord, list(input)))
  input += [17, 31, 73, 47, 23]
  
  sequence = list(range(256))
  curPos = 0
  skipSize = 0
  
  # Calculate sparse hash.
  for round in range(64):
    for length in input:
      seqCopy = sequence[:]*3
      subSeq = list(reversed(seqCopy[curPos:curPos+length]))
      for i in range(length):
        sequence[(curPos+i) % len(sequence)] = subSeq[i]
      
      curPos = (curPos + length + skipSize) % len(sequence)
      skipSize += 1
    
  # Calculate dense hash.
  denseHash = []
  for i in range(16):
    hashNumber = sequence[0 + i*16]
    for j in range(1, 16):
      hashNumber = hashNumber ^ sequence[j + i*16]
    denseHash.append(hashNumber)
  return denseHash
    

def main():
  #input = "flqrgnkx"
  input = "xlqgujun"
  nCount = 128
  data = [0]*nCount*nCount
  
  for row in range(nCount):
    valueHash = hash(input + ("-%d" % (row)))
    # binString = "".join("{:08b}".format(x) for x in valueHash)
    # for i in range(nCount):
      # data[row*nCount+i] = 1 if (binString[i] == "1") else 0
    for i in range(len(valueHash)):
      for b in range(8):
        data[row*nCount+i*8+b] = 1 if (valueHash[i] & 1<<(7-b)) else 0
    
    
  for x in range(8):
    for y in range(8):
      if (data[x*nCount+y] == 1):
        print("#", end="")
      else:
        print(".", end="")
    print("")
    
    
  # Part 1
  usedSqr = 0
  for x in range(nCount):
    for y in range(nCount):
      if (data[x*nCount+y] == 1):
        usedSqr += 1
  
  print(usedSqr)
  
  # Part 2
  regionCounter = 0
  dataR = [0]*nCount*nCount
  for x in range(nCount):
    for y in range(nCount):
      index = x*nCount+y
      if (data[index] == 1 and dataR[index] == 0):
        regionCounter += 1
        # Used square. Try to find already existing region.
        checkList = [index]
        checked = set()
        
        # Depth first search
        while (len(checkList) > 0):
          newIndex = checkList.pop()
          if (newIndex in checked):
            continue
          if (data[newIndex] == 0):
            continue
          checked.add(newIndex)
          dataR[newIndex] = regionCounter
          newX, newY = (newIndex // nCount), (newIndex % nCount)
          if (newX > 0):
            checkList.append((newX-1)*nCount+newY)
          if (newX < nCount-1):
            checkList.append((newX+1)*nCount+newY)
          if (newY > 0):
            checkList.append(newX*nCount+(newY-1))
          if (newY < nCount-1):
            checkList.append(newX*nCount+(newY+1))
          
  for x in range(8):
    for y in range(8):
      if (dataR[x*nCount+y] >= 1):
        print(dataR[x*nCount+y], end="")
      else:
        print(".", end="")
    print("")
    
  print(regionCounter)
  
 
if (__name__ == "__main__"):
  main()