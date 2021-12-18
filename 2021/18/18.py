import math

class Item():
    def __init__(self, left, right, parent):
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return f"[{self.left},{self.right}]"
        #return "[{},{} {}]".format(self.left, self.right, "." if self.parent else "")


    def createCopy(self):
        newItem = Item(None, None, None)

        if (isinstance(self.left, int)):
            newItem.left = self.left
        else:
            newItem.left = self.left.createCopy()
            newItem.left.parent = newItem

        if (isinstance(self.right, int)):
            newItem.right = self.right
        else:
            newItem.right = self.right.createCopy()
            newItem.right.parent = newItem

        return newItem


    def tryExplode(self, depth):
        if (not isinstance(self.left, int)):
            if (self.left.tryExplode(depth+1)):
                return True

        if (not isinstance(self.right, int)):
            if (self.right.tryExplode(depth+1)):
                return True

        if (depth >= 5):
            #print(f"Explode {self}")
            self.explode(True)
            self.explode(False)
            if (self.parent.left == self):
                self.parent.left = 0
            elif (self.parent.right == self):
                self.parent.right = 0
            else:
                print("Problem!")
            return True

        return False


    def explode(self, goLeft):
        value = self.left if goLeft else self.right
        # Go up in hierarchy and find left way.
        current = self
        while True:
            if (not current.parent):
                return # Nothing on left.
            if ((current.parent.right if goLeft else current.parent.left) == current):
                current = current.parent # Found left item.
                break
            current = current.parent

        # If left is value just update and finish.
        if (isinstance((current.left if goLeft else current.right), int)):
            if (goLeft):
                current.left += value
            else:
                current.right += value
            return
        # Else if start from left item and go down right
        current = current.left if goLeft else current.right
        while True:
            if (isinstance((current.right if goLeft else current.left), int)):
                if (goLeft):
                    current.right += value
                else:
                    current.left += value
                return
            current = current.right if goLeft else current.left



    def trySplit(self):
        if (not isinstance(self.left, int)):
            if (self.left.trySplit()):
                return True
        else:
            if (self.left >= 10):
                #print(f"Split {self}")
                self.left = Item(math.floor(self.left / 2), math.ceil(self.left / 2), self)
                return True # Split found

        if (not isinstance(self.right, int)):
            if (self.right.trySplit()):
                return True
        else:
            if (self.right >= 10):
                #print(f"Split {self}")
                self.right = Item(math.floor(self.right / 2), math.ceil(self.right / 2), self)
                return True # Split found

        return False

    def magnitude(self):
        value = 0
        if (isinstance(self.left, int)):
            value += self.left * 3
        else:
            value += self.left.magnitude() * 3

        if (isinstance(self.right, int)):
            value += self.right * 2
        else:
            value += self.right.magnitude() * 2
        return value


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Part 1
    mainNumber = Item(None, None, None)
    roots = []
    for line in lines:
        line = line.strip()
        items = []
        root = None
        for c in line:
            if (c == "["):
                items.append(Item(None, None, items[-1] if items else None))
            elif (c == "]"):
                root = items.pop()
                if (items):
                    if (items[-1].left is None):
                        items[-1].left = root
                    else:
                        items[-1].right = root
            elif (c == ","):
                pass
            else:
                if (items[-1].left is None):
                    items[-1].left = int(c)
                else:
                    items[-1].right = int(c)

        roots.append(root.createCopy())

        #print(f" + {root}")
        if (len(lines) > 1):
            # Do addition.
            if (mainNumber.left is None):
                mainNumber.left = root
                mainNumber.left.parent = mainNumber
                continue
            else:
                if (mainNumber.right is not None):
                    mainNumber = Item(mainNumber, None, None)
                    mainNumber.left.parent = mainNumber
                mainNumber.right = root
                mainNumber.right.parent = mainNumber
        else:
            mainNumber = root

        while True:
            # Try explode.
            if (mainNumber.tryExplode(1)):
                continue
            # Try split.
            if (mainNumber.trySplit()):
                continue
            break

    print(mainNumber)
    print(mainNumber.magnitude())

    # Part 2
    # Check all pairs of roots against each other.
    maxMagnitude = 0
    for i in range(len(roots)):
        for j in range(len(roots)):
            if (i == j):
                continue

            mainNumber = Item(roots[i].createCopy(), roots[j].createCopy(), None)
            mainNumber.left.parent = mainNumber
            mainNumber.right.parent = mainNumber

            while True:
                # Try explode.
                if (mainNumber.tryExplode(1)):
                    continue
                # Try split.
                if (mainNumber.trySplit()):
                    continue
                break

            if (mainNumber.magnitude() > maxMagnitude):
                maxMagnitude = mainNumber.magnitude()
    print(maxMagnitude)


if (__name__ == "__main__"):
    main()
