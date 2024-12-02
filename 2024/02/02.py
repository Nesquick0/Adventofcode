def IsSafe(numbers):
    direction = numbers[1] - numbers[0]
    for i in range(len(numbers)-1):
        step = numbers[i+1] - numbers[i]
        if (abs(step) >= 1 and abs(step) <= 3 and step * direction > 0):
            pass
        else:
            return False

    return True

def part1(lines):
    numSafe = 0
    for line in lines:
        line = list(map(int, line.strip().split(" ")))
        if (IsSafe(line)):
            numSafe += 1

    print(numSafe)

def part2(lines):
    numSafe = 0
    for line in lines:
        line = list(map(int, line.strip().split(" ")))

        if (IsSafe(line)):
            numSafe += 1
        else:
            # Try to remove one item:
            if (IsSafe(line[1:])):
                numSafe += 1
            elif (IsSafe(line[:-1])):
                numSafe += 1
            else:
                for i in range(1, len(line)-1):
                    newLine = line[:i] + line[i+1:]
                    if (IsSafe(newLine)):
                        numSafe += 1
                        break

    print(numSafe)


def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    part1(lines)
    part2(lines)


if (__name__ == '__main__'):
    main()
