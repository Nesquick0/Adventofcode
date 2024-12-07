from itertools import product

class Solver():
    def __init__(self, lines):
        self.lines = lines

    def parseInput(self):
        self.equations = []
        for line in self.lines:
            line = line.strip().split(": ")
            values = list(map(int, line[1].split(" ")))
            self.equations.append([int(line[0]), values])

    def compute(self, values, operators):
        result = values[0]
        for i, operator in enumerate(operators):
            if (operator == 1): # add
                result += values[i+1]
            elif (operator == 2): # multiply
                result *= values[i+1]
            elif (operator == 3): # concatenate
                result = int(str(result) + str(values[i+1]))
        return result

    def tryToSolve(self, result, values):
        numOperators = len(values) - 1
        allPermutations = product([1, 2], repeat = numOperators)
        for operators in allPermutations:
            if (result == self.compute(values, operators)):
                #print(result)
                return result
        return 0

    def part1(self):
        self.parseInput()

        totalSum = 0
        for equation in self.equations:
            result, values = equation
            totalSum += self.tryToSolve(result, values)

        print(totalSum)

    def tryToSolve2(self, result, values):
        numOperators = len(values) - 1
        allPermutations = product([1, 2, 3], repeat = numOperators)
        for operators in allPermutations:
            if (result == self.compute(values, operators)):
                #print(result)
                return result
        return 0

    def part2(self):
        self.parseInput()

        totalSum = 0
        for equation in self.equations:
            result, values = equation
            totalSum += self.tryToSolve2(result, values)

        print(totalSum)



def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    Solver(lines).part1()
    Solver(lines).part2()


if (__name__ == '__main__'):
    main()
