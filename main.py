if __name__ == '__main__':
    import three_coins

    input('Enter your question, focus on it, and press ENTER to start tossing coins\n')

    count = 1
    hexagram = []

    while count < 7:
        line = three_coins.toss()
        hexagram.insert(0, line)

        print(str(count) + ' : ' + str(hexagram[0]))

        count += 1
        input()

    hexagram.reverse()
    print(hexagram)
