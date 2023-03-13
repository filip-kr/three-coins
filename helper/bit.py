def get(coin_toss_result: int) -> int:
    return 0 if coin_toss_result == 6 or coin_toss_result == 8 else 1


def get_reverse(coin_toss_result: int) -> int:
    return 1 if coin_toss_result == 6 or coin_toss_result == 7 else 0
