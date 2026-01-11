import sqlite3
import random


def get_enemy_in_room(room_id, cursor):

    cursor.execute(
        """
        SELECT e.id, e.name, re.current_hp, e.attack, e.description 
        FROM room_enemies re
        JOIN enemies e ON re.enemy_id = e.id
        WHERE re.room_id = ? AND re.is_alive = 1
    """,
        (room_id,),
    )
    return cursor.fetchone()


def get_player_attack_power(cursor):
    cursor.execute(
        """
        SELECT MAX(w.damage) 
        FROM inventory inv
        JOIN weapons w ON inv.item_id = w.item_id
        WHERE inv.is_equipped = 1
    """
    )
    result = cursor.fetchone()
    return result[0] if result and result[0] is not None else 1


def attack_enemy(room_id, cursor, conn, player_stats):

    enemy = get_enemy_in_room(room_id, cursor)

    if not enemy:
        print("You swing your weapon, but the room is empty.")
        return

    e_id, e_name, current_hp, e_atk, e_desc = enemy
    player_dmg = get_player_attack_power(cursor)

    new_hp = current_hp - player_dmg
    print(f"\n⚔️ You strike the {e_name} for {player_dmg} damage!")

    if new_hp <= 0:
        print(f"💥 {e_name} has been defeated!")
        cursor.execute(
            """
            UPDATE room_enemies SET is_alive = 0, current_hp = 0
            WHERE room_id = ? AND enemy_id = ?
        """,
            (room_id, e_id),
        )
    else:
        cursor.execute(
            """
            UPDATE room_enemies SET current_hp = ? 
            WHERE room_id = ? AND enemy_id = ?
        """,
            (new_hp, room_id, e_id),
        )
        print(f"The {e_name} staggered! (HP: {new_hp})")

    conn.commit()


def take_enemy_turn(enemy, player_stats):

    e_id, e_name, current_hp, e_atk, e_desc = enemy

    damage_to_player = max(1, e_atk - player_stats.get("defense", 0))
    player_stats["hp"] -= damage_to_player

    print(f"👹 {e_name} lunges at you, dealing {damage_to_player} damage!")

    if player_stats["hp"] <= 0:
        print("\n💀 You have succumbed to your wounds. Game Over.")
        return "death"
    return "alive"


def start_combat_loop(room_id, cursor, conn, player_stats):

    print("\n--- COMBAT ENGAGED ---")

    while True:
        enemy = get_enemy_in_room(room_id, cursor)
        if not enemy:
            break

        attack_enemy(room_id, cursor, conn, player_stats)

        enemy_after_hit = get_enemy_in_room(room_id, cursor)
        if not enemy_after_hit:
            print("The area is now quiet.")
            break

        status = take_enemy_turn(enemy_after_hit, player_stats)
        if status == "death":
            return "game_over"

        print(f"Player HP: {player_stats['hp']}")
        input("Press Enter for the next round...")

    return "victory"
