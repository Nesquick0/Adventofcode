class Solver():
    def __init__(self, lines):
        self.lines = lines

    def posToIndex(self, x, y):
        return x + y * self.width

    def indexToPos(self, i):
        x = i % self.width
        y = i // self.width
        return (x, y)

    def rotateDir(self, oldDir):
        if (oldDir == (1, 0)): # Right - Down
            return (0, 1)
        if (oldDir == (0, 1)): # Down - Left
            return (-1, 0)
        if (oldDir == (-1, 0)): # Left - Up
            return (0, -1)
        if (oldDir == (0, -1)): # Up - Right
            return (1, 0)
        raise RuntimeError("Bad direction")

    def parseInput(self):
        self.world = []
        self.height = len(self.lines)
        self.width = len(self.lines[0].strip())
        self.guardStart = None
        self.guardDir = (0, -1)
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line.strip()):
                if (char == "."):
                    self.world.append(0)
                elif (char == "#"):
                    self.world.append(1)
                elif (char == "^"):
                    self.guardStart = (x, y)
                    self.world.append(0)

    def part1(self):
        self.parseInput()

        # Simulate movement.
        visited = {}
        guardPos = self.guardStart
        guardDir = self.guardDir
        while True:
            visited[guardPos] = 1
            # Check for object in front.
            newX = guardPos[0] + guardDir[0]
            newY = guardPos[1] + guardDir[1]
            newI = self.posToIndex(newX, newY)
            # New pos out of bounds. Exit.
            if (newX < 0 or newX >= self.width or newY < 0 or newY >= self.height):
                break
            # Wall in front.
            if (self.world[newI] != 0):
                guardDir = self.rotateDir(guardDir)
                continue

            # Move forward.
            guardPos = (newX, newY)

        print(len(visited))

    def checkForLoop(self):
        # Run simulation.
        # Save visited places with direction.
        visited = {}
        guardPos = self.guardStart
        guardDir = self.guardDir
        while True:
            if guardPos not in visited:
                visited[guardPos] = guardDir
            else:
                # Position already visited. If it is same direction then looping.
                if (visited[guardPos] == guardDir):
                    return True
            # Check for object in front.
            newX = guardPos[0] + guardDir[0]
            newY = guardPos[1] + guardDir[1]
            newI = self.posToIndex(newX, newY)
            # New pos out of bounds. Exit.
            if (newX < 0 or newX >= self.width or newY < 0 or newY >= self.height):
                break
            # Wall in front.
            if (self.world[newI] != 0):
                guardDir = self.rotateDir(guardDir)
                continue

            # Move forward.
            guardPos = (newX, newY)
        return False


    def part2(self):
        self.parseInput()

        count = 0
        guardStartIndex = self.posToIndex(self.guardStart[0], self.guardStart[1])
        for i, num in enumerate(self.world):
            # Skip already walls. And Guard start.
            if (num == 1):
                continue
            if (i == guardStartIndex):
                continue

            # Modify world and revert after that.
            self.world[i] = 1
            result = self.checkForLoop()
            self.world[i] = 0
            if (result):
                print(self.indexToPos(i))
                count += 1

        print(count)



def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    Solver(lines).part1()
    Solver(lines).part2()


if (__name__ == '__main__'):
    main()
