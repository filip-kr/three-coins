import three_coins.coin as coin
import three_coins.line as line
from three_coins.hexagram import Hexagram


def main():
    hexagram = Hexagram()
    input('Enter your question, focus on it, and press ENTER to start tossing coins: ')
    print('\nCoin toss round:')

    count = 0
    while count < 6:
        hexagram.__add__(count, coin.toss_three())
        count += 1
        input(str(count) + '/6')

    hex_lines = hexagram.__reversed__()
    hex_binary = hexagram.__str__()

    print('\nPRESENT:')
    for hex_line in hex_lines:
        print(line.draw(hex_line))

    print(hex_binary)
