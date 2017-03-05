def main():
  with open("2.input", "r") as file:
    fileContent = file.readlines()
    
  # 1 2 3
  # 4 5 6
  # 7 8 9
  button = 5
  code = ""
    
  for line in fileContent:
    line = line.strip()
    for instr in line:
      if (instr == "U"):
        if (button > 3):
          button -= 3
      elif (instr == "D"):
        if (button < 7):
          button += 3
      elif (instr == "R"):
        if (button not in (3,6,9)):
          button += 1
      elif (instr == "L"):
        if (button not in (1,4,7)):
          button -= 1
      else:
        print("wrong instruction")
        
    code += str(button)
  
  print(code)

if (__name__ == "__main__"):
  main()