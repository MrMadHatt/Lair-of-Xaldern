# Place for notes about changes or tasks worked on:

import sys # Importing sys module for system-specific parameters and functions.

from movement import get_new_room # Import the ROOMS dictionary from the data module.

from interface import show_status, show_instructions # Import the show_status function from the interface module.

from item_management import pick_up_item

 # Import the get_new_room function from the movement module.

current_room = 'elaborate entrance hall'.title() # Set the starting room for the player.

inventory = [] # Initialize an empty list to hold the player's inventory items.

game_status = 'playing' # Initialize the game status to 'playing'.

def main(): # Main function to run the game loop.

    show_instructions() # Display the game instructions at the start.

    global current_room, inventory, game_status # Declare global variables to modify them within the function.

    while game_status == 'playing': # Continue the game loop while the game status is 'playing'.

        show_status(current_room, inventory) # Display the player's current status.

        user_input = input("> ").upper().lower() # Get user input and convert it to uppercase.

        if user_input == 'QUIT': # Check if the user wants to quit the game.
            
            game_status = 'Quit' # Set the game status to 'quit' to exit the loop.

            print("Thanks for playing! Goodbye.") # Print a goodbye message.

            continue # Skip the rest of the loop and start the next iteration.
        
        if user_input.startswith('command'.upper().lower()): #Displays available commands to player upon request.

            print("Available Commands: 'go [direction]'.title(), 'get [item]'.title(), 'quit'") # Display available commands to the player.

        pick_up_item(user_input, current_room, inventory) # Call the function to pick up an item if applicable.

        current_room = get_new_room(user_input, current_room) # Call the function to get the new room based on user movement.

if __name__ == '__main__': # Check if the script is being run directly.

    main() # Call the main function to start the game.