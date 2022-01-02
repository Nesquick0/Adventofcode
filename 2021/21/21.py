def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Part 1
    players = []
    scores = []
    for line in lines:
        players.append(int(line.strip().split(" ")[-1]) - 1)
        scores.append(0)

    dice = 0
    halfTurn = 0
    plIndex = 0
    while (max(scores) < 1000):
        for _ in range(3):
            players[plIndex] += dice + 1
            dice = (dice + 1) % 100
        players[plIndex] = players[plIndex] % 10
        scores[plIndex] += players[plIndex] + 1
        halfTurn += 1
        plIndex = (plIndex + 1) % len(players)
    
    result = min(scores) * halfTurn * 3
    print(f"Result: {result} Half turn: {halfTurn}, Lost: {min(scores)}")

    # Part 2

if (__name__ == "__main__"):
    main()
