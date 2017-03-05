def main():
  with open("2.input", "r") as file:
    fileContent = file.readlines()
    
  #     1
  #   2 3 4
  # 5 6 7 8 9
  #   A B C
  #     D
  button = 5
  code = ""
    
  for line in fileContent:
    line = line.strip()
    for instr in line:
      if (instr == "U"):
        if (button not in (5, 2, 1, 4, 9)):
          if (button >= 5 and button <= 12):
            button -= 4
          else:
            button -= 2
          
      elif (instr == "D"):
        if (button not in (5, 10, 13, 12, 9)):
          if (button >= 2 and button <= 9):
            button += 4
          else:
            button += 2
          
      elif (instr == "R"):
        if (button not in (1, 4, 9, 12, 13)):
          button += 1
          
      elif (instr == "L"):
        if (button not in (1, 2, 5, 10, 13)):
          button -= 1
      else:
        print("wrong instruction")
        
    code += hex(button)[2:].capitalize()
  
  print(code)

if (__name__ == "__main__"):
  main()