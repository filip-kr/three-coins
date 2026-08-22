import os
import sys

import apsw

_db_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
_db_file = os.path.join(_db_dir, 'hexagrams.db')
_connection = apsw.Connection(_db_file, flags=apsw.SQLITE_OPEN_READONLY)


def get_by_binary(binary: list) -> tuple:
    query = 'SELECT * FROM hexagrams WHERE binary = ? LIMIT 1'
    binding = [''.join(binary)]
    cursor = _connection.cursor()
    row = cursor.execute(query, binding).fetchone()

    if row is None:
        raise ValueError(f'No hexagram found for binary {binding[0]!r}')

    return row
