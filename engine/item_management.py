#logic for picking up items.
def pick_up_item(user_input, current_room_data, current_inventory):
    if not user_input.startswith('get '):
        return

    parts = user_input.lower().split(' ', 1)
    if len(parts) < 2:
        print("\nGet What?")
        return
        
    item_to_get = parts[1].strip() 

#Check if the item is present in the current room and not already in inventory.
    room_items = current_room_data.get('items', [])

    match = next((i for i in room_items if i.lower() == item_to_get), None)

    if match:
            current_inventory.append(match) 
            room_items.remove(match)
            print(f"\n** {match.title()} has been added to your inventory! **")
    else:
            print(f"\nThere is no {item_to_get} here!")