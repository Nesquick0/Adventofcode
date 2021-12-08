'''
1: cf
7: acf
4: bcdf
2: acdeg
3: acdfg
5: abdfg
0: abcefg
6: abdefg
9: abcdfg
8: abcdefg
'''

# Whether base list contains value list
def listContains(base, value):
    for i in value:
        if i not in base:
            return False
    return True


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Part 1
    count = 0
    for line in lines:
        line = line.strip()
        outValues = line.split(" | ")[1].split(" ")
        for i, value in enumerate(outValues):
            if (len(value) == 2): # Number 1
                count += 1
            elif (len(value) == 3): # Number 7
                count += 1
            elif (len(value) == 4): # Number 4
                count += 1
            elif (len(value) == 7): # Number 8
                count += 1

    print(count)

    # Part 2
    outSum = 0
    for line in lines:
        line = line.strip()
        signals, outValues = line.split(" | ")
        signals = list(map(sorted, signals.split(" ")))
        outValues = list(map(sorted, outValues.split(" ")))

        digits = [""] * 10

        # Find digits which are sure by length.
        for i, value in enumerate(signals):
            if (len(value) == 2): # Number 1
                digits[1] = value
            elif (len(value) == 3): # Number 7
                digits[7] = value
            elif (len(value) == 4): # Number 4
                digits[4] = value
            elif (len(value) == 7): # Number 8
                digits[8] = value

        # Find 3 and 9.
        for i, value in enumerate(signals):
            if (len(value) == 5): # Find number 3
                if (listContains(value, digits[7])):
                    digits[3] = value
            elif (len(value) == 6): # Find number 9
                if (listContains(value, digits[4])):
                    digits[9] = value

        # Find 0.
        for i, value in enumerate(signals):
            if (len(value) == 6): # Find number 0
                if (listContains(value, digits[7]) and value != digits[9]):
                    digits[0] = value
        # Last digit with len 6 is 6.
        for i, value in enumerate(signals):
            if (len(value) == 6): # Find number 6
                if (value != digits[0] and value != digits[9]):
                    digits[6] = value

        # Find 5 by comparing to 6 and only 1 segment is different.
        for i, value in enumerate(signals):
            if (len(value) == 5): # Find number 5
                if (listContains(digits[6], value)):
                    digits[5] = value
        # Last digit with len 5 is 2.
        for i, value in enumerate(signals):
            if (len(value) == 5): # Find number 2
                if (value != digits[3] and value != digits[5]):
                    digits[2] = value


        #for i, value in enumerate(digits):
        #    print(f"{i}: {''.join(value)}, ", end="")
        #print("")

        # Translate output values.
        result = ""
        for value in outValues:
            for i, d in enumerate(digits):
                if (value == d):
                    result += str(i)
                    break
        #print(int(result))
        outSum += int(result)
    print(outSum)




if (__name__ == "__main__"):
    main()
