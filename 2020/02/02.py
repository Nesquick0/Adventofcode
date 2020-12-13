class pwdStruct:
  minC = 0
  maxC = 0
  character = ""
  pwdStr = ""
  
  def __init__(self, minC, maxC, character, pwdStr):
    self.minC = minC
    self.maxC = maxC
    self.character = character
    self.pwdStr = pwdStr


def runFirst(pwds):
  valid = 0
  for pwd in pwds:
    n = pwd.pwdStr.count(pwd.character)
    if (n >= pwd.minC and n <= pwd.maxC):
      valid += 1
  return valid

def runSecond(pwds):
  valid = 0
  for pwd in pwds:
    n = 1 if pwd.pwdStr[pwd.minC-1] == pwd.character else 0
    n += 1 if pwd.pwdStr[pwd.maxC-1] == pwd.character else 0
    if (n == 1):
      valid += 1
  return valid


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  pwds = []
  for line in input:
    lineSplit = line.strip().split(" ")
    character = lineSplit[1][0]
    minC, maxC = lineSplit[0].split("-")
    pwdStr = lineSplit[-1]
    pwd = pwdStruct(int(minC), int(maxC), character, pwdStr)
    pwds.append(pwd)

  result = runFirst(pwds)
  print(result)
      
  result = runSecond(pwds)
  print(result)

if (__name__ == "__main__"):
  main()