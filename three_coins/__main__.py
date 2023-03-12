import three_coins.coin as coin
import three_coins.line as line
import three_coins.db.conn as conn
from three_coins.hexagram import Hexagram


def main():
    hexagram = Hexagram()
    input('Enter your question, focus on it, and press ENTER to start tossing coins: \n')

    count = 0
    while count < 6:
        coin_toss_result = coin.toss_three()
        hexagram.__add__(count, coin_toss_result)
        count += 1

    reversed_binary = hexagram.__reversed__()
    reversed_hexagram = conn.get_by_binary(reversed_binary)

    print(reversed_hexagram)
