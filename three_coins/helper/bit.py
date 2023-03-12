def get(coin_toss_result: int) -> int:
    if coin_toss_result == 6 or coin_toss_result == 8:
        bit = 0
    else:
        bit = 1

    return bit
