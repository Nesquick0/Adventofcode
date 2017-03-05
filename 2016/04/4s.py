def convert(char, id):
  ordA = ord("a")
  ordZ = ord("z") + 1
  
  return chr(((ord(char) + id - ordA) % (ordZ - ordA)) + ordA)

def main():
  with open("4.input", "r") as file:
    fileContent = file.readlines()

  for line in fileContent:
    line = line.strip().split("[")
    checkSum = line[1][:-1]
    line = line[0].split("-")
    roomId = int(line[-1])
    roomCode = "".join(line[:-1])
    
    decryptRoomCode = ""
    for char in roomCode:
      decryptRoomCode += convert(char, roomId)
    
    if (decryptRoomCode == "northpoleobjectstorage"):
      print(roomId)
  

if (__name__ == "__main__"):
  main()