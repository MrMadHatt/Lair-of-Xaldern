    # Define the rooms and their connections along with items and objects.
ROOMS = {
    'Elaborate Entrance Hall': {    #Define the Elaborate Entrance Hall room.
        'north': 'Library',    #Define the north exit to the library.
        'east': 'kitchen',  #Define the east exit to the kitchen.
        'south': 'Royal Courtyard',   #Define the south exit to the royal courtyard.
        'west': 'Dungeon', #Define the west exit to the dungeon.
    },
    'Library': {    #Define the Library room.
        'south': 'Elaborate Entrance Hall',   #Define the south exit to the Elaborate Entrance Hall.
        'item': 'Potion of Strength',   #Define the item in the Library room.
    },
    'Kitchen': {    #Define the Kitchen room.
        'west': 'Elaborate Entrance Hall',  #Define the west exit to the Elaborate Entrance Hall.
        'item': 'Vial of Xaldern',  #Define the item in the Kitchen room.
    },
    'Royal Courtyard': {    #Define the Royal Courtyard room.
        'north': 'Elaborate Entrance Hall',  #Define the north exit to the Elaborate Entrance Hall.
        'object': 'Three-Headed Dragon', #Define the object in the Royal Courtyard room.
    },
    'Dungeon': {    #Define the Dungeon room.
        'east': 'Elaborate Entrance Hall', #Define the east exit to the Elaborate Entrance Hall.
        'Secret_Chamber': 'Secret Chamber',    #Define the east exit to the Secret Chamber.
    },
    'Secret Chamber': {    #Define the Secret Chamber room.
        'west': 'Dungeon', #Define the west exit to the Dungeon.
        'item': 'Sword of Gilathis',  #Define the item in the Secret Chamber room.
    },
}