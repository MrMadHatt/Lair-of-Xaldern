# Import the ROOMS data structure from the data module.
import json

try:
    with open("world.json", "r") as f:
        ROOMS = json.load(f)
except FileNotFoundError:
    ROOMS = {}

#logic for picking up items.
def pick_up_item(user_input, room, current_inventory):
    parts = user_input.lower().split()

# Check if the user input starts with 'get ' to pick up an item.
    if user_input.startswith('get '):
        if len(parts) < 2:
            print("\nGet what?")
            return
        
        item_to_get = user_input.split(' ', 1)[1] 

#Check if the item is present in the current room and not already in inventory.
        if 'item' in ROOMS[room] and item_to_get.lower() == ROOMS[room]['item'].lower():
            official_name = ROOMS[room]['item'] 
            current_inventory.append(official_name) 

# Remove the item from the room after picking it up.
            del ROOMS[room]['item']  
            print(f"\n** {official_name} has been added to your inventory! **")

        else:
            print(f"\nThere is no {item_to_get} here!")