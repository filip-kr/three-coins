if __name__ == '__main__':
    import three_coins

    input('Enter your question, focus on it, and press ENTER to start tossing coins')

    count = 0
    while count < 6:
        print(three_coins.toss())
        count += 1
