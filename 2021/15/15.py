import sys
import heapq

class World():
    def __init__(self):
        self.points = []
        self.sizeX = 0
        self.sizeY = 0
        self.dist = []
        self.prev = []

    def getNeighbours(self, index):
        x = index % self.sizeX
        y = index // self.sizeY
        neighbours = []
        if x > 0:
            neighbours.append(index-1)
        if x < self.sizeX-1:
            neighbours.append(index+1)
        if y > 0:
            neighbours.append(index-self.sizeX)
        if y < self.sizeY-1:
            neighbours.append(index+self.sizeX)
        return neighbours

    def findDist(self):
        # Dijkstra's algorithm
        q = []
        for _ in range(len(self.points)):
            self.dist.append(sys.maxsize)
            self.prev.append(None)
        self.dist[0] = 0
        heapq.heappush(q, (0, 0))

        while (q):
            _, u = heapq.heappop(q)

            for v in self.getNeighbours(u):
                alt = self.dist[u] + self.points[v]
                if alt < self.dist[v]:
                    self.dist[v] = alt
                    self.prev[v] = u
                    heapq.heappush(q, (alt, v))


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Part 1
    world = World()
    world.sizeX = len(lines[0].strip())
    world.sizeY = len(lines)
    for line in lines:
        line = line.strip()
        for char in line:
            world.points.append(int(char))

    world.findDist()
    print(world.dist[-1])

    # Part 2
    world = World()
    world.sizeX = len(lines[0].strip())*5
    world.sizeY = len(lines)*5
    for line in lines:
        line = line.strip()
        points = []
        for char in line:
            points.append(int(char))
        world.points.extend(points)
        for _ in range(4):
            points = list(map(lambda x: (x % 9)+1, points))
            world.points.extend(points)

    points = world.points[:]
    for _ in range(4):
        points = list(map(lambda x: (x % 9)+1, points))
        world.points.extend(points)

    world.findDist()
    print(world.dist[-1])


if (__name__ == "__main__"):
    main()
