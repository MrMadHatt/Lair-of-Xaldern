import sqlite3
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "data", "game_data.db")

__all__ = ["check_for_enemies", "DB_PATH"]


def check_for_enemies(room_id, cursor):

    sql_query = """
        SELECT e.id, e.name, re.current_hp, e.attack, e.description
        FROM room_enemies re
        JOIN enemies e ON re.enemy_id = e.id
        WHERE re.room_id = ? AND re.is_alive = 1
"""

    cursor.execute(sql_query, (room_id,))

    return cursor.fetchone()


# Test
if __name__ == "__main__":
    print("--- DEBUG INFO ---")
    print(f"Current Script Location: {CURRENT_DIR}")
    print(f"Looking for Database at: {DB_PATH}")
    print("------------------")

    conn = sqlite3.connect(DB_PATH)
    test_cursor = conn.cursor()

    test_room_id = 105
    result = check_for_enemies(test_room_id, test_cursor)

    if result:
        e_id, name, hp, attack, desc = result
        print(f"SUCCESS: A {name} appeared!")
        print(f"Stats -> HP: {hp}, Attack: {attack}")
        print(f"Description: {desc}")
    else:
        print(f"DATABASE CHECK: Room {test_room_id} is safe...(for now).")
    conn.close()
