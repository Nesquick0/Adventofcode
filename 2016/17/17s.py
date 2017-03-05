import hashlib

def isOpen(char):
  value = int(char, 16)
  if (value > 10):
    return True
  else:
    return False
    
def options(passcode):
  hash = hashlib.md5(passcode).hexdigest()
  # Up, Down, Left, Right
  return (isOpen(hash[0]), isOpen(hash[1]), isOpen(hash[2]), isOpen(hash[3]))

def main():
  passcodeOrig = "pxxbnzuo"
  
  states = [ (0, passcodeOrig) ]
  targetPos = 15
  longestPath = 0
  
  while (len(states) > 0):
    state = states.pop(0)
    pos, passcode = state
    
    if (pos == targetPos):
      if ((len(passcode) - len(passcodeOrig)) > longestPath):
        longestPath = (len(passcode) - len(passcodeOrig))
      continue
    
    option = options(passcode)
    if (option[0]): # Up
      if (pos > 3):
        states.append( (pos - 4, passcode + "U") )
    if (option[1]): # Down
      if (pos < 12):
        states.append( (pos + 4, passcode + "D") )
    if (option[2]): # Left
      if ((pos % 4) > 0):
        states.append( (pos - 1, passcode + "L") )
    if (option[3]): # Right
      if ((pos % 4) < 3):
        states.append( (pos + 1, passcode + "R") )
  
  print(longestPath)
  
if (__name__ == "__main__"):
  main()