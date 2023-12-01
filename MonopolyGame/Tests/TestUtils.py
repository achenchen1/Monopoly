from MonopolyGame import Utils

if __name__ == "__main__":
    x = list(range(10))
    print(x)
    x = Utils.Ring(x)
    print(x)
    x.append(10)
    x.append(11)
    print(x)

    it = iter(x)
    for i in range(15):
        print(next(it))
    print("pop", x.pop(11))
    print(x)
    for i in range(10):
        print(next(it))
    print("pop", x.pop(5))
    for i in range(10):
        print(next(it))

    while len(x) > 1:
        print("pop", x.pop(next(x).value))
    print(x)
