import sys
import os
import sqlite3
import engine.movement as movement
import engine.interface as interface
import engine.item_management as item_management
from engine.combat import start_combat_loop, get_enemy_in_room
from engine.player_manager import load_player_stats, save_player_stats, load_player_inventory

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_game_data():
    """Loads world data from the DB into a local cache for the session."""
    DB_PATH = os.path.join(os.getcwd(), 'data', 'game_data.db')
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM rooms")
        rooms_dict = {row['id']: dict(row) for row in cursor.fetchall()}
        
        for r_id in rooms_dict: 
            rooms_dict[r_id]['items'] = []

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
    if not ROOMS: 
        print("Error: Could not load game data. Did you run tools/data_sync.py?")
        return

    db_path = os.path.join(os.getcwd(), 'data', 'game_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # --- PERSISTENT DATA LOADING ---
    player = load_player_stats(cursor)
    inventory = load_player_inventory(cursor) # Now loads from DB!
    
    current_room_id = player['current_room']
    game_status = 'playing'
    action_message = "...Awaken, Hero......the world needs your strength once more.........."
    
    clear_screen()
    interface.show_instructions()
    input("\nPress Enter to begin...")

    while game_status == 'playing':
        clear_screen()
        current_room_data = ROOMS.get(current_room_id)
        
        if not current_room_data:
            print(f"Error: Room {current_room_id} not found!")
            break

        player['current_room'] = current_room_id

        # --- COMBAT ---
        enemy = get_enemy_in_room(current_room_id, cursor)
        if enemy:
            print(f"\n⚠️  A wild {enemy[1]} appeared!") 
            combat_result = start_combat_loop(current_room_id, cursor, conn, player)
            if combat_result == "game_over":
                game_status = 'game_over'
                break
            save_player_stats(player, cursor, conn)
            action_message = f"You defeated the {enemy[1]}!"
            clear_screen()

        # --- DISPLAY ---
        interface.show_status(current_room_data, inventory, player['hp'], cursor)
        if action_message:
            print(f"\n💬 {action_message}")
            action_message = ""
            
        user_input = input("\n> ").lower().strip()

        # --- LOGIC ---
        if not user_input: continue

        if user_input == 'quit':
            save_player_stats(player, cursor, conn)
            game_status = 'quit' 
        
        elif user_input.startswith('go '):
            new_id = movement.get_new_room(user_input, current_room_id, ROOMS)
            if new_id: 
                current_room_id = new_id
                save_player_stats(player, cursor, conn)
            else:
                action_message = "You can't go that way."
        
        elif user_input.startswith('get '):
            picked_up = item_management.pick_up_item(conn, user_input, current_room_id, inventory)
            if picked_up:
                if picked_up in current_room_data['items']:
                    current_room_data['items'].remove(picked_up)
                action_message = f"Picked up: {picked_up}"
            else:
                action_message = "That item isn't here."
        
        elif user_input.startswith('drop '):
            dropped = item_management.drop_item(conn, user_input, current_room_id, inventory)
            if dropped:
                current_room_data['items'].append(dropped)
                action_message = f"Dropped: {dropped}"
        
        elif user_input in ['inventory', 'i']:
            inv_str = ", ".join(inventory) if inventory else "Empty"
            action_message = f"🎒 Inventory: {inv_str}"
        
        elif user_input in ['help', 'commands']:
            clear_screen()
            interface.show_instructions()
            input("\nPress Enter to return...")
        
        else:   
            action_message = f"Unknown command: '{user_input}'"

    save_player_stats(player, cursor, conn)
    conn.close()

if __name__ == '__main__':
    main()