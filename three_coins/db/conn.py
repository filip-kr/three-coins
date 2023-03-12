import apsw

db_file = 'three_coins/db/three_coins.db'


def get_by_binary(binary: str) -> list:
    conn = apsw.Connection(db_file, flags=apsw.SQLITE_OPEN_READONLY)
    cursor = conn.cursor()
    query = 'SELECT * FROM hexagrams WHERE binary = ? LIMIT 1'
    hexagram = cursor.execute(query, [binary]).fetchall()
    conn.close()

    return hexagram
