import lair_of_xaldern.interface as interface


def get_room_items(cursor, room_id):
    """Returns a list of item names for a specific room."""
    query = """
        SELECT i.name
        FROM items i
        JOIN room_items ri ON i.id = ri.item_id
        WHERE ri.room_id = ?
    """
    cursor.execute(query, (room_id,))
    return [row[0] for row in cursor.fetchall()]


def pick_up_item(conn, user_input, room_id, inventory_list):
    """Handles picking up an item with case-insensitive matching."""
    item_name_input = user_input.replace("get ", "").strip().lower()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT items.id, items.name FROM items
        JOIN room_items ON items.id = room_items.item_id
        WHERE room_items.room_id = ? AND LOWER(items.name) = ?
    """,
        (room_id, item_name_input),
    )

    item = cursor.fetchone()

    if item:
        item_id = item["id"]
        actual_name = item["name"]

        cursor.execute(
            "DELETE FROM room_items WHERE room_id = ? AND item_id = ?",
            (room_id, item_id),
        )
        conn.commit()

        inventory_list.append(actual_name)

        print(f"You picked up the {actual_name}.")
        return actual_name

    print("That item isn't here.")
    return None


def drop_item(conn, user_input, room_id, current_inventory):
    """Processes 'drop [item]' command with case-insensitive matching."""
    if not user_input.startswith("drop "):
        return None

    item_to_drop = user_input.lower().replace("drop ", "").strip()

    match = next((i for i in current_inventory if i.lower() == item_to_drop), None)

    if match:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM items WHERE LOWER(name) = ?", (match.lower(),))
        result = cursor.fetchone()

        if result:
            item_id = result[0]

            cursor.execute(
                "INSERT INTO room_items (room_id, item_id) VALUES (?, ?)",
                (room_id, item_id),
            )
            conn.commit()

            current_inventory.remove(match)

            clean_name = interface.format_item_name(match)
            print(f"\n** You dropped the {clean_name}. **")
            return match

    print(f"\nYou aren't carrying a '{item_to_drop}'!")
    return None
