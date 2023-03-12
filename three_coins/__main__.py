import three_coins.helper.bit as bit_helper
import three_coins.helper.coin as coin
import three_coins.db.conn as conn


def main():
    input('Enter your question, focus on it, and press ENTER to start tossing coins: \n')

    lines = []
    binary = []
    reverse_binary = []

    count = 0
    while count < 6:
        coin_toss_result = coin.toss_three()
        lines.insert(count, coin_toss_result)
        bit = bit_helper.get(coin_toss_result)
        binary.insert(count, str(bit))
        reverse_bit = 0 if bit else 1
        reverse_binary.insert(count, str(reverse_bit))

        count += 1

    hexagram = conn.get_by_binary(binary)
    reverse_hexagram = conn.get_by_binary(reverse_binary)

    print(hexagram)
    print(reverse_hexagram)
