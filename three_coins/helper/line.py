red = '\033[0;31m'
green = '\033[0;32m'
color_reset = '\033[0;0m'


def draw(coin_toss_result: int) -> str:
    half_line = __draw_yy(9) + ' ' * 9 + __draw_yy(9) + color_reset
    full_line = __draw_yy(27) + color_reset

    match coin_toss_result:
        case 6:
            return red + half_line
        case 7:
            return green + full_line
        case 8:
            return green + half_line
        case 9:
            return red + full_line


def __draw_yy(char_count: int) -> str:
    yin_yang = ''

    count = 0
    while count < char_count:
        yin_yang += chr(9775)
        count += 1

    return yin_yang
