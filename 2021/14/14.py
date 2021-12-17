def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    start = list(lines[0].strip())

    rules = {}
    for i in range(2, len(lines)):
        line = lines[i].strip()
        a, b = line.split(" -> ")
        rules[tuple(a)] = b

    # Part 1
    polymer = start.copy()
    for _ in range(10):
        i = 1
        while (i < len(polymer)):
            if (tuple(polymer[i-1:i+1]) in rules):
                polymer.insert(i, rules[tuple(polymer[i-1:i+1])])
                i += 1
            i += 1

        print(len(polymer))

    counts = {}
    for c in polymer:
        if (c in counts):
            counts[c] += 1
        else:
            counts[c] = 1
    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    #print(counts)
    print(f"Result part 1: {counts[0][1] - counts[-1][1]}")

    # Part 2
    polymerPairs = {}
    for rule in rules:
        polymerPairs[rule] = 0

    for i in range(len(start)-1):
        pair = (start[i], start[i+1])
        polymerPairs[pair] += 1

    #print(polymerPairs)
    for _ in range(40):
        newPolymerPairs = {}
        for rule in rules:
            newPolymerPairs[rule] = 0

        for pair in polymerPairs:
            c = rules[pair]
            newPair1, newPair2 = (pair[0], c), (c, pair[1])
            newPolymerPairs[newPair1] += polymerPairs[pair]
            newPolymerPairs[newPair2] += polymerPairs[pair]

        polymerPairs = newPolymerPairs
        #print(sum(polymerPairs.values()))

    counts = {}
    for pair, count in polymerPairs.items():
        if (pair[0] not in counts):
            counts[pair[0]] = 0
        if (pair[1] not in counts):
            counts[pair[1]] = 0
        counts[pair[0]] += count
        #counts[pair[1]] += count
    counts[start[-1]] += 1 # This char will be always at the end.
    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print(f"Result part 2: {counts[0][1] - counts[-1][1]}")


if (__name__ == "__main__"):
    main()
