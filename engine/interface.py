#Logic to display the player's current status.
def show_status(room_data, current_inventory, player_health, ROOMS):

    display_room = str(room_data.get('name', 'Unknown')).title()
    room_name = room_data.get('name', 'Unknown Location')
    display_inventory = [item.title() for item in current_inventory]

    health_bar = ("\u2665" + " ") * (player_health // 10)

    print("-" * 40)
    print(f"Location: {room_name}")
    print(f"Inventory: {', '.join(display_inventory) if current_inventory else 'Empty'}")
    print(f"Health: {health_bar} ({player_health}%)")
    print("-" * 40)
    
    # Display the current room and inventory.
    print(f"You are in the {room_name}.")

    # Define directions using whitelist, not blacklist
    VALID_DIRECTIONS = ['north', 'east', 'south', 'west']
    
    # Display available moves from the current room.
    available_moves = [
        direction.capitalize() for direction in VALID_DIRECTIONS
        if room_data.get(direction) not in [None, "null", "", 0]
    ]
    # Display available exits from the current room.
    print("\nExits: " + ", ".join(available_moves)) 

    # Check and display any items present in the current room.
    if room_data.get('items'):
        for item_name in room_data['items']:     
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