import re

def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  input.sort()
  guards = {}

  guardId = -1
  pattern = re.compile(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)")
  for line in input:
    m = pattern.match(line)
    if (m):
      text = m.group(6)
      minute = int(m.group(5))
      if ("#" in text):
        guardId = int(text.split(" ")[1][1:])
        if (guardId not in guards):
          guards[guardId] = []
      elif ("falls asleep" == text):
        guards[guardId].append( [minute, 0] )
      elif ("wakes up" == text):
        guards[guardId][-1][1] = minute
      else:
        print("error", text)
    else:
      print("error", line)

  maxTime = [-1, 0]
  bestMinute = -1
  for guardId in guards:
    #print(guards[guardId])
    sumDur = 0
    for timer in guards[guardId]:
      sumDur += timer[1] - timer[0]
    if (sumDur > maxTime[1]):
      maxTime[0] = guardId
      maxTime[1] = sumDur

  print(maxTime)

  minutes = 60*[0]
  for timer in guards[maxTime[0]]:
    for i in range(timer[0], timer[1]):
      minutes[i] += 1

  maxMinute = 0
  for i in range(len(minutes)):
    if (minutes[i] > maxMinute):
      bestMinute = i
      maxMinute = minutes[i]

  print(bestMinute)
  print("Result1: %d" % (maxTime[0] * bestMinute))

  # Part 2

  bestGuard = [-1, 0, -1]
  for guardId in guards:
    minutes = 60*[0]
    for timer in guards[guardId]:
      for i in range(timer[0], timer[1]):
        minutes[i] += 1

    maxMinute = 0
    bestMinute = -1
    for i in range(len(minutes)):
      if (minutes[i] > maxMinute):
        bestMinute = i
        maxMinute = minutes[i]

    if (maxMinute > bestGuard[1]):
      bestGuard[0] = guardId
      bestGuard[1] = maxMinute
      bestGuard[2] = bestMinute

  print(bestGuard)
  print("Result2: %d" % (bestGuard[0] * bestGuard[2]))


if (__name__ == "__main__"):
  main()