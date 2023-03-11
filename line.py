def draw(coin_toss_result):
    red = '\033[0;31m'
    green = '\033[0;32m'
    color_reset = '\033[0;0m'
    half_line = draw_yy(9) + draw_empty(9) + draw_yy(9) + color_reset
    full_line = draw_yy(27) + color_reset

    match coin_toss_result:
        case 6:
            return red + half_line
        case 7:
            return green + full_line
        case 8:
            return green + half_line
        case 9:
            return red + full_line


def draw_yy(char_number):
    yin_yang = ''

    count = 0
    while count < char_number:
        yin_yang += chr(9775)
        count += 1

    return yin_yang


def draw_empty(char_number):
    empty = ''

    count = 0
    while count < char_number:
        empty += ' '
        count += 1

    return empty
