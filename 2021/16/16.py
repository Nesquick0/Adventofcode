def readPacket(values):
    version = 0

    i = 0
    while (i < len(values)):
        version = int(values[i:i+3], 2)
        i += 3
        typeId = int(values[i:i+3], 2)
        i += 3
        if (typeId == 4): # literal value
            value = ""
            while (True):
                startBit = values[i]
                value += values[i+1:i+5]
                i += 5
                if (startBit == "0"):
                    break
            value = int(value, 2)
            return (version, i, value)

        else: # Operator
            lengthTypeId = values[i]
            i += 1
            subValues = []
            if (lengthTypeId == "0"):
                numOfBits = int(values[i:i+15], 2)
                i += 15
                limitBits = i + numOfBits
                while (i < limitBits):
                    subVersion, offset, subValue = readPacket(values[i:limitBits])
                    i += offset
                    version += subVersion
                    subValues.append(subValue)
            else:
                numOfPackets = int(values[i:i+11], 2)
                i += 11
                for _ in range(numOfPackets):
                    subVersion, offset, subValue = readPacket(values[i:])
                    i += offset
                    version += subVersion
                    subValues.append(subValue)

            value = 0
            if (typeId == 0):
                value = sum(subValues)
            elif (typeId == 1):
                value = 1
                for subValue in subValues:
                    value *= subValue
            elif (typeId == 2):
                value = min(subValues)
            elif (typeId == 3):
                value = max(subValues)
            elif (typeId == 5):
                value = 1 if (subValues[0] > subValues[1]) else 0
            elif (typeId == 6):
                value = 1 if (subValues[0] < subValues[1]) else 0
            elif (typeId == 7):
                value = 1 if (subValues[0] == subValues[1]) else 0
            return (version, i, value)

    return 0 # Should never happen.


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    hexValues = list(lines[0].strip())
    values = "".join(["{:04b}".format((int(c, 16))) for c in hexValues])

    result = readPacket(values)
    print(f"Part 1: {result[0]}")
    print(f"Part 2: {result[2]}")




if (__name__ == "__main__"):
    main()
