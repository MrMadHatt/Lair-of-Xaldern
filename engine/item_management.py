import sqlite3
import engine.interface as interface

def get_room_items(cursor, room_id):
    """Returns a list of item names for a specific room."""
    query = """
        SELECT i.name 
        FROM items i
        JOIN room_items ri ON i.id = ri.item_id
        WHERE ri.room_id = ?
    """
    cursor.execute(query, (room_id,))
    return [row[0] for row in cursor.fetchall()]

def pick_up_item(conn, user_input, room_id, current_inventory):
    """Processes 'get [item]' command and updates the database."""
    if not user_input.startswith('get '):
        return

    item_to_get = user_input.lower().replace('get ', '').strip()
    cursor = conn.cursor()

    # Search for item in this specific room
    query = """
        SELECT i.id, i.name 
        FROM items i
        JOIN room_items ri ON i.id = ri.item_id
        WHERE ri.room_id = ? AND LOWER(i.name) = ?
    """
    cursor.execute(query, (room_id, item_to_get))
    match = cursor.fetchone()

    if match:
        item_id, item_name = match
        # REMOVE from the world database
        cursor.execute("DELETE FROM room_items WHERE room_id = ? AND item_id = ?", (room_id, item_id))
        conn.commit()
        
        # ADD to the player's inventory
        current_inventory.append(item_name)
        clean_name = interface.format_item_name(item_name)
        print(f"\n** {clean_name} has been added to your inventory! **")
    else:
        print(f"\nThere is no '{clean_name}' here!")