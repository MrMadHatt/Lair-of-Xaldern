#importing necessary modules
import sys
import movement
from interface import show_status, show_instructions 
from item_management import pick_up_item    
#from combat import check_combat


# Main function to run the game loop.
def main():


    # Initialize game variables.
    current_room = 'elaborate entrance hall' 
    inventory = [] 
    game_status = 'playing'
    player_health = 100

    show_instructions() 


    # --- Game Loop ---
    while game_status == 'playing': 

        show_status(current_room, inventory, player_health)
        
        user_input = input("> ").lower().strip()

        # --- Game Logic ---
        if user_input == 'quit':
            game_status = 'quit' 
            print("Til' next time, Hero. Thanks for playing!")

        # Check if user input starts with 'go ' to move to a new room.
        elif user_input.startswith('go '): 
            current_room = movement.get_new_room(user_input, current_room)

        # Check if user input starts with 'get ' to pick up an item.
        elif user_input.startswith('get '):
            pick_up_item(user_input, current_room, inventory) 


        # Display available commands when called by the user.
        elif user_input in ['command', 'commands', 'help']:
            print("Available Commands: 'go [direction]', 'get [item]', 'quit'") 

        # If none of the above, notify user of invalid command.
        else:   
            print("Invalid Command.") 

    # Main game loop ends here.
if __name__ == '__main__':

    #Entry point of the program.
    main()
