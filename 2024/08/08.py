class Solver():
    def __init__(self, lines):
        self.lines = lines

    def posToIndex(self, x, y):
        return x + y * self.width

    def indexToPos(self, i):
        x = i % self.width
        y = i // self.width
        return (x, y)

    def posValid(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def parseInput(self):
        self.height = len(self.lines)
        self.width = len(self.lines[0].strip())
        self.nodes = {}
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line.strip()):
                if (char == "."):
                    pass
                else:
                    if (char not in self.nodes):
                        self.nodes[char] = []
                    self.nodes[char].append(self.posToIndex(x, y))

    def part1(self):
        self.parseInput()

        antinodes = set()
        for _, nodes in self.nodes.items():
            for i in nodes:
                for j in nodes:
                    # Skip same.
                    if (i == j):
                        continue
                    ix, iy = self.indexToPos(i)
                    jx, jy = self.indexToPos(j)
                    newX = (jx - ix) + jx
                    newY = (jy - iy) + jy

                    if (self.posValid(newX, newY)):
                        antinodes.add(self.posToIndex(newX, newY))

        print(len(antinodes))

    def part2(self):
        self.parseInput()

        antinodes = set()
        for _, nodes in self.nodes.items():
            # Skip only one of type.
            if (len(nodes) == 1):
                continue
            for i in nodes:
                for j in nodes:
                    # Skip same.
                    if (i == j):
                        continue
                    ix, iy = self.indexToPos(i)
                    jx, jy = self.indexToPos(j)
                    newPos = (ix, iy)
                    diff = (jx - ix, jy - iy)

                    newPos = (newPos[0] + diff[0], newPos[1] + diff[1])
                    while (self.posValid(newPos[0], newPos[1])):
                        antinodes.add(self.posToIndex(newPos[0], newPos[1]))
                        #print(newPos)
                        newPos = (newPos[0] + diff[0], newPos[1] + diff[1])

        print(len(antinodes))
        # for i in antinodes:
        #     print(self.indexToPos(i))

        # for y in range(self.height):
        #     for x in range(self.width):
        #         if (self.posToIndex(x, y) in antinodes):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print("")


def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    Solver(lines).part1()
    Solver(lines).part2()


if (__name__ == '__main__'):
    main()
