def score(char):
    if (char == ")"):
        return 3
    elif (char == "]"):
        return 57
    elif (char == "}"):
        return 1197
    elif (char == ">"):
        return 25137
    else:
        return 0

def scoreAutocomplete(char):
    if (char == "("):
        return 1
    elif (char == "["):
        return 2
    elif (char == "{"):
        return 3
    elif (char == "<"):
        return 4
    else:
        return 0

def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    totalScore = 0
    allAutocomplete = []
    for line in lines:
        line = line.strip()
        chunks = []
        isValid = True
        for char in line:
            if (char in ["(", "[", "<", "{"]):
                chunks.append(char)
            else:
                if (len(chunks) == 0):
                    isValid = False
                    break
                elif (chunks[-1] == "(" and char == ")"):
                    chunks.pop()
                elif (chunks[-1] == "[" and char == "]"):
                    chunks.pop()
                elif (chunks[-1] == "<" and char == ">"):
                    chunks.pop()
                elif (chunks[-1] == "{" and char == "}"):
                    chunks.pop()
                else:
                    totalScore += score(char)
                    isValid = False
                    break

        # Incomplete
        autocompleteScore = 0
        if (isValid):
            #print(line, "".join(chunks))
            for char in reversed(chunks):
                autocompleteScore *= 5
                autocompleteScore += scoreAutocomplete(char)
            #print(autocompleteScore)
            allAutocomplete.append(autocompleteScore)

    # Part 1
    print(totalScore)

    # Part 2
    print(sorted(allAutocomplete)[len(allAutocomplete)//2])

if (__name__ == "__main__"):
    main()
