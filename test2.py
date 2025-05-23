
d = {
    "A": [1,5,6,3],
    "B": [6,3],
    "C": [15,6,3],
    "D": [1,5,6,3,7],
    "E": [1,5,6,3],
    "F": [1,3],
}

if __name__ == "__main__":
    for value in d.values():
        print(len(value))
    print(type(d.values()))
    shortest = min(d, key=lambda x: len(d[x]))
    print(shortest)