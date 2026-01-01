import engine.item_management as item_mgr

def format_item_name(name):
    """
    Cleans up database names for display.
    Converts 'hunter_s_bow' to 'Hunter's Bow'.
    """
    if not name:
        return "Unknown Item"
    
    # 1. Replace underscores with spaces
    # 2. Use .title() for standard capitalization
    # 3. Fix the apostrophe issue (converts 'S to 's)
    formatted = str(name).replace('_', ' ').title().replace("'S", "'s")
    return formatted

def show_status(room_data, current_inventory, player_health, cursor):
    """
    Displays the current state of the game to the player.
    """
    room_name = room_data.get('name', 'Unknown Location')
    health_bar = ("\u2665" + " ") * (player_health // 10)

    # --- Top Status Bar ---
    print("-" * 40)
    print(f"Location: {room_name}")
    print(f"Health:   {health_bar} ({player_health}%)")
    
    # Format inventory for display
    display_inv = [format_item_name(item) for item in current_inventory]
    print(f"Inventory: {', '.join(display_inv) if display_inv else 'Empty'}")
    print("-" * 40)

    # --- Room Description ---
    print(f"\nYou are in the {room_name}.")

    # --- Exits Logic ---
    VALID_DIRECTIONS = ['north', 'east', 'south', 'west']
    available_moves = [
        direction.capitalize() for direction in VALID_DIRECTIONS
        if room_data.get(direction) not in [None, "null", "", 0]
    ]
    print("Exits: " + ", ".join(available_moves))

    # --- Items in Room ---
    # We fetch fresh from DB to ensure sync with Main.py
    room_items = item_mgr.get_room_items(cursor, room_data['id']) 
    if room_items:
        print("") # Extra spacing for readability
        for item in room_items:   
            print(f"You see a {format_item_name(item)} here.")

def show_instructions():
    """
    Prints the help menu.
    """
    print('\n' + '='*30)
    print('   LAIR OF XALDERN   ')
    print('='*30)
    print("Commands: 'Go [direction]', 'Get [item]', 'Drop [item]', 'Quit'") 
    print("Directions: North, East, South, West ") 
    print("-" * 30) 
    print("Quest: Find the Sword of Gilathis and defeat the Dragon!") 
    print('='*30 + '\n')