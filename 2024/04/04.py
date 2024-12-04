class WordSearch():
    def __init__(self, lines):
        self.lines = lines

    def checkAllDirections(self, i) -> int:
        x = i % self.width
        y = i // self.width
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        word = "XMAS"

        num = 0
        for direction in directions:
            curPos = [x, y]
            found = True
            for char in word:
                i = curPos[0] + curPos[1] * self.width
                if (self.isValidPos(curPos[0], curPos[1]) and self.chars[i] == char):
                    # Continue
                    pass
                else:
                    # Wrong position or wrong char.
                    found = False
                    break
                curPos[0] += direction[0]
                curPos[1] += direction[1]
            if (found):
                #print(x, y)
                num += 1
        return num


    def checkAllDirections2(self, i) -> int:
        x = i % self.width
        y = i // self.width

        # Center has to be "A"
        char = self.chars[i]
        if (char != "A"):
            return 0

        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        allValid = True
        # Try to get all 4 corners.
        corners = []
        for direction in directions:
            newPos = [x + direction[0], y + direction[1]]
            if (self.isValidPos(newPos[0], newPos[1])):
                i = newPos[0] + newPos[1] * self.width
                corners.append(self.chars[i])
        # Must be all 4 corners.
        if (len(corners) != 4):
            allValid = False
        else:
            # M and S must alternate in pairs.
            cornerPairs = [i + j for i,j in zip(corners[::2], corners[1::2])]
            for cornerPair in cornerPairs:
                if (cornerPair == "SM" or cornerPair == "MS"):
                    pass # Valid
                else:
                    allValid = False

        if (allValid):
            return 1
        return 0

    def isValidPos(self, x, y):
        if (x >= 0 and x < self.width and y >= 0 and y < self.height):
            return True
        return False

    def run(self):
        self.chars = []
        self.height = len(self.lines)
        self.width = len(self.lines[0].strip())
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line.strip()):
                self.chars.append(char)

        num = 0
        for i, _ in enumerate(self.chars):
            num += self.checkAllDirections(i)
        print(num)

    def run2(self):
        self.chars = []
        self.height = len(self.lines)
        self.width = len(self.lines[0].strip())
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line.strip()):
                self.chars.append(char)

        num = 0
        for i, _ in enumerate(self.chars):
            num += self.checkAllDirections2(i)
        print(num)

def part1(lines):
    WordSearch(lines).run()

def part2(lines):
    WordSearch(lines).run2()

def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    part1(lines)
    part2(lines)


if (__name__ == '__main__'):
    main()
