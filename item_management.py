# Import the ROOMS data structure from the data module.
from data import ROOMS

#logic for picking up items.
def pick_up_item(user_input, room, current_inventory):

# Check if the user input starts with 'get ' to pick up an item.
    if user_input.startswith('get '): 
        item_to_get = user_input.split(' ', 1)[1] 

#Check if the item is present in the current room and not already in inventory.
        if 'item' in ROOMS[room] and item_to_get.lower() == ROOMS[room]['item'].lower(): 
            current_inventory.append(item_to_get) 

# Remove the item from the room after picking it up.
            del ROOMS[room]['item']  
            print("\n**" + item_to_get + " has been added to your inventory!**")