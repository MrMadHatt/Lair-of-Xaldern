#importing necessary modules
import sys
import engine.movement as movement
import engine.interface as interface
import engine.item_management as item_management
import sqlite3
import os
##from combat import check_combat


def load_game_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    DB_PATH = os.path.join(os.getcwd(), 'data', 'game_data.db')

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 1. Fetch all rooms
        cursor.execute("SELECT * FROM rooms")
        rows = cursor.fetchall()

        rooms_dict = {}
        for row in rows:
            rooms_dict[row['id']] = dict(row)
            # Initialize an empty items list for each room
            rooms_dict[row['id']]['items'] = []

        # 2. Fetch all items currently in rooms and attach them
        cursor.execute('''
            SELECT room_items.room_id, items.name 
            FROM items 
            JOIN room_items ON items.id = room_items.item_id
        ''')
        item_rows = cursor.fetchall()
        for item in item_rows:
            if item['room_id'] in rooms_dict:
                rooms_dict[item['room_id']]['items'].append(item['name'])

        conn.close() # Connection closes AFTER the loops are done
        return rooms_dict # Return happens AFTER the loops are done
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# Main function to run the game loop.
def main():
    ROOMS = load_game_data()
    if not ROOMS:
        print("Error: No room data found.")
        return

    # Initialize game variables.
    current_room_id = 100
    inventory = [] 
    game_status = 'playing'
    player_health = 100

    interface.show_instructions() 

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'game_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # --- Game Loop ---
    while game_status == 'playing': 
        # 1. Update current room data from the ROOMS dictionary
        current_room_data = ROOMS.get(current_room_id)
        
        if not current_room_data:
            print(f"Error: Room {current_room_id} not found!")
            break

        # 2. Show the interface (Calling the function, not defining it)
        interface.show_status(current_room_data, inventory, player_health, cursor)
        
        # 3. Get Input
        user_input = input("\n> ").lower().strip()

        # --- Game Logic (All correctly indented inside the loop now) ---
        if user_input == 'quit':
            game_status = 'quit' 
            print("Til' next time, Hero. Thanks for playing!")

        elif user_input.startswith('go '):
            new_id = movement.get_new_room(user_input, current_room_id, ROOMS)
            if new_id:
                current_room_id = new_id
                print("\n" + "="*20)

        elif user_input.startswith('get '):
            item_name = user_input.replace('get ', '').strip().lower()
            
            # 1. Remove from Database
            item_management.pick_up_item(conn, user_input, current_room_id, inventory)
    
            # 2. Remove from Local Memory
            if 'items' in current_room_data:
                current_room_data['items'] = [i for i in current_room_data['items'] if i.lower() != item_name]
            
        elif user_input in ['help', 'commands']:
            interface.show_instructions()

        elif user_input in ['inventory', 'i']:
            print(f"\n🎒 Inventory: {', '.join(inventory) if inventory else 'Empty'}")

        else:   
            print("Invalid Command.") 

    # --- End of while loop ---
    conn.close() 

    # Main game loop ends here.
if __name__ == '__main__':

    #Entry point of the program.
    main()
