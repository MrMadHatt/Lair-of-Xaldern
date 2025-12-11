from data import ROOMS  #Import the ROOMS dictionary from the data module.

#Logic to display the player's current status.
def show_status(room, current_inventory): # Function to display the player's current status.

    print("\n---------------------" ) # Print a separator line for better readability.
    
    print("You are in the " + room) # Display the current room of the player.

    print("Inventory: " + str(current_inventory)) # Display the player's current inventory.

    # Check for items in the current room.
    if 'item' in ROOMS[room]: # Check if there is an item in the current room.

        item_name = ROOMS[room]['item'] # Get the name of the item in the room.
        
        if item_name not in current_inventory: # Check if the item is not already in the inventory

            print("You see a " + item_name + " here.") # Notify the player of the item in the room.

# Function to display game instructions.
def show_instructions():

    print(' ---- Lair of Xaldern ----') # Display game title.

    print("Commands: 'go [direction]', 'get [item]', 'quit'") # Display available commands to the player.

    print(" Directions: north, south, east, west ") # Display possible movement directions.

    print("-" * 40) # Print a separator line for better readability.

    print("Quest: Find the Sword of Gilathis and defeat Xaldern the three-headed dragon!") # Display the player's quest objective.
    
    print("-" * 40) # Print another separator line for better readability.
    #Logic to display instructions only once at the start of the game.