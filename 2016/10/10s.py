def main():
  with open("10.input", "r") as file:
    fileContent = file.readlines()
    
  bots = {}
  botValues = {}
  outputs = {}
  
  # Load instruction first
  for line in fileContent:
    line = line.strip()
    if ("gives" in line):
      instr = line.split(" ")
      instr[5] = instr[5][0]
      instr[10] = instr[10][0]
      bots[int(instr[1])] = ( (instr[5], int(instr[6])), (instr[10], int(instr[11])))
    else:
      instr = line.split(" ")
      value = int(instr[1])
      bot = int(instr[5])
      if (bot not in botValues):
        botValues[bot] = []
      botValues[bot].append(value)
      
  #print(bots)
  #print(botValues)
  
  done = False
  while (not done):
    done = True
    
    for bot in botValues:
      values = botValues[bot]
      if (len(values) == 2):
        done = False
        
        instr = bots[bot]
        lower = min(values[0], values[1])
        higher = max(values[0], values[1])
        if (lower == 17 and higher == 61):
          print(bot)
        
        targetL = instr[0][1]
        targetH = instr[1][1]
        
        if (instr[0][0] == "b"):
          if (targetL not in botValues):
            botValues[targetL] = []
          botValues[targetL].append(lower)
        else:
          if (targetL not in outputs):
            outputs[targetL] = []
          outputs[targetL].append(lower)
          
        if (instr[1][0] == "b"):
          if (targetH not in botValues):
            botValues[targetH] = []
          botValues[targetH].append(higher)
        else:
          if (targetH not in outputs):
            outputs[targetH] = []
          outputs[targetH].append(higher)
        
        botValues[bot] = []
        break
  
  print(outputs)
  print(outputs[0][0] * outputs[1][0] * outputs[2][0])
    
  
if (__name__ == "__main__"):
  main()