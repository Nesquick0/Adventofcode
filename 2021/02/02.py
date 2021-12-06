def main():
    # Read instuctions from input.txt
    with open('input.txt', 'r') as f:
        instructions = f.readlines()

    # Part 1
    posX = 0
    posY = 0

    for line in instructions:
        line = line.strip()
        if ("forward" in line):
            posX += int(line.split(" ")[1])
        elif ("down" in line):
            posY += int(line.split(" ")[1])
        elif ("up" in line):
            posY -= int(line.split(" ")[1])

    result = posX * posY
    print(result)

    # Part 2
    posX = 0
    posY = 0
    aim = 0

    for line in instructions:
        line = line.strip()
        if ("forward" in line):
            value = int(line.split(" ")[1])
            posX += value
            posY += value * aim
        elif ("down" in line):
            aim += int(line.split(" ")[1])
        elif ("up" in line):
            aim -= int(line.split(" ")[1])

    result = posX * posY
    print(result)


if (__name__ == "__main__"):
    main()