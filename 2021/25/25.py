def draw(world, sizeX, sizeY):
    for y in range(sizeY):
        for x in range(sizeX):
            value = world[y * sizeX + x]
            if (value == 0):
                print(".", end='')
            elif (value == 1):
                print(">", end='')
            elif (value == 2):
                print("v", end='')
        print()
    print()

def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    sizeX = len(lines[0].strip())
    sizeY = len(lines)
    world = [0] * sizeY * sizeX
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if (char == "."):
                pass
            elif (char == ">"):
                world[y * sizeX + x] = 1
            elif (char == "v"):
                world[y * sizeX + x] = 2
            else:
                raise Exception("Bad char")

    print(world.count(1))
    print(world.count(2))
    draw(world, sizeX, sizeY)

    lastStep = 0
    while True:
        movement = False
        # Simulate right.
        newWorld = [0] * sizeY * sizeX
        for y in range(sizeY):
            for x in range(sizeX):
                if (world[y * sizeX + x] == 1):
                    nextX = (x+1)%sizeX
                    if (world[y * sizeX + nextX] == 0):
                        newWorld[y * sizeX + nextX] = 1
                        movement = True
                    else:
                        newWorld[y * sizeX + x] = 1
                elif (world[y * sizeX + x] == 2):
                    newWorld[y * sizeX + x] = 2
        world = newWorld

        # Simulate down.
        newWorld = [0] * sizeY * sizeX
        for y in range(sizeY):
            for x in range(sizeX):
                if (world[y * sizeX + x] == 2):
                    nextY = (y+1)%sizeY
                    if (world[nextY * sizeX + x] == 0):
                        newWorld[nextY * sizeX + x] = 2
                        movement = True
                    else:
                        newWorld[y * sizeX + x] = 2
                elif (world[y * sizeX + x] == 1):
                    newWorld[y * sizeX + x] = 1
        world = newWorld

        #draw(world, sizeX, sizeY)

        lastStep += 1
        if (not movement):
            break

    print(f"Last step: {lastStep}")


if (__name__ == "__main__"):
    main()
