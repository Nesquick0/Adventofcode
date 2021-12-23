def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    algorithm = [[1 if x == "#" else 0 for x in lines[0].strip()]]

    if (lines[0][0] == "."):
        infinityBit = ["0"]
    else:
        infinityBit = ["0", "1"]

    image = {}
    for i in range(2, len(lines)):
        line = lines[i].strip()
        for j in range(len(line)):
            y = i-2
            x = j
            if (line[j] == "#"):
                image[(x, y)] = 1

    print(f"Image original: {len(image)}")
    for i in range(50):
        newImage = {}

        # Calculate min and max positions.
        minX = min(image.keys(), key=lambda x: x[0])[0]
        maxX = max(image.keys(), key=lambda x: x[0])[0]
        minY = min(image.keys(), key=lambda x: x[1])[1]
        maxY = max(image.keys(), key=lambda x: x[1])[1]

        for y in range(minY-2, maxY+3):
            for x in range(minX-2, maxX+3):
                # Get value.
                value = ""
                for diffY in range(-1, 2):
                    for diffX in range(-1, 2):
                        if (x+diffX < minX or x+diffX > maxX or y+diffY < minY or y+diffY > maxY):
                            value += infinityBit[i%len(infinityBit)]
                        else:
                            if (image.get((x+diffX, y+diffY), 0) == 1):
                                value += "1"
                            else:
                                value += "0"
                value = int(value, 2)
                if (algorithm[i%len(algorithm)][value] == 1):
                    newImage[(x, y)] = 1

        image = newImage
        print(f"Image: {len(image)}")
        # for y in range(minY, maxY+1):
        #     for x in range(minX, maxX+1):
        #         print("#" if image.get((x, y), 0) == 1 else ".", end="")
        #     print()

if (__name__ == "__main__"):
    main()
