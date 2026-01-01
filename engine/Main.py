import sys
import engine.movement as movement
import engine.interface as interface
import engine.item_management as item_management
import sqlite3
import os

def load_game_data():
    DB_PATH = os.path.join(os.getcwd(), 'data', 'game_data.db')
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rows = cursor.fetchall()

        rooms_dict = {}
        for row in rows:
            rooms_dict[row['id']] = dict(row)
            rooms_dict[row['id']]['items'] = []

        cursor.execute('''
            SELECT room_items.room_id, items.name 
            FROM items 
            JOIN room_items ON items.id = room_items.item_id
        ''')
        for item in cursor.fetchall():
            if item['room_id'] in rooms_dict:
                rooms_dict[item['room_id']]['items'].append(item['name'])

        conn.close()
        return rooms_dict
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def main():
    ROOMS = load_game_data()
    if not ROOMS: return

    current_room_id = 100
    inventory = [] 
    game_status = 'playing'
    player_health = 100

    interface.show_instructions() 

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'game_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    while game_status == 'playing': 
        current_room_data = ROOMS.get(current_room_id)
        interface.show_status(current_room_data, inventory, player_health, cursor)
        
        user_input = input("\n> ").lower().strip()

        if user_input == 'quit':
            game_status = 'quit' 
        elif user_input.startswith('go '):
            new_id = movement.get_new_room(user_input, current_room_id, ROOMS)
            if new_id: current_room_id = new_id
        elif user_input.startswith('get '):
            picked_up = item_management.pick_up_item(conn, user_input, current_room_id, inventory)
            if picked_up and 'items' in current_room_data:
                current_room_data['items'] = [i for i in current_room_data['items'] if i != picked_up]
        elif user_input.startswith('drop '):
            dropped = item_management.drop_item(conn, user_input, current_room_id, inventory)
            if dropped and 'items' in current_room_data:
                current_room_data['items'].append(dropped)
        elif user_input in ['inventory', 'i']:
            print(f"\n🎒 Inventory: {', '.join(inventory) if inventory else 'Empty'}")
        elif user_input in ['help', 'commands']:
            interface.show_instructions()
        else:   
            print("Invalid Command.") 

    conn.close() 

if __name__ == '__main__':
    main()