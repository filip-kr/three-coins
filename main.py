if __name__ == '__main__':
    import three_coins
    import line

    input('Enter your question, focus on it, and press ENTER to start tossing coins\n')

    hexagram = []

    count = 0
    while count < 6:
        coin_toss_result = three_coins.toss()
        hexagram.insert(count, coin_toss_result)

        count += 1
        input('Coin toss: ' + str(count) + '/6')
        print('\nPresent:') if count == 6 else None

    hexagram.reverse()

    for coin_toss_result in hexagram:
        print(line.draw(coin_toss_result))

    print('\n')
