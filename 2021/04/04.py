class Board():
    def __init__(self):
        self.values = []
        self.sizeX = 5
        self.sizeY = 5
        self.marked = [0] * self.sizeX * self.sizeY
        self.win = False


    def mark(self, value):
        foundIndex = -1
        for i in range(self.sizeX * self.sizeY):
            if self.values[i] == value:
                self.marked[i] = 1
                foundIndex = i
                break

        # Check whether row or column is marked
        if (foundIndex >= 0):
            x = foundIndex % self.sizeX
            y = foundIndex // self.sizeX

            foundRow = True
            for i in range(self.sizeX):
                if (self.marked[i + y * self.sizeX] == 0):
                    foundRow = False
                    break
            if (foundRow):
                return True
                    
            foundColumn = True
            for i in range(self.sizeY):
                if (self.marked[x + i * self.sizeX] == 0):
                    foundColumn = False
                    break
            if (foundColumn):
                return True

        return False

    def sumNonMarked(self):
        result = 0
        for i in range(self.sizeX * self.sizeY):
            if (self.marked[i] == 0):
                result += self.values[i]
        return result



def part1(boards, numbers):
    for number in numbers:
        for board in boards:
            if board.mark(number):
                return (board.sumNonMarked(), number)

    return (-1, -1)


def part2(boards, numbers):
    nBoards = len(boards)
    countWinners = 0
    for number in numbers:
        for board in boards:
            if board.mark(number):
                if (not board.win):
                    countWinners += 1
                board.win = True
                if (countWinners == nBoards):
                    return (board.sumNonMarked(), number)

    return (-1, -1)



def main():
    # Read the input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Read numbers
    numbers = list(map(int, lines[0].split(',')))\

    # Read boards
    boards = []
    board = Board()
    for line in lines[2:]:
        if (not line.strip()):
            boards.append(board)
            board = Board()
        
        for value in line.strip().split(' '):
            try:
                board.values.append(int(value))
            except ValueError:
                pass

    boards.append(board)

    # Part 1
    result = part1(boards, numbers)
    print(result[0] * result[1])

    # Part 1
    result = part2(boards, numbers)
    print(result[0] * result[1])


if (__name__ == '__main__'):
    main()