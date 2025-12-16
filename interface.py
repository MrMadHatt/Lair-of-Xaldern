from data import ROOMS  #Import the ROOMS dictionary from the data module.

#Logic to display the player's current status.
def show_status(room, current_inventory): # Function to display the player's current status.

    print("\n------------------------------------------------" ) # Print a separator line for better readability.
    
    print("You are in the " + room) #Display the current room the player is in.
    print("Inventory: " + str(current_inventory)) # Display the player's current inventory.

    NON_DIRECTION_KEYS = ['item', 'object'] # Define keys that are not directions.

    available_moves = [key for key in ROOMS[room].keys() if key not in NON_DIRECTION_KEYS] # Get available movement directions from the current room.

    print("\nExits: " + ", ".join(available_moves)) # Display available exits from the current room.

    # Check for items in the current room.
    if 'item' in ROOMS[room]: # Check if there is an item in the current room.

        item_name = ROOMS[room]['item'] # Get the name of the item in the room.
        
        if item_name not in current_inventory: # Check if the item is not already in the inventory

            print("You see a " + item_name + " here.") # Notify the player of the item in the room.

# Function to display game instructions.
def show_instructions():

    print(' ---- Lair of Xaldern ----') # Display game title.

    print("-" * 80) # Print a separator line for better readability.

    print("Commands: 'Go [direction]', 'Get [item]', 'Quit'") # Display available commands to the player.

    print("Directions: North, South, East, West ") # Display possible movement directions.

    print("-" * 80) # Print a separator line for better readability.

    print("Quest: Find the Sword of Gilathis and defeat Xaldern the Three-Headed Dragon!") # Display the player's quest objective.
    
    print("-" * 80) # Print another separator line for better readability.
    #Logic to display instructions only once at the start of the game.