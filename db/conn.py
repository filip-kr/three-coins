import apsw


def get_by_binary(binary: list) -> tuple:
    db_file = 'db/hexagrams.db'
    query = 'SELECT * FROM hexagrams WHERE binary = ? LIMIT 1'
    binding = [''.join(binary)]
    conn = apsw.Connection(db_file, flags=apsw.SQLITE_OPEN_READONLY)
    cursor = conn.cursor()
    hexagram = cursor.execute(query, binding).fetchall()
    conn.close()

    return hexagram[0]
