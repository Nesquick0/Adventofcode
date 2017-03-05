def swapPos(text, x, y):
  tmp = text[x]
  text[x] = text[y]
  text[y] = tmp
  return text
  
def swapChars(text, x, y):
  for i in xrange(len(text)):
    if (text[i] == x):
      text[i] = y
    elif (text[i] == y):
      text[i] = x
  return text
  
def reverse(text, x, y):
  y += 1
  return text[:x] + list(reversed(text[x:y])) + text[y:]
  
def rotate(text, count):
  count = count % len(text)
  return text[-count:] + text[:-count]
  
def rotateBased(text, char):
  index = text.index(char)
  if (index < 4):
    return rotate(text, index + 1)
  else:
    return rotate(text, index + 2)
  
def move(text, x, y):
  if (x <= y):
    return text[:x] + text[x+1:y+1] + [text[x]] + text[y+1:]
  else:
    return text[:y] + [text[x]] + text[y:x] + text[x+1:]
  

def main():
  with open("21.input", "r") as file:
    fileContent = file.readlines()
    
  # password = list("abcde")
  # password = swapPos(password, 4, 0)
  # print(password)
  # password = swapChars(password, "d", "b")
  # print(password)
  # password = reverse(password, 0, 4)
  # print(password)
  # password = rotate(password, -1)
  # print(password)
  # password = move(password, 1, 4)
  # print(password)
  # password = move(password, 3, 0)
  # print(password)
  # password = rotateBased(password, "b")
  # print(password)
  # password = rotateBased(password, "d")
  # print(password)
  
  password = list("abcdefgh")
  
  for line in fileContent:
    line = line.strip()
    instr = line.split(" ")
    if ("rotate right" in line):
      password = rotate(password, int(instr[2]))
    elif ("rotate left" in line):
      password = rotate(password, -int(instr[2]))
    elif ("swap position" in line):
      password = swapPos(password, int(instr[2]), int(instr[5]))
    elif ("swap letter" in line):
      password = swapChars(password, instr[2], instr[5])
    elif ("rotate based" in line):
      password = rotateBased(password, instr[6])
    elif ("reverse positions" in line):
      password = reverse(password, int(instr[2]), int(instr[4]))
    elif ("move position" in line):
      password = move(password, int(instr[2]), int(instr[5]))
  
  print("".join(password))

if (__name__ == "__main__"):
  main()