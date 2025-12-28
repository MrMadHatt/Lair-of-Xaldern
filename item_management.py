#logic for picking up items.
def pick_up_item(user_input, room, current_inventory, ROOMS):
    parts = user_input.lower().split()

# Check if the user input starts with 'get ' to pick up an item.
    if user_input.startswith('get '):
        if len(parts) < 2:
            print("\nGet what?")
            return
        
        item_to_get = user_input.split(' ', 1)[1].lower().strip() 

#Check if the item is present in the current room and not already in inventory.
        room_items = ROOMS[room].get('items', [])

        match = next((i for i in room_items if i.lower() == item_to_get), None)

        if match:
            current_inventory.append(match) 
            room_items.remove(match)
            print(f"\n** {match.title()} has been added to your inventory! **")
        else:
            print(f"\nThere is no {item_to_get} here!")