def main():
  #input = "3, 4, 1, 5"
  input = "14,58,0,116,179,16,1,104,2,254,167,86,255,55,122,244"
  input = list(map(int, map(str.strip, input.split(","))))
  
  sequence = list(range(256))
  curPos = 0
  skipSize = 0
  
  for length in input:
    seqCopy = sequence[:]*3
    subSeq = list(reversed(seqCopy[curPos:curPos+length]))
    for i in range(length):
      sequence[(curPos+i) % len(sequence)] = subSeq[i]
    
    curPos = (curPos + length + skipSize) % len(sequence)
    skipSize += 1
    
  print(sequence[0] * sequence[1])
  

if (__name__ == "__main__"):
  main()