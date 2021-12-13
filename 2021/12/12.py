class World():
    def __init__(self):
        self.caves = {}



def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    world = World()
    for line in lines:
        a, b = line.strip().split("-")
        if (a not in world.caves):
            world.caves[a] = []
        if (b not in world.caves):
            world.caves[b] = []
        world.caves[a].append(b)
        world.caves[b].append(a)

    # Part 1
    queue = [("start", ["start"])]
    paths = []
    while (queue):
        cave, state = queue.pop(0)
        for neighbour in world.caves[cave]:
            if (neighbour == "end"):
                paths.append(state + [neighbour])
            else:
                if (neighbour == "start"):
                    continue
                if (neighbour.islower() and neighbour in state):
                    continue
                queue.append((neighbour, state + [neighbour]))

    # for path in paths:
    #     print(path)
    print(len(paths))

    # Part 2
    queue = [("start", ["start"], None)]
    paths = []
    while (queue):
        cave, state, specialCaveO = queue.pop(0)
        for neighbour in world.caves[cave]:
            specialCave = specialCaveO
            if (neighbour == "end"):
                paths.append((state + [neighbour], specialCave))
            else:
                if (neighbour == "start"):
                    continue
                if (neighbour.islower() and neighbour in state):
                    if (not specialCave):
                        specialCave = neighbour
                    else:
                        continue
                queue.append((neighbour, state + [neighbour], specialCave))

    # for path in paths:
    #     print(path)
    print(len(paths))


if (__name__ == "__main__"):
    main()
