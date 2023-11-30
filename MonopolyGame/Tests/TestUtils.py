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
    for i in range(10):
        print(next(it))
    print("------")
    for i in range(20):
        print(next(it))
