import functools
import itertools

@functools.cache
def count_wins(position_1, position_2, score_1, score_2):
    wins_1 = 0
    wins_2 = 0
    for roll_1, roll_2, roll_3 in itertools.product((1, 2, 3), repeat=3):
        new_position_1 = (position_1 - 1 + roll_1 + roll_2 + roll_3) % 10 + 1
        new_score_1 = score_1 + new_position_1
        if new_score_1 >= 21:
            wins_1 += 1
        else:
            new_wins_2, new_wins_1 = count_wins(position_2, new_position_1, score_2, new_score_1)
            wins_1 += new_wins_1
            wins_2 += new_wins_2
    return wins_1, wins_2

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

    # Part 2 - from https://github.com/Farbfetzen/Advent_of_Code/blob/main/python/2021/day21.py
    players = []
    for line in lines:
        players.append(int(line.strip().split(" ")[-1]) - 1)
    scores = count_wins(players[0]+1, players[1]+1, 0, 0)
    print(f"Part2: {max(scores)}")

if (__name__ == "__main__"):
    main()
