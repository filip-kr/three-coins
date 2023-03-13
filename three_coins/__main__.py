from db import conn
from helper import bit, coin


def main():
    lines = []
    binary = []
    reverse_binary = []

    count = 0
    while count < 6:
        coin_toss_result = coin.toss_three()
        lines.insert(count, coin_toss_result)

        line_bit = bit.get(coin_toss_result)
        binary.insert(count, str(line_bit))

        reverse_bit = bit.get_reverse(coin_toss_result)
        reverse_binary.insert(count, str(reverse_bit))

        input(str(count) + '/6')
        count += 1

    hexagram = conn.get_by_binary(binary)
    print(hexagram, lines)

    if 6 not in lines and 9 not in lines:
        exit('No changing lines')

    reverse_hexagram = conn.get_by_binary(reverse_binary)
    print(reverse_hexagram)
