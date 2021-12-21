class Scanner:
    def __init__(self, number):
        self.beacons = []
        self.number = number

        self.allPos = []
        self.correctRotIndex = -1
        self.realPos = None
        self.offset = None

    def generateRotations(self):
        self.allPos = []

        self.allPos.append( list(map(lambda p: ( p[0],  p[1],  p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: (-p[0],  p[1],  p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: ( p[0], -p[1],  p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: (-p[0], -p[1],  p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: ( p[0],  p[1], -p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: (-p[0],  p[1], -p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: ( p[0], -p[1], -p[2]), self.beacons[:] )))
        self.allPos.append( list(map(lambda p: (-p[0], -p[1], -p[2]), self.beacons[:] )))

        for i in range(8):
            self.allPos.append( list(map(lambda p: ( p[1],  p[0],  p[2]), self.allPos[i][:] )))
        for i in range(8):
            self.allPos.append( list(map(lambda p: ( p[0],  p[2],  p[1]), self.allPos[i][:] )))
        for i in range(8):
            self.allPos.append( list(map(lambda p: ( p[2],  p[1],  p[0]), self.allPos[i][:] )))
        for i in range(8):
            self.allPos.append( list(map(lambda p: ( p[2],  p[0],  p[1]), self.allPos[i][:] )))
        for i in range(8):
            self.allPos.append( list(map(lambda p: ( p[1],  p[2],  p[0]), self.allPos[i][:] )))

        # for i in range(len(self.allPos)):
        #     for j in range(len(self.allPos)):
        #         if (i == j):
        #             continue
        #         if (self.allPos[i][4] == self.allPos[j][4]):
        #             print(f"{i} {j}")
        #             break
        # for i in range(len(self.allPos)):
        #     print(f"\nTest {i}")
        #     for pos in range(len(self.allPos[i])):
        #         print(f"{self.allPos[i][pos][0]},{self.allPos[i][pos][1]},{self.allPos[i][pos][2]}")


def posAdd(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1], pos1[2] + pos2[2])


def posSub(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2])


def dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])


def compare(first: Scanner, second: Scanner):
    testPositions = first.beacons
    # For each pos in original beacons position. Try to find base beacon from first scanner.
    for testPos in testPositions:
        # For each rotation of second scanner. Have to check for every rotation of second scanner.
        for secIndex, secBeacons in enumerate(second.allPos):
            # For each position of second scanner. Try to fit every beacon of second scanner to test position.
            for secPos in secBeacons:
                diff = 0
                offset = posSub(testPos, secPos)

                # For each pos in second beacons position.
                for _firstPosIndex, firstPos in enumerate(testPositions):
                    for pos in secBeacons:
                        if (firstPos == posAdd(pos, offset)):
                            diff += 1
                            if (diff >= 12):
                                #print(f"Found {diff}, {offset}, {secIndex}, {i}")
                                return (diff, offset, secIndex)

    # return (diffMax, bestOffset, correctRotIndex)
    return (0, None, None)


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    scanners = []
    scanner = None
    for i in range(len(lines)):
        line = lines[i].strip()
        if ("scanner" in line):
            scanner = Scanner(int(line.split(" ")[2]))
            scanners.append(scanner)
            continue
        if (not line):
            continue
        x, y, z = list(map(int, line.split(",")))
        scanner.beacons.append((x, y, z))

    for scanner in scanners:
        scanner.generateRotations()

    # Part 1
    scanners[0].realPos = (0, 0, 0)
    scanners[0].offset = (0, 0, 0)
    scanners[0].correctPos = 0

    #for i in range(len(scanners)):
    #    for j in range(i, len(scanners)):
    testPool = list(range(1, len(scanners)))
    checkedPool = [0]
    while (testPool):
        checkSize = len(testPool)
        #for i, first in enumerate(scanners):
        for i in checkedPool[:]:
            #for j, second in enumerate(scanners):
            for j in testPool[:]:
                print(f"Checking {i}, {j}")
                if (i == j):
                    continue
                # if (second.correctRotIndex >= 0):
                #     continue
                diff, offset, secRotIndex = compare(scanners[i], scanners[j])
                #print(diff)
                if (diff >= 12):
                    print(f"Same: {i} {j}")
                    scanners[j].offset = offset
                    scanners[j].correctRotIndex = secRotIndex
                    scanners[j].beacons = list(map(lambda x: posAdd(x, offset), scanners[j].allPos[secRotIndex][:]))
                    #scanners[j].realPos = posAdd(scanners[i].realPos, offset)
                    scanners[j].realPos = offset
                    print(scanners[j].realPos)
                    testPool.remove(j)
                    checkedPool.append(j)
            checkedPool.remove(i)
        if (checkSize == len(testPool)):
            print("Nothing found!")
            break

    for i, scanner in enumerate(scanners):
        print(f"{i} - {scanners[i].realPos}")

    beacons = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            beacons.add(beacon)

    # Part 1
    for beacon in beacons:
        print(beacon)
    print(len(beacons))

    # Part 2
    maxDist = 0
    for i in range(len(scanners)):
        for j in range(i, len(scanners)):
            newDist = dist(scanners[i].realPos, scanners[j].realPos)
            if (newDist > maxDist):
                maxDist = newDist
    print(maxDist)

if (__name__ == "__main__"):
    main()
