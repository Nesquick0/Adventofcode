from collections import defaultdict

def main():
  with open("input", "r") as file:
    input = file.readlines()
    
  progs = defaultdict(list)
  for line in input:
    line = line.strip().split(" ")
    for prg in line[2:]:
      progs[int(line[0])].append(int(prg.replace(",", "")))
    
  checkList = [0]
  checked = set()
  while (len(checkList) > 0):
    item = checkList.pop()
    if (item in checked):
      continue
    
    checked.add(item)
    checkList.extend(progs[item])
      
  print(len(checked))
 
if (__name__ == "__main__"):
  main()