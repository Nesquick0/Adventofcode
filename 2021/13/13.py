def draw(spots):
    maxX = max(spots, key=lambda x: x[0])[0]
    maxY = max(spots, key=lambda x: x[1])[1]
    for x in range(maxX+1):
        for y in range(maxY+1):
            if (x, y) in spots:
                print("x", end="")
            else:
                print(" ", end="")
        print()
    print()

def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    spots = []
    folds = []
    for i in range(len(lines)):
        line = lines[i].strip()
        if (not line):
            break

        x, y = line.split(",")
        spots.append((int(x), int(y)))

    for i in range(i+1, len(lines)):
        line = lines[i].strip()
        axis, n = line.split(" ")[-1].split("=")
        folds.append((axis, int(n)))

    #print(spots)
    #print(folds)

    # Part 1
    #draw(spots)
    nSpots = [len(spots)]
    for fold in folds:
        axis, n = fold
        if axis == "x":
            for i in range(len(spots)):
                x, y = spots[i]
                if (x > n):
                    x = n - x + n
                spots[i] = (x, y)
        elif axis == "y":
            for i in range(len(spots)):
                x, y = spots[i]
                if (y > n):
                    y = n - y + n
                spots[i] = (x, y)
        spots = list(set(spots))
        nSpots.append(len(spots))

    print(f"After first fold: {nSpots[1]}")
    draw(list(map(lambda x: (x[1], x[0]), spots)))


if (__name__ == "__main__"):
    main()
