def findLoop(publicKey, subjNum):
  value = 1
  loopSize = 0
  while (True):
    value *= subjNum
    value = value % 20201227
    loopSize += 1
    if (value == publicKey):
      return loopSize


def getEncryption(publicKey, loopSize):
  value = 1
  for i in range(loopSize):
    value *= publicKey
    value = value % 20201227
  return value


def runFirst(publicKeys):
  cardLoop = findLoop(publicKeys[0], 7)
  doorLoop = findLoop(publicKeys[1], 7)
  print(cardLoop, doorLoop, 7)
  result1 = getEncryption(publicKeys[0], doorLoop)
  result2 = getEncryption(publicKeys[1], cardLoop)
  return result1


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  #publicKeys = [5764801, 17807724]
  publicKeys = [11562782, 18108497]

  result = runFirst(publicKeys)
  print(result)


if (__name__ == "__main__"):
  main()
