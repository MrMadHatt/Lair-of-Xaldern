"""
import random

def get_enemy_in_room(room_id, cursor):
    ""Helper to find the active enemy in the current room.""
    cursor.execute('''
        SELECT e.id, e.name, e.health, e.attack, e.description 
        FROM enemies e
        JOIN room_enemies re ON e.id = re.enemy_id
        WHERE re.room_id = ? AND re.is_alive = 1
    ''', (room_id,))
    return cursor.fetchone()

def get_player_attack_power(cursor):
    ""Calculates max damage based on inventory weapons.""
    cursor.execute('''
        SELECT MAX(w.damage) 
        FROM inventory inv
        JOIN weapons w ON inv.item_id = w.item_id
    ''')
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 1

def attack_enemy(room_id, cursor, conn):
    ""Executes one round of player attacking an enemy.""
    enemy = get_enemy_in_room(room_id, cursor)
    
    if not enemy:
        print("You swing at the air... there's nothing here to fight.")
        return

    e_id, e_name, e_hp, e_atk, e_desc = enemy
    player_dmg = get_player_attack_power(cursor)
    
    new_hp = e_hp - player_dmg
    print(f"You hit the {e_name} for {player_dmg} damage!")

    if new_hp <= 0:
        print(f"💥 The {e_name} collapses! You have defeated it.")
        cursor.execute('''
            UPDATE room_enemies SET is_alive = 0 
            WHERE room_id = ? AND enemy_id = ?
        ''', (room_id, e_id))
        
        # This is where we will call the loot function
        resolve_loot(e_id, room_id, cursor, conn)
    else:
        cursor.execute('UPDATE enemies SET health = ? WHERE id = ?', (new_hp, e_id))
        print(f"The {e_name} has {new_hp} HP remaining.")
        
    conn.commit()
 
# Combat resolution logic would go here
"""