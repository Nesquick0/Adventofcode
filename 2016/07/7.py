import re

def checkCode(text):
  if (len(text) < 4):
    return False
  for i in xrange(0, len(text) - 3):
    if ((text[i] == text[i+3]) and (text[i+1] == text[i+2]) and (text[i] != text[i+1])):
      return True
  return False

def main():
  with open("7.input", "r") as file:
    fileContent = file.readlines()
    
  numberOfTLS = 0

  for line in fileContent:
    line = re.split("(\[[^\[]*\])", line.strip())
    #print(line)
    
    codeExist = False
    codeInBrackets = False
    
    for part in line:
      # In brackets check that special code isn't there.
      if (part[0] == "["):
        if (checkCode(part)):
          codeInBrackets = True
      # Outside of brackets check it is there
      else:
        if (checkCode(part)):
          codeExist = True
    
    if (codeExist and not codeInBrackets):
      numberOfTLS += 1
      
  print(numberOfTLS)

if (__name__ == "__main__"):
  main()