def main():
    # Load list of numbers from input.txt
    with open('input.txt', 'r') as f:
        numbers = [int(line) for line in f]

    # Part 1
    # How many times is number larger than previous number?
    count = 0
    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i - 1]:
            count += 1
    print(count)

    # Part 2
    # Sliding window of size 3
    slidingNumbers = []
    for i in range(len(numbers) - 2):
        slidingNumbers.append(sum(numbers[i:i+3]))

    count = 0
    for i in range(1, len(slidingNumbers)):
        if slidingNumbers[i] > slidingNumbers[i - 1]:
            count += 1
    print(count)


if (__name__ == "__main__"):
    main()
