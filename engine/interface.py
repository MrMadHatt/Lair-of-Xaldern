import os

def show_instructions():
    #Displays the help menu for the player.
    print("""
========================================
           GAME INSTRUCTIONS
========================================
Commands:
  go [direction]  - Move (North, South, East, West)
  get [item]     - Pick up an item from the room
  drop [item]    - Leave an item behind
  inventory / i  - View your items
  help           - Show these instructions
  quit           - Save and exit the game
========================================""")

def show_status(room, inventory, hp, cursor):
    # Draws the main game screen including stats and room info. 
    
    # 1. HEADER & LOCATION
    print("=" * 40)
    print(f"📍 LOCATION: {room['name'].upper()}")
    print("-" * 40)

    # 2. PLAYER STATS BAR
    # Creates a heart bar: 100hp = 10 hearts, 50hp = 5 hearts
    hearts = "♥ " * (max(0, hp) // 10)
    empty_hearts = "♡ " * (10 - (max(0, hp) // 10))
    
    print(f"HP: [{hearts}{empty_hearts}] {hp}%")
    
    # Simple inventory count
    inv_count = len(inventory) if inventory else 0
    print(f"🎒 INVENTORY: {inv_count} item(s)")
    print("-" * 40)

    # 3. ROOM DESCRIPTION
    # We use .get() to avoid errors if a key is missing
    print(f"\n{room.get('description', 'You look around, but find nothing of particular note.')}")

    # 4. ITEMS ON THE GROUND
    items_here = room.get('items', [])
    if items_here:
        print("\nYOU SEE:")
        for item in items_here:
            print(f"  ✨ {item}")

    # 5. NAVIGATION / EXITS
    exits = []
    # Check directions in the room dictionary
    for direction in ['north', 'south', 'east', 'west']:
        if room.get(direction):
            exits.append(direction.capitalize())
    
    if exits:
        print(f"\nEXIT ROUTES: {', '.join(exits)}")
    else:
        print("\nThere are no obvious exits. You are trapped!")
    
    print("-" * 40)