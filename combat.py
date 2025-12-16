from data import ROOMS
from interface import show_status, show_instructions 
from item_management import pick_up_item

def check_combat(current_room, inventory):
    # Placeholder for combat logic
    
    if 'Three-Headed Dragon' in ROOMS['royal courtyard'].get('monsters', []):
        print("\nA Three-Headed Dragon appears! Prepare for battle!")