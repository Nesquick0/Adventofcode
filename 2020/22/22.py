from collections import deque

def runFirst(deck1, deck2):
  pl1 = deque(deck1)
  pl2 = deque(deck2)

  while (len(pl1) > 0 and len(pl2) > 0):
    n1 = pl1.popleft()
    n2 = pl2.popleft()
    if (n1 > n2):
      pl1.append(n1)
      pl1.append(n2)
    else:
      pl2.append(n2)
      pl2.append(n1)

  score = 0
  winList = list(reversed(list(pl1) if (len(pl1) > 0) else list(pl2)))
  for i in range(len(winList)):
    score += winList[i]*(i+1)
  return score


def playGame(deck1, deck2):
  pl1 = list(deck1)
  pl2 = list(deck2)
  states = set()

  while (len(pl1) > 0 and len(pl2) > 0):
    # Compare to previous.
    state = ( tuple(pl1), tuple(pl2) )
    if (state in states):
      return 1, 0
    states.add(state)

    # Draw
    n1 = pl1.pop(0)
    n2 = pl2.pop(0)

    # Recurse
    if (len(pl1) >= n1 and len(pl2) >= n2):
      winnerSubGame = playGame(pl1[:n1], pl2[:n2])[0]
      if (winnerSubGame == 1):
        pl1.append(n1)
        pl1.append(n2)
      else:
        pl2.append(n2)
        pl2.append(n1)
      continue

    if (n1 > n2):
      pl1.append(n1)
      pl1.append(n2)
    else:
      pl2.append(n2)
      pl2.append(n1)

  score = 0
  winList = list(reversed(list(pl1) if (len(pl1) > 0) else list(pl2)))
  for i in range(len(winList)):
    score += winList[i]*(i+1)
  return 1 if (len(pl1) > 0) else 2, score

def runSecond(deck1, deck2):
  return playGame(deck1, deck2)


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  deck1 = []
  deck2 = []
  mode = 1
  for line in input:
    line = line.strip()
    if (not line):
      continue
    if ("Player 1:" in line):
      continue
    if ("Player 2:" in line):
      mode = 2
      continue
    if (mode == 1):
      deck1.append(int(line))
    else:
      deck2.append(int(line))

  result = runFirst(deck1, deck2)
  print(result)
  
  result = runSecond(deck1, deck2)
  print(result)


if (__name__ == "__main__"):
  main()