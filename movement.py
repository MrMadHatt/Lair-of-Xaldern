# Importing the ROOMS dictionary from the data module.
from data import ROOMS

#Logic for moving between rooms.
def get_new_room(user_move, current_room): 

# Check if the user input starts with 'go ' to move to a new room.
    if user_move.startswith('go '):
        direction = user_move.split()[1]

# Check if the direction is valid for the current room.
        if direction in ROOMS[current_room]: 
            return ROOMS[current_room][direction]
        
        #Notify the player of an invalid move.
        else:
            print("YOU SHALL NOT PASS! Invalid move. ")
            
            # Return the current room if the move is invalid.
    return current_room 