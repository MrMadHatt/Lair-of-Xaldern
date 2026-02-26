import os
import sys
import sqlite3
import yaml
import re

# --- PATH CONFIGURATION ---
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from lair_of_xaldern.load_logic import DB_PATH as DB_NAME

DATA_FOLDER = os.path.join(PROJECT_ROOT, "design", "content")


def clean_id(val):
    if val is None:
        return None
    # Strips brackets, quotes, and everything after an underscore
    s = str(val).replace("[", "").replace("]", "").replace('"', "").replace("'", "")
    s = s.split("_")[0]
    try:
        return int(s.strip())
    except ValueError:
        return None


def setup_database():
    db_dir = os.path.dirname(DB_NAME)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Main Items table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS items
                     (id INTEGER PRIMARY KEY, name TEXT, status TEXT)"""
    )

    # 2. Rooms table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS rooms
                     (id INTEGER PRIMARY KEY, name TEXT, north INTEGER, south INTEGER,
                      east INTEGER, west INTEGER, is_locked INTEGER DEFAULT 0,
                      status TEXT)"""
    )

    # 3. Room-Item Join Table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS room_items
                     (room_id INTEGER, item_id INTEGER,
                      FOREIGN KEY(room_id) REFERENCES rooms(id),
                      FOREIGN KEY(item_id) REFERENCES items(id))"""
    )

    # 4. Specialized Weapons table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS weapons (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT,
                    damage INTEGER DEFAULT 0,
                    weight REAL DEFAULT 0.0,
                    price INTEGER DEFAULT 0,
                    health_modifier INTEGER DEFAULT 0,
                    status TEXT,
                    FOREIGN KEY (item_id) REFERENCES items(id)
                )"""
    )

    # 5. Master Enemy table (Templates)
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS enemies (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    health INTEGER,
                    max_health INTEGER,
                    attack INTEGER,
                    defense INTEGER,
                    description TEXT,
                    status TEXT
                )"""
    )

    # 6. Enemy Loot Bridge table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS enemy_loot (
                    enemy_id INTEGER,
                    item_id INTEGER,
                    drop_chance REAL,
                    FOREIGN KEY (enemy_id) REFERENCES enemies(id),
                    FOREIGN KEY (item_id) REFERENCES items(id)
                )"""
    )

    # 7. Room Enemies (Instances)
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS room_enemies (
                    room_id INTEGER,
                    enemy_id INTEGER,
                    current_hp INTEGER,
                    is_alive INTEGER DEFAULT 1,
                    FOREIGN KEY(room_id) REFERENCES rooms(id),
                    FOREIGN KEY(enemy_id) REFERENCES enemies(id)
                )"""
    )

    # 8. Player Stats
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS player_stats (
                    id INTEGER PRIMARY KEY,
                    hp INTEGER,
                    max_hp INTEGER,
                    attack INTEGER,
                    defense INTEGER,
                    current_room INTEGER,
                    FOREIGN KEY(current_room) REFERENCES rooms(id)
                )"""
    )

    # 9. Player Inventory
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER,
                    quantity INTEGER DEFAULT 1,
                    is_equipped INTEGER DEFAULT 0,
                    FOREIGN KEY(item_id) REFERENCES items(id)
                )"""
    )

    conn.commit()
    conn.close()


def sync_data():
    setup_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")
    print(f"--- Starting Sync from {DATA_FOLDER} ---")

    # 0. CLEANUP PHASE
    print("🧹 Cleaning old data...")
    tables = [
        "room_items",
        "enemy_loot",
        "room_enemies",
        "weapons",
        "enemies",
        "rooms",
        "items",
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='inventory'")

    # 1. FILE DISCOVERY & PARSING
    files = []
    for root, _dirs, filenames in os.walk(DATA_FOLDER):
        if "draft" in root.lower():
            continue
        for f in filenames:
            if f.lower().endswith(".md") and "template" not in f.lower():
                files.append(os.path.join(root, f))

    parsed_data = []
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            # .strip() handles leading blank lines before the first ---
            full_text = f.read().strip()
            # Robust regex handles spaces after dashes
            match = re.search(
                r"^---\s*\n(.*?)\n---\s*(.*)", full_text, re.DOTALL | re.MULTILINE
            )

            if not match:
                print(f"❌ REGEX FAILED: {filename} - Check YAML delimiters (---)")
                continue

            try:
                metadata = yaml.safe_load(match.group(1))
                body = match.group(2).strip()
                if isinstance(metadata, dict):
                    parsed_data.append((metadata, body, filename))
            except Exception as e:
                print(f"❌ YAML ERROR in {filename}: {e}")

    print(
        f"📊 Files Discovered: {len(files)} | Successfully Parsed: {len(parsed_data)}"
    )

    # 2. PASS 1: GLOBAL ENTITIES (Items, Weapons, Enemies)
    for metadata, body, filename in parsed_data:
        etype = str(metadata.get("type", "")).lower().strip()
        status = str(metadata.get("status", "unfinished")).lower().strip()
        raw_id = (
            metadata.get("id")
            or metadata.get("item_id")
            or metadata.get("enemy_id")
            or metadata.get("weapon_id")
        )

        if not raw_id or status != "finished":
            continue

        entry_id = clean_id(raw_id)

        if etype in ["item", "weapon", "consumable"]:
            name = str(metadata.get("name", "Unknown")).strip("\"'")
            cursor.execute(
                "INSERT OR REPLACE INTO items VALUES (?,?,?)", (entry_id, name, status)
            )
            if etype == "weapon":
                cursor.execute(
                    "INSERT OR REPLACE INTO weapons VALUES (?,?,?,?,?,?,?)",
                    (
                        entry_id,
                        name,
                        metadata.get("damage", 0),
                        metadata.get("weight", 0.0),
                        metadata.get("price", 0),
                        metadata.get("health_modifier", 0),
                        status,
                    ),
                )
            print(f"📦 {etype.capitalize()} {entry_id} synced.")

        elif etype == "enemy":
            name = metadata.get("name", "Unknown Enemy")
            hp = metadata.get("hp", 10)
            cursor.execute(
                "INSERT OR REPLACE INTO enemies VALUES (?,?,?,?,?,?,?,?)",
                (
                    entry_id,
                    name,
                    hp,
                    hp,
                    metadata.get("attack", 2),
                    metadata.get("defense", 0),
                    body,
                    status,
                ),
            )

            loot_list = metadata.get("loot", [])
            if isinstance(loot_list, list):
                for loot in loot_list:
                    l_id = clean_id(loot.get("id"))
                    if l_id:
                        cursor.execute(
                            "INSERT INTO enemy_loot VALUES (?,?,?)",
                            (entry_id, l_id, loot.get("chance", 1.0)),
                        )
            print(f"👹 Enemy Template {entry_id} synced.")

    # 3. PASS 2: RELATIONSHIPS (Rooms, Room Items, Room Enemies)
    print("\n--- Starting Pass 2 (Rooms) ---")
    for metadata, body, filename in parsed_data:
        etype = str(metadata.get("type", "")).lower().strip()
        status = str(metadata.get("status", "unfinished")).lower().strip()
        raw_id = metadata.get("id") or metadata.get("location_id")

        # Verbose Debug for potential rooms
        if "room" in filename.lower() or etype in ["room", "location"]:
            if status != "finished":
                print(
                    f"⚠️  SKIPPING {filename}: Status is '{status}' (Expected 'finished')"
                )
            if not raw_id:
                print(f"❓ ERROR {filename}: No ID found in YAML metadata.")

        if etype not in ["room", "location"] or status != "finished":
            continue

        entry_id = clean_id(raw_id)
        room_name = str(metadata.get("name", filename)).strip("\"'")
        n, s, e, w = [
            clean_id(metadata.get(d)) for d in ["north", "south", "east", "west"]
        ]

        cursor.execute(
            "INSERT OR REPLACE INTO rooms VALUES (?,?,?,?,?,?,?,?)",
            (entry_id, room_name, n, s, e, w, metadata.get("is_locked", 0), status),
        )

        # Room Items
        for item_raw in metadata.get("items") or metadata.get("contains_items") or []:
            i_id = clean_id(item_raw)
            if i_id:
                cursor.execute("INSERT INTO room_items VALUES (?, ?)", (entry_id, i_id))

        # Room Enemies
        for enemy_raw in (
            metadata.get("enemies") or metadata.get("contains_enemies") or []
        ):
            e_id = clean_id(enemy_raw)
            if e_id:
                cursor.execute("SELECT health FROM enemies WHERE id = ?", (e_id,))
                res = cursor.fetchone()
                hp = res[0] if res else 10
                cursor.execute(
                    "INSERT INTO room_enemies VALUES (?, ?, ?, 1)", (entry_id, e_id, hp)
                )

        print(f"📍 Room {entry_id} synced.")

    conn.commit()
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.close()
    print("--- Sync Complete! ---")


if __name__ == "__main__":
    sync_data()
