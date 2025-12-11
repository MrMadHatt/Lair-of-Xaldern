from data import ROOMS # Importing the ROOMS dictionary from the data module.
#Logic for moving between rooms.
def get_new_room(user_move, current_room): # Function to get the new room based on user movement.

    if user_move.startswith('go '): # Check if the user input starts with 'go '.

        direction = user_move.split() [1] # Extract the direction from the user input.

        if direction in ROOMS[current_room]: # Check if the direction is valid for the current room.

            return ROOMS[current_room][direction] # Return the new room based on the direction.
        
        else:

            print("YOU SHALL NOT PASS! Invalid move. ") # Notify the player of an invalid move.

        return current_room # Return the current room if the move is invalid.
