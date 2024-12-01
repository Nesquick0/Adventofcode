import re

def part1(lines):
    pattern = re.compile(r"(\d+)\s+(\d+)")

    list1 = []
    list2 = []
    for line in lines:
        if (m := pattern.match(line)):
            a, b = int(m.group(1)), int(m.group(2))
            list1.append(a)
            list2.append(b)

    list1.sort()
    list2.sort()

    sumError = 0
    for i, _ in enumerate(list1): 
        sumError += abs(list1[i] - list2[i])

    print(sumError)

def part2(lines):
    pattern = re.compile(r"(\d+)\s+(\d+)")

    numbers = []
    howMany = {}
    for line in lines:
        if (m := pattern.match(line)):
            a, b = int(m.group(1)), int(m.group(2))
            numbers.append(a)
            if (b not in howMany):
                howMany[b] = 0
            howMany[b] += 1

    similarity = 0
    for i, n in enumerate(numbers):
        if (n in howMany):
            similarity += n * howMany[numbers[i]]

    print(similarity)

def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    part1(lines)
    part2(lines)


if (__name__ == '__main__'):
    main()
