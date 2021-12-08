def median(values):
    values = sorted(values)
    return values[len(values)//2] if len(values) % 2 else (values[len(values)//2] + values[len(values)//2-1])/2


def calculateFuel(positions, target):
    totalFuel = 0
    for pos in positions:
        dist = abs(pos - target)
        totalFuel += (dist/2)*(dist+1)
    return int(totalFuel)


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Parse fishes into buckets for each internal day of fish.
    positions = [int(n) for n in lines[0].split(',')]

    # Part 1
    mid = int(median(positions))
    totalFuel = 0
    for pos in positions:
        totalFuel += abs(pos - mid)

    print(totalFuel)

    # Part 2
    leastFuel = -1
    for x in range(min(positions), max(positions)):
        totalFuel = calculateFuel(positions, x)
        if (leastFuel == -1):
            leastFuel = totalFuel
        if totalFuel < leastFuel:
            leastFuel = totalFuel
    print(leastFuel)

if (__name__ == "__main__"):
    main()
