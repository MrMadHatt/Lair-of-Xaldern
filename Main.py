import sys # Importing sys module for system-specific parameters and functions.

from movement import get_new_room # Import the ROOMS dictionary from the data module.

from interface import show_status, show_instructions # Import the show_status function from the interface module.

from item_management import pick_up_item

 # Import the get_new_room function from the movement module.

current_room = 'Elaborate Entrance Hall' # Set the starting room for the player.

inventory = [] # Initialize an empty list to hold the player's inventory items.

game_status = 'playing' # Initialize the game status to 'playing'.

def main(): # Main function to run the game loop.

    global current_room, inventory, game_status # Declare global variables to modify them within the function.

    while game_status == 'playing': # Continue the game loop while the game status is 'playing'.

        show_status(current_room, inventory) # Display the player's current status.

        user_input = input("> ").lower() # Get user input and convert it to lowercase.

        if user_input == 'quit': # Check if the user wants to quit the game.
            
            global game_status # Declare game_status as global to modify it.
            
            game_status = 'quit' # Set the game status to 'quit' to exit the loop.

            print("Thanks for playing! Goodbye.") # Print a goodbye message.

            continue # Skip the rest of the loop and start the next iteration.
