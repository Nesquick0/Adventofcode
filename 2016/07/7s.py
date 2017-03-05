import re

def checkFormat(seq):
  if (len(seq) != 3):
    return False
  if ((seq[0] == seq[2]) and (seq[0] != seq[1])):
    return True
  return False

def getSequences(text):
  if (len(text) < 3):
    return []
    
  result = []
  for i in xrange(0, len(text) - 2):
    if (checkFormat(text[i:i+3])):
      result.append(text[i:i+3])
      
  return result
  
def checkSequences(first, second):
  if ((first[0] == second[1]) and (first[1] == second[0])):
    return True
  return False

def main():
  with open("7.input", "r") as file:
    fileContent = file.readlines()
    
  numberOfSSL = 0

  for line in fileContent:
    line = re.split("(\[[^\[]*\])", line.strip())
    #print(line)
    
    sequences = []
    sequencesInBrackets = []
    
    # Find all SSL sequences.
    for part in line:
      if (part[0] == "["):
        sequencesInBrackets += getSequences(part)
      else:
        sequences += getSequences(part)
    
    sslFound = False
    for seq1 in sequences:
      for seq2 in sequencesInBrackets:
        if (checkSequences(seq1, seq2)):
          sslFound = True
          
    if (sslFound):
      numberOfSSL += 1
      
  print(numberOfSSL)

if (__name__ == "__main__"):
  main()