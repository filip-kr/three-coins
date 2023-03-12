class LineDrawer:
    red = '\033[0;31m'
    green = '\033[0;32m'
    color_reset = '\033[0;0m'

    @staticmethod
    def draw(coin_toss_result):
        half_line = LineDrawer.__draw_yy(9) + ' ' * 9 + LineDrawer.__draw_yy(9) + LineDrawer.color_reset
        full_line = LineDrawer.__draw_yy(27) + LineDrawer.color_reset

        match coin_toss_result:
            case 6:
                return LineDrawer.red + half_line
            case 7:
                return LineDrawer.green + full_line
            case 8:
                return LineDrawer.green + half_line
            case 9:
                return LineDrawer.red + full_line

    @staticmethod
    def __draw_yy(char_number):
        yin_yang = ''

        count = 0
        while count < char_number:
            yin_yang += chr(9775)
            count += 1

        return yin_yang
