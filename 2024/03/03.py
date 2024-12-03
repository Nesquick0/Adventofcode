import re

def part1(lines):
    totalSum = 0
    for line in lines:
        pattern = re.compile(r"mul\((\w+),(\w+)\)")
        for m in pattern.finditer(line):
            x, y = m.group(1), m.group(2)
            totalSum += int(x) * int(y)

    print(totalSum)

def part2(lines):
    totalSum = 0
    state = True
    for line in lines:
        pattern = re.compile(r"(mul\((\w+),(\w+)\)|do\(\)|don't\(\))")
        for m in pattern.finditer(line):
            foundGroup = m.group(1)
            if (foundGroup.startswith("mul")):
                if (state):
                    x, y = m.group(2), m.group(3)
                    totalSum += int(x) * int(y)
            elif (foundGroup == "do()"):
                state = True
            elif (foundGroup == "don't()"):
                state = False
            else:
                print(f"Error {foundGroup}")


    print(totalSum)

def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    part1(lines)
    part2(lines)


if (__name__ == '__main__'):
    main()
