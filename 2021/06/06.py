def simulate(fishes, days):
    # Simulate day
    for _i in range(days):
        newFishes = fishes[1:] + [0]
        if (fishes[0] > 0):
            newFishes[8] = fishes[0]
            newFishes[6] += fishes[0]
        fishes = newFishes
        #print(f"{_i+1}: {fishes}, {sum(fishes)}")

    print(sum(fishes))

def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Parse fishes into buckets for each internal day of fish.
    numbers = [int(n) for n in lines[0].split(',')]
    fishes = [0] * 9
    for n in numbers:
        fishes[n] += 1
    print(fishes)

    # Part 1
    simulate(fishes[:], 80)

    # Part 2
    simulate(fishes[:], 256)

if (__name__ == "__main__"):
    main()
