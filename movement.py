#Logic for moving between rooms.
def get_new_room(user_move, current_room, ROOMS): 
    move = user_move.lower().strip()

    # Check if the user input starts with 'go ' to move to a new room.
    if move.startswith('go '):
        parts = move.split()

        if len(parts) >= 2:
            direction = parts[1]

            # Use .get() to avoid crashing if 'direction' isn't in the room data.
            destination = ROOMS[current_room].get(direction)   

            # Check if the direction is valid for the current room.
            if destination in ROOMS:
                return destination
        
            #Notify the player of an invalid move.
            else:
                if destination in [None, "null", " "]:
                               print("YOU SHALL NOT PASS!")
                else:
                    print(f"The path to '{destination}' is under construction! ")
            
                return current_room
            
            # Return the current room if the move is invalid.
        return current_room 