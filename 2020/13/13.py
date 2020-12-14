import math

def runFirst(timeStamp, buses):
  minDelay = timeStamp
  bestId = 0
  for bus in buses:
    delay = bus - (timeStamp % bus)
    if (delay < minDelay):
      minDelay = delay
      bestId = bus
  return minDelay * bestId


def lcm(nums):
  num = nums[0]
  for i in range(1, len(nums)):
    num = (num * nums[i]) // math.gcd(num, nums[i])
  return num


def runSecond(buses):
  buses[0][1] = buses[0][0]
  timeStamp = buses[0][0]
  step = buses[0][0]

  # Find steps
  foundTime = 0
  for i in range(1, len(buses)):
    foundTime = 0
    while True:
      timeStamp += step
      if (buses[i][0] - (timeStamp % buses[i][0]) == (buses[i][1] % buses[i][0])):
        print(timeStamp, step, foundTime)
        if (foundTime):
          step = timeStamp - foundTime
          break
        else:
          foundTime = timeStamp
  return foundTime


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
  
  timeStamp = int(input[0])
  buses = sorted(list(map(int, filter(lambda x: x != "x", input[1].strip().split(",")) )))
  result = runFirst(timeStamp, buses)
  print(result)
      
  busesInput = input[1].strip().split(",")
  buses = []
  for i in range(len(busesInput)):
    if (busesInput[i] != "x"):
      buses.append([int(busesInput[i]), i])
  result = runSecond(buses)
  print(result)


if (__name__ == "__main__"):
  main()