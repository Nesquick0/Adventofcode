class Solver():
    def __init__(self, lines):
        self.lines = lines


    def parseInput(self):
        i = 0
        # Parse rules
        self.rules = {}
        while (self.lines[i].strip()):
            rule = list(map(int, self.lines[i].strip().split("|")))
            x, y = rule
            if (rule[0] not in self.rules):
                self.rules[x] = []
            self.rules[x].append(y)
            i += 1
        i += 1

        # Parse updates
        self.updates = []
        while (i < len(self.lines)):
            update = list(map(int, self.lines[i].strip().split(",")))
            self.updates.append(update)
            i += 1


    def isCorrect(self, update) -> bool:
        for i, n in enumerate(update):
            # Get rest of list.
            if (i == 0):
                continue
            beforeUpdate = update[:i]
            if (n not in self.rules):
                continue # Number missing, doesn't matter.

            rule = self.rules[n]
            ruleSet = set(rule)
            beforeUpdateSet = set(beforeUpdate)

            intersect = ruleSet.intersection(beforeUpdateSet)
            if (len(intersect) > 0):
                # Something still there which it shouldn't.
                return False

        return True


    def part1(self):
        self.parseInput()

        # Check if valid and count middle.
        counter = 0
        for update in self.updates:
            if (self.isCorrect(update)):
                middle = update[len(update) // 2]
                counter += middle
        print(counter)


    def reorder(self, update):
        # Take slice from 1 to all and if not correct move last one forward until correct.
        currentUpdate = [update[0]]

        for n in update[1:]:
            foundSolution = False
            for i in range(len(currentUpdate), -1, -1):
                newUpdate = currentUpdate[:i] + [n] + currentUpdate[i:]
                if (self.isCorrect(newUpdate)):
                    currentUpdate = newUpdate
                    foundSolution = True
                    break # New number
            if (not foundSolution):
                print(f"Something wrong:\n{update}\n{currentUpdate}\n{n}")

        return currentUpdate


    def part2(self):
        self.parseInput()

        # Check if valid and count middle.
        counter = 0
        for update in self.updates:
            if (self.isCorrect(update)):
                continue # Skip already correct
            update = self.reorder(update)
            middle = update[len(update) // 2]
            counter += middle
        print(counter)


def main():
    with open('input.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    Solver(lines).part1()
    Solver(lines).part2()


if (__name__ == '__main__'):
    main()
