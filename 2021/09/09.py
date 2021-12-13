class World():
    def __init__(self, values, maxX, maxY):
        self.values = values
        self.maxX = maxX
        self.maxY = maxY


    def getNeighbours(self, index):
        x = index % self.maxX
        y = index // self.maxX
        neighbours = []
        if x > 0:
            neighbours.append((index-1, self.values[index-1]))
        if x < self.maxX-1:
            neighbours.append((index+1, self.values[index+1]))
        if y > 0:
            neighbours.append((index-self.maxX, self.values[index-self.maxX]))
        if y < self.maxY-1:
            neighbours.append((index+self.maxX, self.values[index+self.maxX]))
        return neighbours


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    allValues = []
    maxX = len(lines[0].strip())
    maxY = len(lines)
    for line in lines:
        values = list(map(int, list(line.strip())))
        allValues.extend(values)

    world = World(allValues, maxX, maxY)

    # Part 1
    lowPoints = []
    lowPointsIndex = []
    for i, value in enumerate(world.values):
        neighbours =  world.getNeighbours(i)
        lowest = True
        for n in neighbours:
            if (value >= n[1]):
                lowest = False
                break

        if (lowest):
            lowPoints.append(value)
            lowPointsIndex.append(i)

    print(lowPoints)
    print(sum(map(lambda x: x+1, lowPoints)))

    # Part 2
    visited = set()
    basins = []
    for lowIndex in lowPointsIndex:
        todo = [lowIndex]
        basin = []

        while (todo):
            newIndex = todo.pop()
            if (newIndex in visited):
                continue
            visited.add(newIndex)
            basin.append(newIndex)

            neighbours = world.getNeighbours(newIndex)
            for n in neighbours:
                if (n[1] < 9):
                    todo.append(n[0])

        basins.append(basin)

    basins = sorted(basins, key=len, reverse=True)
    for basin in basins[:3]:
        print(basin)
    print(len(basins[0]) * len(basins[1]) * len(basins[2]))



if (__name__ == "__main__"):
    main()
