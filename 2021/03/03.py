def findCommonBits(numbers):

    nBits1 = [0] * len(numbers[0])
    nBits0 = [0] * len(numbers[0])
    for number in numbers:
        for i, char in enumerate(number):
            if char == '1':
                nBits1[i] += 1
            else:
                nBits0[i] += 1

    return nBits1, nBits0


def main():
    # Load input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Part 1
    numbers = []
    for line in lines:
        numbers.append(line.strip())

    nBits1, nBits0 = findCommonBits(numbers)

    mostCommonBits = 0
    leastCommonBits = 0
    for i in range(len(nBits1)):
        if nBits1[i] >= nBits0[i]:
            mostCommonBits += 2 ** (len(nBits1) - i - 1)
        else:
            leastCommonBits += 2 ** (len(nBits1) - i - 1)

    print(mostCommonBits)
    print(leastCommonBits)
    print(mostCommonBits * leastCommonBits)

    # Part 2
    numbersOxygen = numbers[:]
    index = 0
    while (len(numbersOxygen) > 1):
        nBits1, nBits0 = findCommonBits(numbersOxygen)
        if (nBits1[index] >= nBits0[index]):
            commonBit = "1"
        else:
            commonBit = "0"

        numbersOxygen = [x for x in numbersOxygen if x[index] == commonBit]
        index = (index + 1) % len(numbersOxygen[0])
    print(int(numbersOxygen[0], 2))

    numbersCO2 = numbers[:]
    index = 0
    while (len(numbersCO2) > 1):
        nBits1, nBits0 = findCommonBits(numbersCO2)
        if (nBits1[index] >= nBits0[index]):
            commonBit = "1"
        else:
            commonBit = "0"

        numbersCO2 = [x for x in numbersCO2 if x[index] != commonBit]
        index = (index + 1) % len(numbersCO2[0])
    print(int(numbersCO2[0], 2))
    print(int(numbersOxygen[0], 2) * int(numbersCO2[0], 2))

if (__name__ == "__main__"):
    main()