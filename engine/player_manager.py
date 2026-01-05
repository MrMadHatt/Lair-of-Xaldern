import sqlite3

def load_player_stats(cursor):
    #Loads basic player stats. If no player exists, creates a default one.
    cursor.execute("SELECT hp, max_hp, attack, defense, current_room FROM player_stats WHERE id = 1")
    row = cursor.fetchone()
    if row:
        return dict(row)
    else:
        # Default start stats
        return {'hp': 100, 'max_hp': 100, 'attack': 10, 'defense': 5, 'current_room': 100}

def save_player_stats(player, cursor, conn):
    #Saves current player health and location to the database.
    cursor.execute('''
        UPDATE player_stats 
        SET hp = ?, current_room = ? 
        WHERE id = 1
    ''', (player['hp'], player['current_room']))
    conn.commit()

def load_player_inventory(cursor):
    """
    Fetches item names from the inventory table.
    This allows the inventory list in Main.py to persist across sessions.
    """
    cursor.execute('''
        SELECT items.name 
        FROM inventory 
        JOIN items ON inventory.item_id = items.id
    ''')
    # Returns a list of strings: ["Dull Sword", "Health Potion"]
    return [row[0] for row in cursor.fetchall()]