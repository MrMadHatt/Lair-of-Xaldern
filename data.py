    # Define the rooms and their connections along with items and objects.
ROOMS = {
    'elaborate entrance hall': {    #Define the Elaborate Entrance Hall room.
        'north': 'library',    #Define the north exit to the library.
        'east': 'kitchen',  #Define the east exit to the kitchen.
        'south': 'royal courtyard',   #Define the south exit to the royal courtyard.
        'west': 'dungeon', #Define the west exit to the dungeon.
    },
    'library': {    #Define the Library room.
        'south': 'elaborate entrance hall',   #Define the south exit to the Elaborate Entrance Hall.
        'item': 'potion of strength',   #Define the item in the Library room.
    },
    'kitchen': {    #Define the Kitchen room.
        'west': 'elaborate entrance hall',  #Define the west exit to the Elaborate Entrance Hall.
        'item': 'vial of xaldern',  #Define the item in the Kitchen room.
    },
    'royal courtyard': {    #Define the Royal Courtyard room.
        'north': 'elaborate entrance hall',  #Define the north exit to the Elaborate Entrance Hall.
        'object': 'three-headed dragon', #Define the object in the Royal Courtyard room.
    },
    'dungeon': {    #Define the Dungeon room.
        'east': 'elaborate entrance hall', #Define the east exit to the Elaborate Entrance Hall.
        'south': 'secret chamber',    #Define the east exit to the Secret Chamber.
    },
    'secret chamber': {    #Define the Secret Chamber room.
        'west': 'dungeon', #Define the west exit to the Dungeon.
        'item': 'sword of gilathis',  #Define the item in the Secret Chamber room.
    },
}