import os
import sqlite3
import yaml
import re

# --- PATH CONFIGURATION ---
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(TOOLS_DIR)
DATA_FOLDER = os.path.join(BASE_DIR, 'design') 
DB_NAME = os.path.join(BASE_DIR, 'data', 'game_data.db')

def setup_database():
    if not os.path.exists(os.path.dirname(DB_NAME)):
        os.makedirs(os.path.dirname(DB_NAME))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Clean Items Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS items 
                     (id INTEGER PRIMARY KEY, name TEXT, damage INTEGER DEFAULT 0, 
                      weight REAL DEFAULT 0.0, price INTEGER DEFAULT 0,
                      health_modifier INTEGER DEFAULT 0, status TEXT)''')
    
    # Clean Rooms Table (Added 'name' column so your interface can show 'Town 01')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms 
                     (id INTEGER PRIMARY KEY, name TEXT, north INTEGER, south INTEGER, 
                      east INTEGER, west INTEGER, is_locked INTEGER DEFAULT 0,
                      status TEXT)''')

    # The Join Table (Option 2)
    cursor.execute('''CREATE TABLE IF NOT EXISTS room_items 
                     (room_id INTEGER, 
                      item_id INTEGER,
                      FOREIGN KEY(room_id) REFERENCES rooms(id),
                      FOREIGN KEY(item_id) REFERENCES items(id))''')
    conn.commit()
    conn.close()

def sync_data():
    setup_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"--- Starting Sync from {DATA_FOLDER} ---")
    
    # 1. Define filenames to skip (case-insensitive)
    IGNORE_LIST = ['room templates.md', 'roomtemplates.md']
    
    # 2. Replaced the one-liner with a loop to allow filtering
    files = []
    for root, dirs, filenames in os.walk(DATA_FOLDER):
        for f in filenames:
            if f.lower().endswith('.md'):
                # Skip if the file is in our ignore list
                if f.lower() in [name.lower() for name in IGNORE_LIST]:
                    continue
                files.append(os.path.join(root, f))

    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            if not match: continue

            try:
                doc = yaml.safe_load(match.group(1))
                if not isinstance(doc, dict): continue

                raw_id = doc.get('id') or doc.get('item_id') or doc.get('location_id') or doc.get('weapon_id')
                status = str(doc.get('status', 'unfinished')).lower().strip().replace('"', '')
                
                if status != 'finished' or raw_id is None:
                    continue

                entry_id = int(str(raw_id).strip('"'))
                etype = str(doc.get('type')).lower()

                # --- ROOM / LOCATION SYNC ---
                if etype in ['room', 'location']:
                    room_name = doc.get('name', filename).strip('"')
                    cursor.execute('''INSERT OR REPLACE INTO rooms (id, name, north, south, east, west, is_locked, status) 
                                    VALUES (?,?,?,?,?,?,?,?)''',
                                 (entry_id, room_name, doc.get('north'), doc.get('south'), 
                                  doc.get('east'), doc.get('west'), doc.get('is_locked', 0), status))
                    
                    room_items = doc.get('room_items', [])
                    if isinstance(room_items, list):
                        cursor.execute("DELETE FROM room_items WHERE room_id = ?", (entry_id,))
                        for item_id in room_items:
                            cursor.execute("INSERT INTO room_items (room_id, item_id) VALUES (?, ?)", 
                                         (entry_id, item_id))
                    
                    print(f"📍 Room {entry_id} ({room_name}) synced.")

                # --- ITEM / WEAPON SYNC ---
                elif etype in ['item', 'weapon', 'consumable']:
                    name = doc.get('name', 'Unknown').strip('"')
                    dmg = doc.get('damage') or doc.get('power') or 0
                    val = doc.get('value') or doc.get('price') or 0
                    
                    cursor.execute('''INSERT OR REPLACE INTO items 
                        (id, name, damage, weight, price, health_modifier, status) 
                        VALUES (?,?,?,?,?,?,?)''',
                        (entry_id, name, dmg, doc.get('weight', 0), val, doc.get('health_modifier', 0), status))
                    print(f"⚔️ Item {entry_id} ({name}) synced.")

            except Exception as e:
                print(f"❌ Error in {filename}: {e}")

    conn.commit()
    conn.close()
    print("--- Sync Complete! ---")

if __name__ == "__main__":
    sync_data()