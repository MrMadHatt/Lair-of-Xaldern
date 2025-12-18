    # Define the rooms and their connections along with items and objects.
ROOMS = {
    # Room definitions
    'elaborate entrance hall': {    
        'north': 'library',    
        'east': 'kitchen',  
        'south': 'royal courtyard',   
        'west': 'dungeon', 
    },
    # Additional rooms
    'library': {    
        'south': 'elaborate entrance hall',   
        'item': 'potion of strength',   
    },
    # Define the kitchen room.
    'kitchen': {
        'west': 'elaborate entrance hall',  
        'item': 'vial of xaldern', 
    },
    # Define the Royal Courtyard room/object.
    'royal courtyard': {    
        'north': 'elaborate entrance hall',  
        'object': 'three-headed dragon', 
    },
    # Define the Dungeon room and its connections.
    'dungeon': {    
        'east': 'elaborate entrance hall', 
        'south': 'secret chamber',
    },
    # Define the Secret Chamber room and sword item.
    'secret chamber': {    
        'south': 'dungeon', 
        'item': 'sword of gilathis',  
    },
}
