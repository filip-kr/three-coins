if __name__ == '__main__':
    import three_coins
    import line

    input('Enter your question, focus on it, and press ENTER to start tossing coins: ')
    print('\nCoin toss round:')

    hexagram = []
    binary = []

    count = 0
    while count < 6:
        coin_toss_result = three_coins.toss()
        hexagram.insert(count, + coin_toss_result)

        if coin_toss_result == 6 or coin_toss_result == 8:
            binary.insert(count, '0')
        else:
            binary.insert(count, '1')

        count += 1
        input(str(count) + '/6')

    hexagram.reverse()
    binary = ''.join(binary)

    print('\nPRESENT:')

    for coin_toss_result in hexagram:
        print(line.draw(coin_toss_result))

    print(binary)
