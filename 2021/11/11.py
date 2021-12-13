class World():
    def __init__(self):
        self.grid = []
        self.sizeX = 0
        self.sizeY = 0

    def isValidPos(self, x, y):
        return x >= 0 and x < self.sizeX and y >= 0 and y < self.sizeY

    def neighbourIndeces(self, i):
        x = i % self.sizeX
        y = i // self.sizeX
        neighbours = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx == 0 and dy == 0):
                    continue
                if (self.isValidPos(x + dx, y + dy)):
                    neighbours.append((x + dx) + (y + dy) * self.sizeX)
        return neighbours

    def draw(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                print(self.grid[x + y * self.sizeX], end="")
            print("")

    def simulate(self):
        flashes = 0

        flashed = [0] * len(self.grid)
        self.grid = list(map(lambda x: x+1, self.grid))
        anyChange = True
        while (anyChange):
            anyChange = False
            for i in range(len(self.grid)):
                # For any cell which should flash but haven't already.
                if (self.grid[i] > 9 and flashed[i] == 0):
                    flashed[i] = 1
                    flashes += 1
                    self.grid[i] = 0
                    anyChange = True

                    neighbours = self.neighbourIndeces(i)
                    # For any neighbour that haven't flashed increase by 1.
                    for neighbour in neighbours:
                        if (flashed[neighbour] == 0):
                            self.grid[neighbour] += 1

        return flashes

def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Create world
    world = World()
    world.sizeY = len(lines)
    for line in lines:
        line = line.strip()
        world.sizeX = len(line)
        for char in line:
            world.grid.append(int(char))
    world2 = World()
    world2.grid = world.grid.copy()
    world2.sizeX = world.sizeX
    world2.sizeY = world.sizeY

    # Part 1
    flashes = 0
    for _step in range(100):
        flashes += world.simulate()
    print(flashes)

    # Part 2
    steps = 0
    while True:
        steps += 1
        flashes = world2.simulate()
        if (flashes == world2.sizeX * world2.sizeY):
            break

    print(steps)



if (__name__ == "__main__"):
    main()
