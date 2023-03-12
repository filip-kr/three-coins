if __name__ == '__main__':
    from hexagram import Hexagram
    from coin import Coin
    from linedrawer import LineDrawer

    hexagram = Hexagram()
    input('Enter your question, focus on it, and press ENTER to start tossing coins: ')
    print('\nCoin toss round:')

    count = 0
    while count < 6:
        hexagram.__add__(count, Coin.toss_three())
        count += 1
        input(str(count) + '/6')

    hex_lines = hexagram.__reversed__()
    hex_binary = hexagram.__str__()

    print('\nPRESENT:')
    for hex_line in hex_lines:
        print(LineDrawer.draw(hex_line))

    print(hex_binary)
