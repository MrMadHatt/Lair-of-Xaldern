#importing necessary modules
import sys
import movement
from interface import show_status, show_instructions 
from item_management import pick_up_item
import sqlite3
import os
##from combat import check_combat


def load_game_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    DB_PATH = os.path.join(base_dir, 'data', 'game_data.db')

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

    show_instructions() 


    # --- Game Loop ---
    while game_status == 'playing': 

        current_room_data = ROOMS.get(current_room_id)

        #temp debug line
        print(f"DEBUG: Current Room Items: {current_room_data.get('items')}")

        if not current_room_data:
            print(f"Error: Room {current_room_id} not found in database!")
            break

        show_status(current_room_data, inventory, player_health, ROOMS)
        
        user_input = input("> ").lower().strip()

        # --- Game Logic ---
        if user_input == 'quit':
            game_status = 'quit' 
            print("Til' next time, Hero. Thanks for playing!")

        # Check if user input starts with 'go ' to move to a new room.
        elif user_input.startswith('go '):
            old_id = current_room_id
            new_id = movement.get_new_room(user_input, current_room_id, ROOMS)
            if new_id:
                current_room_id = new_id

            if old_id != current_room_id:
                print("\n" + "="*20)

        # Check if user input starts with 'get ' to pick up an item.
        elif user_input.startswith('get '):
            pick_up_item(user_input, current_room_data, inventory) 


        # Display available commands when called by the user.
        elif user_input in ['command', 'commands', 'help']:
            print("Available Commands: 'go [direction]', 'get [item]', 'quit'") 
        
        # Check current inventory.
        elif user_input in ['inventory', 'i']:
            if not inventory:
                print("\nYour inventory is empty.")
            else:
                print("\n🎒 Your Inventory: " + ", ".join(inventory))

        # If none of the above, notify user of invalid command.
        else:   
            print("Invalid Command.") 

    # Main game loop ends here.
if __name__ == '__main__':

    #Entry point of the program.
    main()
