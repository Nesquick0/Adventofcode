import sys
import heapq

def getChar(value):
    if (value == 0):
        return " "
    return chr(value+64)

def draw(state):
    print("."*(len(state[0])+2))
    print(".", end="")
    for i in range(len(state[0])):
        print(getChar(state[0][i]), end="")
    print(".")

    if (len(state[1]) == 8):
        for y in range(2):
            print("..." if y == 0 else "  .", end="")
            for i in range(4):
                print(f"{getChar(state[1][i*2+y])}.", end="")
            print(".." if y == 0 else "", end="")
            print("")
    else:
        for y in range(4):
            print("..." if y == 0 else "  .", end="")
            for i in range(4):
                print(f"{getChar(state[1][i*4+y])}.", end="")
            print(".." if y == 0 else "", end="")
            print("")

    print("  " + "."*(len(state[0])-2))
    print(state[2])


def getEnergy(animal):
    return 10**(animal-1)


def createStateFromTopPlaces(hall, room, energy, queue, visited):
    for i in range(4):
        if (room[i*2] != 0):
            value = room[i*2]
            startIndex = i*2+2
            for j in range(startIndex-1, -1, -1):
                if (hall[j] != 0):
                    break
                if (j >= 2 and j <= 8 and j%2 == 0):
                    continue
                newState = (hall[:j] + (value,) + hall[j+1:], room[:i*2] + (0,) + room[i*2+1:], energy + getEnergy(value)*(startIndex-j+1))
                addToQueue(newState, queue, visited)
            for j in range(startIndex+1, len(hall)):
                if (hall[j] != 0):
                    break
                if (j >= 2 and j <= 8 and j%2 == 0):
                    continue
                newState = (hall[:j] + (value,) + hall[j+1:], room[:i*2] + (0,) + room[i*2+1:], energy + getEnergy(value)*(j-startIndex+1))
                addToQueue(newState, queue, visited)


def createStateFromTopPlaces2(hall, room, energy, queue, visited):
    for i in range(4):
        if (room[i*4] != 0):
            value = room[i*4]
            startIndex = i*2+2
            for j in range(startIndex-1, -1, -1):
                if (hall[j] != 0):
                    break
                if (j >= 2 and j <= 8 and j%2 == 0):
                    continue
                newState = (hall[:j] + (value,) + hall[j+1:], room[:i*4] + (0,) + room[i*4+1:], energy + getEnergy(value)*(startIndex-j+1))
                addToQueue2(newState, queue, visited)
            for j in range(startIndex+1, len(hall)):
                if (hall[j] != 0):
                    break
                if (j >= 2 and j <= 8 and j%2 == 0):
                    continue
                newState = (hall[:j] + (value,) + hall[j+1:], room[:i*4] + (0,) + room[i*4+1:], energy + getEnergy(value)*(j-startIndex+1))
                addToQueue2(newState, queue, visited)


def isFinalRoom(room):
    return (room == (1,1,2,2,3,3,4,4))

def isFinalRoom2(room):
    return (room == (1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4))


def addToQueue(state, queue, visited):
    hashedState = state[:2]
    if (hashedState not in visited or visited[hashedState] > state[2] or isFinalRoom(state[1])):
        heapq.heappush(queue, (state[2], state))
        visited[hashedState] = state[2]

def addToQueue2(state, queue, visited):
    hashedState = state[:2]
    if (hashedState not in visited or visited[hashedState] > state[2] or isFinalRoom2(state[1])):
        heapq.heappush(queue, (state[2], state))
        visited[hashedState] = state[2]


