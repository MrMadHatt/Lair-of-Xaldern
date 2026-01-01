import os
import sqlite3
import yaml
import re

# --- PATH CONFIGURATION ---
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(TOOLS_DIR)
DATA_FOLDER = os.path.join(BASE_DIR, 'design', 'content') 
DB_NAME = os.path.join(BASE_DIR, 'data', 'game_data.db')

def clean_id(val):
    if val is None: return None
    # Strips brackets, quotes, and everything after an underscore
    s = str(val).replace('[', '').replace(']', '').replace('"', '').replace("'", "")
    s = s.split('_')[0] 
    try:
        return int(s.strip())
    except ValueError:
        return None

def setup_database():
    if not os.path.exists(os.path.dirname(DB_NAME)):
        os.makedirs(os.path.dirname(DB_NAME))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Main Items table - Now only contains universal info
    cursor.execute('''CREATE TABLE IF NOT EXISTS items 
                     (id INTEGER PRIMARY KEY, name TEXT, status TEXT)''')
    
    # 2. Rooms table
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms 
                     (id INTEGER PRIMARY KEY, name TEXT, north INTEGER, south INTEGER, 
                      east INTEGER, west INTEGER, is_locked INTEGER DEFAULT 0,
                      status TEXT)''')
    
    # 3. Room-Item Join Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS room_items 
                     (room_id INTEGER, item_id INTEGER,
                      FOREIGN KEY(room_id) REFERENCES rooms(id),
                      FOREIGN KEY(item_id) REFERENCES items(id))''')
    
    # 4. Specialized Weapons table (Option 2)
    cursor.execute('''CREATE TABLE IF NOT EXISTS weapons (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT,
                    damage INTEGER DEFAULT 0,
                    weight REAL DEFAULT 0.0,
                    price INTEGER DEFAULT 0,
                    health_modifier INTEGER DEFAULT 0,
                    status TEXT,
                    FOREIGN KEY (item_id) REFERENCES items(id)
                )''')
    # The master enemy table
    cursor.execute('''CREATE TABLE IF NOT EXISTS enemies (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    health INTEGER,
                    max_health INTEGER,
                    attack INTEGER,
                    defense INTEGER,
                    description TEXT,
                    status TEXT
                )''')

# The "Bridge" table for loot
    cursor.execute('''CREATE TABLE IF NOT EXISTS enemy_loot (
                    enemy_id INTEGER,
                    item_id INTEGER,
                    drop_chance REAL,
                    FOREIGN KEY (enemy_id) REFERENCES enemies(id),
                    FOREIGN KEY (item_id) REFERENCES items(id)
                )''')
    
    conn.commit()
    conn.close()

def sync_data():
    setup_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")
    
    print(f"--- Starting Sync from {DATA_FOLDER} ---")
    
    # 1. FILE DISCOVERY PHASE
    files = []
    for root, dirs, filenames in os.walk(DATA_FOLDER):
        lowercase_root = root.lower()
        # --- SAFETY GUARD ---
        # If '02-world-draft' is in the current path, skip it entirely
        if '02-world-draft' in lowercase_root or 'draft' in lowercase_root:
            continue
            
        for f in filenames:
            if f.lower().endswith('.md') and 'template' not in f.lower():
                files.append(os.path.join(root, f))

    # 2. PROCESSING PHASE
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^\s*---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            
            if not match:
                print(f"⚠️  {filename}: Frontmatter format error.")
                continue

            try:
                doc = yaml.safe_load(match.group(1))
                if not isinstance(doc, dict): continue

                raw_id = doc.get('id') or doc.get('item_id') or doc.get('location_id') or doc.get('weapon_id')
                status = str(doc.get('status', 'unfinished')).lower().strip()

                if raw_id is None:
                    print(f"❓ {filename}: Missing 'id' field.")
                    continue
                
                if status != 'finished':
                    continue

                entry_id = clean_id(raw_id)
                etype = str(doc.get('type', 'room')).lower()

                # --- DATABASE INSERTION LOGIC ---
                if etype in ['room', 'location']:
                    room_name = str(doc.get('name', filename)).strip('"').strip("'")
                    n, s, e, w = [clean_id(doc.get(d)) for d in ['north', 'south', 'east', 'west']]
                    
                    cursor.execute('''INSERT OR REPLACE INTO rooms (id, name, north, south, east, west, is_locked, status) 
                                    VALUES (?,?,?,?,?,?,?,?)''',
                                 (entry_id, room_name, n, s, e, w, doc.get('is_locked', 0), status))
                    
                    cursor.execute("DELETE FROM room_items WHERE room_id = ?", (entry_id,))
                    item_list = doc.get('items') or doc.get('contains_items')
                    if item_list and isinstance(item_list, list):
                        for item_raw in item_list:
                            i_id = clean_id(item_raw)
                            if i_id: cursor.execute("INSERT INTO room_items (room_id, item_id) VALUES (?, ?)", (entry_id, i_id))
                    print(f"📍 Room {entry_id} ({room_name}) synced.")

                elif etype in ['item', 'weapon', 'consumable']:
                    name = str(doc.get('name', 'Unknown')).strip('"').strip("'")
                    cursor.execute('INSERT OR REPLACE INTO items (id, name, status) VALUES (?,?,?)', (entry_id, name, status))
                    
                    if etype == 'weapon':

                        damage = doc.get('damage', 0)
                        weight = doc.get('weight', 0)
                        price = doc.get('price', 0)
                        health_mod = doc.get('health_modifier', 0)
                        weapon_values = (entry_id, name, damage, weight, price, health_mod, status)
                        cursor.execute('''INSERT OR REPLACE INTO weapons (item_id, name, damage, weight, price, health_modifier, status) 
                                        VALUES (?,?,?,?,?,?,?)''', weapon_values)
                                        
                        print(f"⚔️ Weapon {entry_id} ({name}) synced.")
                    else:
                        print(f"📦 Item {entry_id} ({name}) synced.")

            except Exception as e:
                print(f"❌ Error in {filename}: {e}")

    conn.commit()
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.close()
    print("--- Sync Complete! ---")

if __name__ == "__main__":
    sync_data()