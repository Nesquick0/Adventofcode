import re

class Main():
  def __init__(self):
    self.registers = [0] * 4
    self.operations = {}


  def doOperation(self, operation, operType, registers):
    result = registers[:]
    A, B, C = operation[1], operation[2], operation[3]

    if (operType == "addr"):
      result[C] = registers[A] + registers[B]
    elif (operType == "addi"):
      result[C] = registers[A] + B

    elif (operType == "mulr"):
      result[C] = registers[A] * registers[B]
    elif (operType == "muli"):
      result[C] = registers[A] * B

    elif (operType == "banr"):
      result[C] = registers[A] & registers[B]
    elif (operType == "bani"):
      result[C] = registers[A] & B

    elif (operType == "borr"):
      result[C] = registers[A] | registers[B]
    elif (operType == "bori"):
      result[C] = registers[A] | B

    elif (operType == "setr"):
      result[C] = registers[A]
    elif (operType == "seti"):
      result[C] = A

    elif (operType == "gtir"):
      result[C] = 1 if (A > registers[B]) else 0
    elif (operType == "gtri"):
      result[C] = 1 if (registers[A] > B) else 0
    elif (operType == "gtrr"):
      result[C] = 1 if (registers[A] > registers[B]) else 0

    elif (operType == "eqir"):
      result[C] = 1 if (A == registers[B]) else 0
    elif (operType == "eqri"):
      result[C] = 1 if (registers[A] == B) else 0
    elif (operType == "eqrr"):
      result[C] = 1 if (registers[A] == registers[B]) else 0

    return result


  def checkOperation(self, operation, before, after):
    operations = []
    checkOpers = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori",
      "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

    for oper in checkOpers:
      if (self.doOperation(operation, oper, before) == after):
        operations.append(oper)

    return operations


  def run(self):
    with open("input.txt", "r") as file:
      input = file.readlines()

    for i in range(16):
      self.operations[i] = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori",
        "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

    # Part 1
    like3OrMore = 0
    i = 0
    lastSample = 0
    while i < len(input):
      line = input[i]
      if ("Before" in line):
        before = line.strip()
        operation = input[i+1].strip()
        after = input[i+2].strip()

        m = re.match(r"Before: \[(\d), (\d), (\d), (\d)\]", before)
        before = list(map(int, [m.group(1), m.group(2), m.group(3), m.group(4)]))

        m = re.match(r"After:  \[(\d), (\d), (\d), (\d)\]", after)
        after = list(map(int, [m.group(1), m.group(2), m.group(3), m.group(4)]))

        operation = list(map(int, operation.split(" ")))
        
        validOper = self.checkOperation(operation, before, after)
        if (len(validOper) >= 3):
          like3OrMore += 1

        # Filter operations
        self.operations[operation[0]] = list(filter(lambda x: x in validOper, self.operations[operation[0]]))

        i += 2
        lastSample = i+1

      i += 1

    print(like3OrMore)

    # Part 2
    # Filter known operations
    for i in range(16):
      for operIndex in range(16):
        oper = self.operations[operIndex]
        if (len(oper) == 1):
          knownOper = oper[0]
          for j in range(16):
            if (j != operIndex and knownOper in self.operations[j]):
              self.operations[j].remove(knownOper)

    # Run test program
    i = lastSample
    while i < len(input):
      line = input[i].strip()
      if (line):
        operation = list(map(int, line.split(" ")))
        self.registers = self.doOperation(operation, self.operations[operation[0]][0], self.registers)
      i += 1

    print(self.registers)
      

if (__name__ == "__main__"):
  Main().run()