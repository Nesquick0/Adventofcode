def runFirst(input):
  lastNum = 0
  nums = {}
  for i in range(len(input)):
    nums[input[i]] = [i]
  lastNum = input[-1]
  for i in range(len(input), 2020):
    if (len(nums[lastNum]) <= 1):
      lastNum = 0
      if (lastNum not in nums):
        nums[lastNum] = []
      nums[lastNum].append(i)
    else:
      diff = nums[lastNum][-1] - nums[lastNum][-2]
      lastNum = diff
      if (diff not in nums):
        nums[diff] = []
      nums[diff].append(i)
  return lastNum


def runSecond(input):
  lastNum = 0
  nums = {0 : []}
  for i in range(len(input)):
    nums[input[i]] = [i]
  lastNum = input[-1]
  for i in range(len(input), 30000000):
    if (len(nums[lastNum]) <= 1):
      lastNum = 0
      #if (lastNum not in nums):
      #  nums[lastNum] = []
      nums[lastNum].append(i)
    else:
      diff = nums[lastNum][-1] - nums[lastNum][-2]
      lastNum = diff
      if (diff not in nums):
        nums[diff] = []
      nums[diff].append(i)
  return lastNum

def main():
  input = [2,0,1,7,4,14,18]
  
  result = runFirst(input)
  print(result)
  
  result = runSecond(input)
  print(result)


if (__name__ == "__main__"):
  main()