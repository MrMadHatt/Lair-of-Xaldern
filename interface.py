    # Import necessary data from the data module.
from data import ROOMS

    #Logic to display the player's current status.
def show_status(room, current_inventory, player_health):

    display_room = room.title()
    display_inventory = [item.title() for item in current_inventory]

    health_bar = ("\u2665" + " ") * (player_health // 10)

    print("-" * 40)
    print(f"Location: {display_room}")
    print(f"Inventory: {', '.join(display_inventory) if current_inventory else 'Empty'}")
    print(f"Health: {health_bar} ({player_health}%)")
    print("-" * 40)
    
    # Display the current room and inventory.
    print(f"You are in the {display_room}.")

    # Define non-direction keys to filter out from room connections.
    NON_DIRECTION_KEYS = ['item', 'object']
    
    # Display available moves from the current room.
    available_moves = [key for key in ROOMS[room].keys() if key not in NON_DIRECTION_KEYS] 

    # Display available exits from the current room.
    print("\nExits: " + ", ".join(available_moves)) 

    # Check and display any items present in the current room.
    if 'item' in ROOMS[room]:
        item_name = ROOMS[room]['item']     
        if item_name not in current_inventory: 
            print("You see a {item_name.title()} here.")


    # Function to show game instructions to the player.
def show_instructions():
    print(' ---- Lair of Xaldern ----')
    print("-" * 80) 
    print("Commands: 'Go [direction]', 'Get [item]', 'Quit'") 
    print("Directions: North, South, East, West ") 
    print("-" * 80) 
    print("Quest: Find the Sword of Gilathis and defeat Xaldern the Three-Headed Dragon!") 
    print("-" * 80) 
    print("\nGood luck, brave hero!\n")