    # Define the rooms and their connections along with items and objects.
ROOMS = {
    'Elaborate Entrance Hall': {    #Define the Elaborate Entrance Hall room.
        'South': 'Library',    #Define the north exit to the library.
        'East': 'Kitchen',  #Define the east exit to the kitchen.
        'South': 'Royal Courtyard',   #Define the south exit to the royal courtyard.
        'West': 'Dungeon', #Define the west exit to the dungeon.
    },
    'Library': {    #Define the Library room.
        'South': 'Elaborate Entrance Hall',   #Define the south exit to the Elaborate Entrance Hall.
        'item': 'Potion of Strength',   #Define the item in the Library room.
    },
    'Kitchen': {    #Define the Kitchen room.
        'West': 'Elaborate Entrance Hall',  #Define the west exit to the Elaborate Entrance Hall.
        'item': 'Vial of Xaldern',  #Define the item in the Kitchen room.
    },
    'Royal Courtyard': {    #Define the Royal Courtyard room.
        'North': 'Elaborate Entrance Hall',  #Define the north exit to the Elaborate Entrance Hall.
        'object': 'Three-Headed Dragon', #Define the object in the Royal Courtyard room.
    },
    'Dungeon': {    #Define the Dungeon room.
        'East': 'Elaborate Entrance Hall', #Define the east exit to the Elaborate Entrance Hall.
        'Secret Chamber': 'Secret Chamber',    #Define the east exit to the Secret Chamber.
    },
    'Secret Chamber': {    #Define the Secret Chamber room.
        'West': 'Dungeon', #Define the west exit to the Dungeon.
        'item': 'Sword of Gilathis',  #Define the item in the Secret Chamber room.
    },
}