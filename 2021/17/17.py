import re

def simulate(areaS, areaE, initSpd) -> bool:
    spdX, spdY = initSpd
    posX, posY = (0, 0)

    while True:
        posX += spdX
        posY += spdY
        if (spdX > 0):
            spdX -= 1
        spdY -= 1

        if (posX > areaE[0] or posY < areaE[1]):
            return False

        if (posX >= areaS[0] and posY <= areaS[1]):
            return True


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    m = re.match(r'^target area: x=([-\d]+)\.\.+([-\d]+), y=([-\d]+)\.\.+([-\d]+)$', lines[0])
    areaS = (int(m.group(1)), int(m.group(4)))
    areaE = (int(m.group(2)), int(m.group(3)))
    print(areaS, areaE)

    # Part 1
    maxSpdY = (0 - areaE[1] - 1)
    topHeight = int((maxSpdY + 1) * (maxSpdY / 2))
    print(topHeight)

    # Part 2
    speedRangeX = (0, areaE[0])
    speedRangeY = (areaE[1], maxSpdY)
    print(speedRangeX, speedRangeY)

    counter = 0
    for x in range(speedRangeX[0], speedRangeX[1] + 1):
        for y in range(speedRangeY[0], speedRangeY[1] + 1):
            if (simulate(areaS, areaE, (x, y))):
                counter += 1
                #print(f"{x},{y}")

    print(counter)




if (__name__ == "__main__"):
    main()
