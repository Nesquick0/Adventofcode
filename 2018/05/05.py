import string

def collapse(input):
  lastIndex = 0
  while True:
    found = False
    #print(input)
    for i in range(lastIndex, len(input)-1):
      char1 = input[i]
      char2 = input[i+1]
      if (char1.lower() == char2.lower() and
        ((char1.islower() and not char2.islower()) or (not char1.islower() and char2.islower())) ):
          input.pop(i)
          input.pop(i)
          found = True
          lastIndex = max(0, i-1)
          break

    if (not found):
      break

def main():
  with open("input.txt", "r") as file:
    input = list(file.readline().strip())

  # First
  collapse(input)
  print(len(input))

  # Second
  shortest = len(input)
  chars = list(string.ascii_lowercase)
  for char in chars:
    inputCopy = list(filter(lambda x: x.lower() != char, input))
    
    collapse(inputCopy)
    print(char, len(inputCopy))

    if (len(inputCopy) < shortest):
      shortest = len(inputCopy)

  print(shortest)


if (__name__ == "__main__"):
  main()