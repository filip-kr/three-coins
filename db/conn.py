import apsw
import os
import sys

__db_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
__db_file = os.path.join(__db_dir, 'hexagrams.db')


def get_by_binary(binary: list) -> tuple:
    query = 'SELECT * FROM hexagrams WHERE binary = ? LIMIT 1'
    binding = [''.join(binary)]
    conn = apsw.Connection(__db_file, flags=apsw.SQLITE_OPEN_READONLY)
    cursor = conn.cursor()
    hexagram = cursor.execute(query, binding).fetchall()
    conn.close()

    return hexagram[0]
