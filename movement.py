# Importing the ROOMS dictionary from the data module.
import json

try:
#Loading the world data from a JSON file.
    with open('world.json') as f:
        ROOMS = json.load(f)
except FileNotFoundError:
    print("Error: world.json file not found.")
    ROOMS = {}

#Logic for moving between rooms.
def get_new_room(user_move, current_room): 
    move = user_move.lower().strip()

# Check if the user input starts with 'go ' to move to a new room.
    if move.startswith('go '):
        parts = move.split()

    if len(parts) >= 2:
        direction = parts[1]   

# Check if the direction is valid for the current room.
        if direction in ROOMS[current_room]: 
            return ROOMS[current_room][direction]
        
        #Notify the player of an invalid move.
        else:
            print("YOU SHALL NOT PASS! Invalid move. ")
            
            # Return the current room if the move is invalid.
    return current_room 