def main():
    # Read input.txt
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Part 1
    initState = [ [0]*lines[1].count(".") , [0]*8]
    items1 = [x for x in lines[2].strip().split("#") if x]
    items2 = [x for x in lines[3].strip().split("#") if x]
    items = list(zip(items1, items2))
    for i, item in enumerate(items):
        initState[1][i*2] = item[0]
        initState[1][i*2+1] = item[1]
    for i in range(len(initState[1])):
        if (initState[1][i] == "A"):
            initState[1][i] = 1
        elif (initState[1][i] == "B"):
            initState[1][i] = 2
        elif (initState[1][i] == "C"):
            initState[1][i] = 3
        elif (initState[1][i] == "D"):
            initState[1][i] = 4
    initState = (tuple(initState[0]), tuple(initState[1]), 0)
    draw(initState)

    visited = {}
    queue = []
    heapq.heappush(queue, (initState[2], initState))
    minEnergy = sys.maxsize

    while (queue):
        state = heapq.heappop(queue)
        hall, room, energy = state[1]
        if (isFinalRoom(room)):
            minEnergy = min(minEnergy, energy)
            continue

        # From bottom place in room to any free space in hall. Go to top place and simulate as from top.
        for i in range(4):
            # Top place is occupied.
            if (room[i*2] != 0):
                continue
            if (room[i*2+1] != 0):
                value = room[i*2+1]
                newRoom = room[:i*2] + (value, 0) + room[i*2+2:]
                newEnergy = energy + getEnergy(value)
                createStateFromTopPlaces(hall, newRoom, newEnergy, queue, visited)

        # From top place in room to any free space in hall.
        createStateFromTopPlaces(hall, room, energy, queue, visited)

        # From hall go to correct room.
        for i in range(len(hall)):
            if (hall[i] == 0):
                continue
            value = hall[i]
            correctRoom = (value-1)
            if (room[correctRoom*2] == 0):
                # Check whether way in hall is clear.
                wayClear = True
                direction = 1 if (i < value*2) else -1
                for j in range(i+direction, value*2+direction, direction):
                    if (hall[j] != 0):
                        wayClear = False
                        break
                if (wayClear):
                    # Move to top place in room. If empty space in bottom room move there.
                    newHall = hall[:i] + (0,) + hall[i+1:]

                    if (room[correctRoom*2+1] == 0):
                        newRoom = room[:correctRoom*2+1] + (value,) + room[correctRoom*2+2:]
                        newEnergy = energy + getEnergy(value)*(abs(i-value*2)+2)
                    else:
                        newRoom = room[:correctRoom*2] + (value,) + room[correctRoom*2+1:]
                        newEnergy = energy + getEnergy(value)*(abs(i-value*2)+1)

                    newState = (newHall, newRoom, newEnergy)
                    addToQueue(newState, queue, visited)

    print(f"Part 1: {minEnergy}\n")


    # Part 2
    t = initState[1]
    initState = (initState[0], (t[0], 4, 4, t[1], t[2], 3, 2, t[3], t[4], 2, 1, t[5], t[6], 1, 3, t[7]), 0)
    draw(initState)

    visited = {}
    queue = []
    heapq.heappush(queue, (initState[2], initState))
    minEnergy = sys.maxsize

    test = -1
    while (queue):
        state = heapq.heappop(queue)
        hall, room, energy = state[1]
        if (isFinalRoom2(room)):
            minEnergy = min(minEnergy, energy)
            print(f"Done! {energy}")
            #draw(state[1])
            continue

        # From not-top places in room to any free space in hall. Go to top place and simulate as from top.
        for i in range(4):
            if (room[i*4] != 0):
                continue
            # Check each row of room (not top one).
            for j in range(1, 4):
                # Check place is occupied. Don't need to check below.
                if (room[i*4+j] != 0):
                    value = room[i*4+j]

                    newRoom = list(room)
                    newRoom[i*4] = value
                    newRoom[i*4+j] = 0
                    newRoom = tuple(newRoom)

                    newEnergy = energy + getEnergy(value)*j
                    createStateFromTopPlaces2(hall, newRoom, newEnergy, queue, visited)
                    break

        # From top place in room to any free space in hall.
        createStateFromTopPlaces2(hall, room, energy, queue, visited)

        # From hall go to correct room.
        for i in range(len(hall)):
            if (hall[i] == 0):
                continue
            value = hall[i]
            correctRoom = (value-1)
            if (room[correctRoom*4] == 0):
                # Check whether way in hall is clear.
                wayClear = True
                direction = 1 if (i < value*2) else -1
                for j in range(i+direction, value*2+direction, direction):
                    if (hall[j] != 0):
                        wayClear = False
                        break
                if (wayClear):
                    # Move to top place in room. Check how deep it can go.
                    newHall = hall[:i] + (0,) + hall[i+1:]

                    deep = 0
                    badValue = False
                    for j in range(1, 4):
                        if (room[correctRoom*4+j] == 0):
                            deep = j
                        else:
                            if (room[correctRoom*4+j] != value):
                                badValue = True
                            break
                    if (badValue):
                        continue

                    newEnergy = energy + getEnergy(value)*(abs(i-value*2)+1+deep)
                    newRoom = room[:correctRoom*4+deep] + (value,) + room[correctRoom*4+1+deep:]

                    newState = (newHall, newRoom, newEnergy)
                    addToQueue2(newState, queue, visited)

    print(f"Part 2: {minEnergy}\n")


