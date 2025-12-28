#Logic to display the player's current status.
def show_status(room, current_inventory, player_health, ROOMS):

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

    # Define directions using whitelist, not blacklist
    VALID_DIRECTIONS = ['north', 'east', 'south', 'west']
    
    # Display available moves from the current room.
    available_moves = [
    direction for direction in VALID_DIRECTIONS
    if direction in ROOMS[room] and ROOMS[room][direction] not in [None, "null", ""]]

    # Display available exits from the current room.
    print("\nExits: " + ", ".join(available_moves)) 

    # Check and display any items present in the current room.
    if 'items' in ROOMS[room] and ROOMS[room]['items']:
        for item_name in ROOMS[room]['items']:     
            print(f"You see a {str(item_name).title()} here.")


    # Function to show game instructions to the player.
def show_instructions():
    print(' ---- Lair of Xaldern ----')
    print("-" * 80) 
    print("Commands: 'Go [direction]', 'Get [item]', 'Quit'") 
    print("Directions: North, East, South, West ") 
    print("-" * 80) 
    print("Quest: Find the Sword of Gilathis and defeat Xaldern the Three-Headed Dragon!") 
    print("-" * 80) 
    print("\nGood luck, brave hero!\n")