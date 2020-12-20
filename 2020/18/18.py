def calculate(input):
  value = 0

  mode = 1 # 1 add, 2 multi
  for i in range(0, len(input)):
    if (type(input[i]) is list):
      if (mode == 1):
        value += calculate(input[i])
      else:
        value *= calculate(input[i])
    elif (input[i] == "+"):
      mode = 1
    elif (input[i] == "*"):
      mode = 2
    else:
      if (mode == 1):
        value += input[i]
      else:
        value *= input[i]
  return value


def parse(line):
  ex = []
  i = 0
  while (i < len(line)):
    if (line[i] == "("):
      r = parse(line[i+1:])
      ex.append(r[0])
      i += r[1]
    elif (line[i] == ")"):
      return (ex, i+1)
    elif (line[i] == "*" or line[i] == "+"):
      ex.append(line[i])
    else:
      ex.append(int(line[i]))
    i += 1
  return (ex, i)


def runFirst(expressions):
  sum = 0
  for ex in expressions:
    sum += calculate(ex)
    #print(calculate(ex))
  return sum


def preprocess(input):
  newEx = []
  i = 0
  while (i < len(input)):
    if (type(input[i]) is list):
      newEx.append(preprocess(input[i]))
    elif (input[i] == "+"):
      newItem = input[i+1]
      if (type(newItem) is list):
        newItem = preprocess(newItem)
      newEx[-1] = [newEx[-1], "+", newItem]
      i += 1
    elif (input[i] == "*"):
      newEx.append(input[i])
    else:
      newEx.append(input[i])
    i += 1
  return newEx


def runSecond(expressions):
  sum = 0
  for ex in expressions:
    # Preprocess expression
    ex = preprocess(ex)
    sum += calculate(ex)
    #print(calculate(ex))
  return sum


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  expressions = []
  for line in input:
    line = line.strip().replace(" ", "")
    expressions.append(parse(line)[0])
    
  result = runFirst(expressions)
  print(result)
  
  result = runSecond(expressions)
  print(result)


if (__name__ == "__main__"):
  main()