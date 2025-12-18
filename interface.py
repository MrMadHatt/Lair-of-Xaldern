    # Import necessary data from the data module.
from data import ROOMS

    #Logic to display the player's current status.
def show_status(room, current_inventory): 

    # Print a separator line for better readability.
    print("\n------------------------------------------------" )
    
    # Display the current room and inventory.
    print(f"You are in the [room}")
    print("Inventory: " + str(current_inventory)) 

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
            print("You see a " + item_name + " here.") 

    # Function to show game instructions to the player.
def show_instructions():
    print(' ---- Lair of Xaldern ----')
    print("-" * 80) 
    print("Commands: 'Go [direction]', 'Get [item]', 'Quit'") 
    print("Directions: North, South, East, West ") 
    print("-" * 80) 
    print("Quest: Find the Sword of Gilathis and defeat Xaldern the Three-Headed Dragon!") 
    print("-" * 80) 
