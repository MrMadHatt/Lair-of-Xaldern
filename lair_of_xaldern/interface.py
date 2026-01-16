def show_instructions():
    rule = "=" * 60
    print(
        f"""
{rule}
                GAME INSTRUCTIONS
{rule}
Commands:
  go [direction] - Move (North, South, East, West)
  get [item]     - Pick up an item from the room
  drop [item]    - Leave an item behind
  inventory / i  - View your items
  help           - Show these instructions
  quit           - Save and exit the game

{rule}"""
    )
def show_status(room, inventory, hp, cursor):
    _ = cursor 
    print("=" * 60)
    print(f" LOCATION: {room['name'].upper()}")
    print("-" * 60)

    hearts = "♥ " * (max(0, hp) // 10)
    empty_hearts = "♡ " * (10 - (max(0, hp) // 10))

    print(f" HP: [{hearts}{empty_hearts}] {hp}%")

    inv_count = len(inventory) if inventory else 0
    print(f" INVENTORY: {inv_count} item(s)")
    print("-" * 60)

    print(
        f"\n{room.get('description', 'You look around, but find nothing of particular note.')}"
    )

    items_here = room.get("items", [])
    if items_here:
        print("\nYOU SEE:")
        for item in items_here:
            print(f"  ✨ {item}")

    exits = []

    for direction in ["north", "south", "east", "west"]:
        if room.get(direction):
            exits.append(direction.capitalize())

    if exits:
        print(f"\nEXIT ROUTES: {', '.join(exits)}")
    else:
        print("\nThere are no obvious exits. You are trapped!")

    print("-" * 60)
