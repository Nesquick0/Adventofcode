def main():
  #input = "1,2,3"
  input = "14,58,0,116,179,16,1,104,2,254,167,86,255,55,122,244"
  input = list(map(ord, list(input)))
  input += [17, 31, 73, 47, 23]
  print(input)
  
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
    
  print(denseHash)
  print("".join("%02x" %i for i in denseHash))
  

if (__name__ == "__main__"):
  main()