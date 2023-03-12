from art import *


def intro() -> None:
    tprint('Three Coins', 'thin')
    print('Copyright (c) 2023 Filip Krnjaković')
    print('github.com/filip-kr/three-coins \n')
    input('Enter your question, focus on it, and press ENTER to start tossing coins: \n')


def newline() -> None:
    print('\n')


def loading(step: int) -> None:
    if step == 6:
        msg = 'Hexagrams ready'
    else:
        msg = str(step) + '/6'

    input(art('loading' + str(step)) + msg)


def draw_line(coin_toss_result: int) -> None:
    half_line = __draw_yy(9) + ' ' * 9 + __draw_yy(9) + '\033[0;0m'
    full_line = __draw_yy(27) + '\033[0;0m'

    match coin_toss_result:
        case 6:
            print('\033[0;31m' + half_line)
        case 7:
            print('\033[0;32m' + full_line)
        case 8:
            print('\033[0;32m' + half_line)
        case 9:
            print('\033[0;31m' + full_line)


def hex_info(hexagram: tuple) -> None:
    print('#' + str(hexagram[0]))
    print(str(hexagram[1]))


def __draw_yy(char_count: int) -> str:
    yin_yang = ''

    count = 0
    while count < char_count:
        yin_yang += chr(9775)
        count += 1

    return yin_yang
