from data import ROOMS
#logic for picking up items.
def pick_up_item(user_input, room, current_inventory): # Function to pick up an item.

    if user_input.startswith('get '): #Check if the user input starts with 'get '.

        item_to_get = user_input.split(' ', 1)[1] #Extract the item name from the user input.

        if 'item' in ROOMS[room] and item_to_get == ROOMS[room]['item']: #Check if the item is in the current room.

            current_inventory.append(item_to_get)   #Add the item to the player's inventory.

            del ROOMS[room]['item']  #Remove the item from the room after picking it up.

            print("\n**" + item_to_get + " has been added to your inventory!**") #Notify the player that the item has been added to the inventory.