# Place for notes about changes or tasks worked on:

import sys # Importing sys module for system-specific parameters and functions.

from movement import get_new_room # Import from the movement module.

from interface import show_status, show_instructions # Import the show_status function from the interface module.

from item_management import pick_up_item    #Import the pick_up_item function from the item_management module.

from combat import check_combat #Import the check_combat function from the combat module.

def main(): # Main function to run the game loop.


    # --- FIX: Move variables INSIDE main() to avoid scope errors ---
    current_room = 'elaborate entrance hall' # Set the starting room (lowercase to match data.py keys)

    inventory = [] # Initialize an empty list for inventory.
    
    game_status = 'playing' # Initialize game status.

    show_instructions() # Display instructions once at start.

    while game_status == 'playing': # Game loop.

        show_status(current_room, inventory) # Display status.
        
        user_input = input("> ").lower().strip() # Get input, lower it, and strip whitespace.

        # --- Game Logic ---
        if user_input == 'quit': # Quit the game
            game_status = 'quit' # Ends the loop
            print("Thanks for playing! Goodbye.") # Farewell message

        elif user_input.startswith('go '): # Move to a new room
            # Capture the returned room!
            current_room = get_new_room(user_input, current_room)

        elif user_input.startswith('get '): # Pick up item
            # Pass the list 'inventory' which is mutable, so it updates automatically
            pick_up_item(user_input, current_room, inventory) 

        elif user_input == 'command' or user_input == 'commands': # Show available commands
            print("Available Commands: 'go [direction]', 'get [item]', 'quit'") 

        else:   
            print("Invalid Command.") # Notify the player of an invalid command.

if __name__ == '__main__':  # Entry point of the program
    main()  # Call the main function to start the game