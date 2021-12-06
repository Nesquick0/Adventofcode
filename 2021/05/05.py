class Vent():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.points = []
        self.generatePoints()

    def isHV(self):
        if (self.x1 == self.x2):
            return True
        elif (self.y1 == self.y2):
            return True
        return False


    def generatePoints(self):
        # Generate points between x1, y1 and x2, y2.
        x = self.x1
        y = self.y1
        step = (0, 0)
        if (abs(self.x2 - self.x1) >= abs(self.y2 - self.y1)):
            # X is main axis.
            xStep = 1 if (self.x2 > self.x1) else -1
            if (self.isHV()):
                step = (xStep, 0)
            else:
                step = (xStep, (self.y2 - self.y1) / abs(self.x2 - self.x1))
        else:
            # Y is main axis.
            yStep = 1 if (self.y2 > self.y1) else -1
            if (self.isHV()):
                step = (0, yStep)
            else:
                step = ((self.x2 - self.x1) / abs(self.y2 - self.y1), yStep)

        while (x != self.x2 or y != self.y2):
            self.points.append((x, y))
            x += int(round(step[0],0))
            y += int(round(step[1],0))
        self.points.append((x, y))


    def isInside(self, x, y):
        if (self.isHV()):
            return False

        if ((x, y) in self.points):
            return True
        return False




def draw(vents, onlyHV):
    points = {}
    maxX = 0
    maxY = 0

    for vent in vents:
        if (onlyHV and not vent.isHV()):
            continue
        for point in vent.points:
            x, y = point
            maxX = max(maxX, x)
            maxY = max(maxY, y)
            if (point not in points):
                points[point] = 1
            else:
                points[point] += 1

    for y in range(maxY + 1):
        for x in range(maxX + 1):
            if (x, y) in points:
                print(points[(x, y)], end='')
            else:
                print('.', end='')
        print()


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    # Part 1
    vents = []
    for line in lines:
        line = line.strip()
        start, end = line.split(" -> ")
        x1, y1 = start.split(",")
        x2, y2 = end.split(",")
        vent = Vent(int(x1), int(y1), int(x2), int(y2))
        vents.append(vent)
    #draw(vents, True)

    # Count points
    points = {}
    for vent in vents:
        if (not vent.isHV()):
            continue
        for point in vent.points:
            if (point not in points):
                points[point] = 1
            else:
                points[point] += 1
    count = 0
    for point in points:
        if (points[point] > 1):
            count += 1
    print(count)

    # Part 2
    #draw(vents, False)
    points = {}
    for vent in vents:
        for point in vent.points:
            if (point not in points):
                points[point] = 1
            else:
                points[point] += 1
    count = 0
    for point in points:
        if (points[point] > 1):
            count += 1
    print(count)

if (__name__ == "__main__"):
    main()
