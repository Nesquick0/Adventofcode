import re

class Box():
    def __init__(self, x1, x2, y1, y2, z1, z2) -> None:
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
        self.z1 = min(z1, z2)
        self.z2 = max(z1, z2)


    def insideOther(self, other) -> bool:
        allInside = True
        for point in self.getPoints():
            if (not other.insidePoint(point)):
                allInside = False
                break
        return allInside

    def insidePoint(self, point):
        return self.inside(point[0], point[1], point[2])


    def inside(self, xn, yn, zn) -> bool:
        if (xn >= self.x1 and xn <= self.x2 and yn >= self.y1 and yn <= self.y2 and zn >= self.z1 and zn <= self.z2):
            return True
        return False


    def getPoints(self) -> list:
        points = []
        points.append((self.x1, self.y1, self.z1))
        points.append((self.x1, self.y1, self.z2))
        points.append((self.x1, self.y2, self.z1))
        points.append((self.x1, self.y2, self.z2))
        points.append((self.x2, self.y1, self.z1))
        points.append((self.x2, self.y1, self.z2))
        points.append((self.x2, self.y2, self.z1))
        points.append((self.x2, self.y2, self.z2))
        return points


    def getSize(self) -> int:
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)


    def intersect(self, other) -> bool:
        if (other.x2 > self.x1 and other.x1 < self.x2 and other.y2 > self.y1 and other.y1 < self.y2 and other.z2 > self.z1 and other.z1 < self.z2):
            return True
        return False


def adding(boxes, newBox):
    #print("Adding: ", newBox.x1, newBox.x2, newBox.y1, newBox.y2, newBox.z1, newBox.z2)
    for box in boxes:
        # Check whether newBox is inside box.
        if (newBox.insideOther(box)):
            return

        # Check whether newBox intersect with any previous box.
        if (box.intersect(newBox)):
            if (newBox.x1 < box.x1):
                adding(boxes, Box(newBox.x1, box.x1, newBox.y1, newBox.y2, newBox.z1, newBox.z2))
                adding(boxes, Box(box.x1, newBox.x2, newBox.y1, newBox.y2, newBox.z1, newBox.z2))
                return
            if (newBox.x2 > box.x2):
                adding(boxes, Box(newBox.x1, box.x2, newBox.y1, newBox.y2, newBox.z1, newBox.z2))
                adding(boxes, Box(box.x2, newBox.x2, newBox.y1, newBox.y2, newBox.z1, newBox.z2))
                return
            if (newBox.y1 < box.y1):
                adding(boxes, Box(newBox.x1, newBox.x2, newBox.y1, box.y1, newBox.z1, newBox.z2))
                adding(boxes, Box(newBox.x1, newBox.x2, box.y1, newBox.y2, newBox.z1, newBox.z2))
                return
            if (newBox.y2 > box.y2):
                adding(boxes, Box(newBox.x1, newBox.x2, newBox.y1, box.y2, newBox.z1, newBox.z2))
                adding(boxes, Box(newBox.x1, newBox.x2, box.y2, newBox.y2, newBox.z1, newBox.z2))
                return
            if (newBox.z1 < box.z1):
                adding(boxes, Box(newBox.x1, newBox.x2, newBox.y1, newBox.y2, newBox.z1, box.z1))
                adding(boxes, Box(newBox.x1, newBox.x2, newBox.y1, newBox.y2, box.z1, newBox.z2))
                return
            if (newBox.z2 > box.z2):
                adding(boxes, Box(newBox.x1, newBox.x2, newBox.y1, newBox.y2, newBox.z1, box.z2))
                adding(boxes, Box(newBox.x1, newBox.x2, newBox.y1, newBox.y2, box.z2, newBox.z2))
                return
            print("Something wrong")

    #print("Box added: ", newBox.x1, newBox.x2, newBox.y1, newBox.y2, newBox.z1, newBox.z2, newBox.getSize())
    boxes.append(newBox)


def removing(boxes, newBox, newBoxes):
    for box in boxes:
        # Check whether box is inside newBox.
        if (box.insideOther(newBox)):
            continue

        # Check whether newBox intersect with any previous box.
        if (box.intersect(newBox)):
            if (box.x1 < newBox.x1):
                adding(newBoxes, Box(box.x1, newBox.x1, box.y1, box.y2, box.z1, box.z2))
            if (box.x2 > newBox.x2):
                adding(newBoxes, Box(newBox.x2, box.x2, box.y1, box.y2, box.z1, box.z2))
            if (box.y1 < newBox.y1):
                adding(newBoxes, Box(box.x1, box.x2, box.y1, newBox.y1, box.z1, box.z2))
            if (box.y2 > newBox.y2):
                adding(newBoxes, Box(box.x1, box.x2, newBox.y2, box.y2, box.z1, box.z2))
            if (box.z1 < newBox.z1):
                adding(newBoxes, Box(box.x1, box.x2, box.y1, box.y2, box.z1, newBox.z1))
            if (box.z2 > newBox.z2):
                adding(newBoxes, Box(box.x1, box.x2, box.y1, box.y2, newBox.z2, box.z2))
        else:
            newBoxes.append(box)


def draw(boxes):
    minMax = [50,0,50,0,50,0]
    for box in boxes:
        minMax[0] = min(minMax[0], box.x1)
        minMax[1] = max(minMax[1], box.x2)
        minMax[2] = min(minMax[2], box.y1)
        minMax[3] = max(minMax[3], box.y2)
        minMax[4] = min(minMax[4], box.z1)
        minMax[5] = max(minMax[5], box.z2)

    for y in range(minMax[3], minMax[2] - 1, -1):
        for x in range(minMax[0], minMax[1] + 1):
            isInside = False
            for box in boxes:
                for z in range(minMax[4], minMax[5] + 1):
                    if (box.insidePoint([x, y, z])):
                        isInside = True
                        break

            if (isInside):
                print("#", end="")
            else:
                print(" ", end="")
        print()


def getActive(boxes):
    active = 0
    for box in boxes:
        active += box.getSize()
    print(active)


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Parse line: on x=-20..26,y=-36..17,z=-47..7
    boxes = []
    part1Limits = Box(-51, 51, -51, 51, -51, 51)
    for line in lines:
        m = re.match(r'(on|off) x=(.+),y=(.+),z=(.+)', line)
        op = m.group(1)
        minX, maxX = map(int, m.group(2).split('..'))
        minY, maxY = map(int, m.group(3).split('..'))
        minZ, maxZ = map(int, m.group(4).split('..'))

        # Enable for part 1
        # if (not part1Limits.inside(minX, minY, minZ)):
        #     continue
        # if (not part1Limits.inside(maxX, maxY, maxZ)):
        #     continue

        print(op, minX, maxX, minY, maxY, minZ, maxZ)

        if (op == 'on'):
            # Add box with +1. Think about it like float borders instead of int. So max doesn't include box.
            # So Box 10-14 has 10, 11, 12 and 13.
            adding(boxes, Box(minX, maxX+1, minY, maxY+1, minZ, maxZ+1))
        else:
            newBoxes = []
            removing(boxes, Box(minX, maxX+1, minY, maxY+1, minZ, maxZ+1), newBoxes)
            boxes = newBoxes

        #draw(boxes)
    getActive(boxes)



if (__name__ == "__main__"):
    main()