if (__name__ == "__main__"):
    main()



        # if (test == -1):
        #     test = 0
        # elif (hall == (0,0,0,2,0,0,0,0,0,0,0) and test == 0 and energy == 40):
        #     draw(state[1])
        #     test = 1
        # elif (hall == (0,0,0,2,0,3,0,0,0,0,0) and test == 1 and energy == 240):
        #     draw(state[1])
        #     test = 2
        # elif (hall == (0,0,0,2,0,0,0,0,0,0,0) and test == 2 and energy == 440):
        #     draw(state[1])
        #     test = 3
        # elif (hall == (0,0,0,2,0,4,0,0,0,0,0) and test == 3 and energy == 3440):
        #     draw(state[1])
        #     test = 4
        # elif (hall == (0,0,0,0,0,4,0,0,0,0,0) and test == 4 and energy == 3470):
        #     draw(state[1])
        #     test = 5
        # elif (hall == (0,0,0,2,0,4,0,0,0,0,0) and test == 5 and energy == 3490):
        #     draw(state[1])
        #     test = 6
        # elif (hall == (0,0,0,0,0,4,0,0,0,0,0) and test == 6 and energy == 3510):
        #     draw(state[1])
        #     test = 7
        # elif (hall == (0,0,0,0,0,4,0,4,0,0,0) and test == 7 and energy == 5510):
        #     draw(state[1])
        #     test = 8
        # elif (hall == (0,0,0,0,0,4,0,4,0,1,0) and test == 8 and energy == 5513):
        #     draw(state[1])
        #     test = 9
        # elif (hall == (0,0,0,0,0,4,0,0,0,1,0) and test == 9 and energy == 8513):
        #     draw(state[1])
        #     test = 10
        # elif (hall == (0,0,0,0,0,0,0,0,0,1,0) and test == 10 and energy == 12513):
        #     draw(state[1])
        #     test = 11
        # elif (hall == (0,0,0,0,0,0,0,0,0,0,0) and test == 11 and energy == 12521):
        #     draw(state[1])
        #     test = 12
        # else:
        #     continue



        # if (test == -1):
        #     test = 0
        # elif (hall == (0,0,0,0,0,0,0,0,0,0,4) and test == 0 and energy == 3000):
        #     draw(state[1])
        #     test = 1
        # elif (hall == (1,0,0,0,0,0,0,0,0,0,4) and test == 1 and energy == 3010):
        #     draw(state[1])
        #     test = 2
        # elif (hall == (1,0,0,0,0,0,0,0,0,2,4) and test == 2 and energy == 3050):
        #     draw(state[1])
        #     test = 3
        # elif (hall == (1,0,0,0,0,0,0,2,0,2,4) and test == 3 and energy == 3080):
        #     draw(state[1])
        #     test = 4
        # elif (hall == (1,1,0,0,0,0,0,2,0,2,4) and test == 4 and energy == 3088):
        #     draw(state[1])
        #     test = 5
        # elif (hall == (1,1,0,0,0,3,0,2,0,2,4) and test == 5 and energy == 3288):
        #     draw(state[1])
        #     test = 6
        # elif (hall == (1,1,0,0,0,0,0,2,0,2,4) and test == 6 and energy == 3688):
        #     draw(state[1])
        #     test = 7
        # elif (hall == (1,1,0,0,0,3,0,2,0,2,4) and test == 7 and energy == 3988):
        #     draw(state[1])
        #     test = 8
        # elif (hall == (1,1,0,0,0,0,0,2,0,2,4) and test == 8 and energy == 4288):
        #     draw(state[1])
        #     test = 9
        # elif (hall == (1,1,0,0,0,2,0,2,0,2,4) and test == 9 and energy == 4328):
        #     #draw(state[1])
        #     test = 10
        # elif (hall == (1,1,0,0,0,2,0,2,0,2,4) and test == 10 and energy == 4328):
        #     draw(state[1])
        #     test = 11
        # elif (hall == (1,1,0,4,0,2,0,2,0,2,4) and test == 11 and energy == 9328):
        #     draw(state[1])
        #     test = 12
        # elif (hall == (1,1,0,4,0,0,0,2,0,2,4) and test == 12 and energy == 9378):
        #     draw(state[1])
        #     test = 13
        # elif (hall == (1,1,0,4,0,0,0,0,0,2,4) and test == 13 and energy == 9438):
        #     draw(state[1])
        #     test = 14
        # elif (hall == (1,1,0,4,0,0,0,0,0,0,4) and test == 14 and energy == 9508):
        #     draw(state[1])
        #     test = 15
        # elif (hall == (1,1,0,4,0,0,0,3,0,0,4) and test == 15 and energy == 9908):
        #     draw(state[1])
        #     test = 16
        # elif (hall == (1,1,0,4,0,0,0,0,0,0,4) and test == 16 and energy == 10108):
        #     draw(state[1])
        #     test = 17
        # elif (hall == (1,1,0,4,0,0,0,0,0,1,4) and test == 17 and energy == 10113):
        #     draw(state[1])
        #     test = 18
        # elif (hall == (1,1,0,0,0,0,0,0,0,1,4) and test == 18 and energy == 19113):
        #     draw(state[1])
        #     test = 19
        # elif (hall == (1,1,0,2,0,0,0,0,0,1,4) and test == 19 and energy == 19133):
        #     draw(state[1])
        #     test = 20
        # elif (hall == (1,1,0,0,0,0,0,0,0,1,4) and test == 20 and energy == 19153):
        #     draw(state[1])
        #     test = 21
        # elif (hall == (1,1,0,4,0,0,0,0,0,1,4) and test == 21 and energy == 22153):
        #     draw(state[1])
        #     test = 22
        # elif (hall == (1,1,0,0,0,0,0,0,0,1,4) and test == 22 and energy == 30153):
        #     draw(state[1])
        #     test = 23
        # elif (hall == (1,1,0,4,0,0,0,0,0,1,4) and test == 23 and energy == 34153):
        #     draw(state[1])
        #     test = 24
        # elif (hall == (1,1,0,0,0,0,0,0,0,1,4) and test == 24 and energy == 41153):
        #     draw(state[1])
        #     test = 25
        # elif (hall == (1,0,0,0,0,0,0,0,0,1,4) and test == 25 and energy == 41157):
        #     draw(state[1])
        #     test = 26
        # elif (hall == (0,0,0,0,0,0,0,0,0,1,4) and test == 26 and energy == 41161):
        #     draw(state[1])
        #     test = 27
        # elif (hall == (0,0,0,0,0,0,0,0,0,0,4) and test == 27 and energy == 41169):
        #     draw(state[1])
        #     test = 28
        # elif (hall == (0,0,0,0,0,0,0,0,0,0,0) and test == 28 and energy == 44169):
        #     draw(state[1])
        #     test = 29
        # else:
        #     continue