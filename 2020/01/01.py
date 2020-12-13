def runFirst(input):
  numbers = {}
  for line in input:
    number = int(line)
    target = 2020 - number
    if (target in numbers):
      return target * number
    numbers[number] = 1

def runSecond(input):
  numbers = {}
  for line in input:
    num1 = int(line)

    for num2 in numbers:
      target = 2020 - num1 - num2
      if (target in numbers):
        return target * num1 * num2
    numbers[num1] = 1


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()
      
  result = runFirst(input)
  print(result)
      
  result = runSecond(input)
  print(result)

if (__name__ == "__main__"):
  main()