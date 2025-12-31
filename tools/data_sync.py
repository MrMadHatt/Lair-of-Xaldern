import os
import sqlite3
import yaml
import re

# --- PATH CONFIGURATION ---
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(TOOLS_DIR)
DATA_FOLDER = os.path.join(BASE_DIR, 'design') 
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS items 
                     (id INTEGER PRIMARY KEY, name TEXT, damage INTEGER DEFAULT 0, 
                      weight REAL DEFAULT 0.0, price INTEGER DEFAULT 0,
                      health_modifier INTEGER DEFAULT 0, status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms 
                     (id INTEGER PRIMARY KEY, name TEXT, north INTEGER, south INTEGER, 
                      east INTEGER, west INTEGER, is_locked INTEGER DEFAULT 0,
                      status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS room_items 
                     (room_id INTEGER, item_id INTEGER,
                      FOREIGN KEY(room_id) REFERENCES rooms(id),
                      FOREIGN KEY(item_id) REFERENCES items(id))''')
    conn.commit()
    conn.close()

def sync_data():
    setup_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"--- Starting Sync from {DATA_FOLDER} ---")
    
    IGNORE_LIST = ['room templates.md', 'roomtemplates.md']
    
    files = []
    for root, dirs, filenames in os.walk(DATA_FOLDER):
        for f in filenames:
            if f.lower().endswith('.md') and f.lower() not in IGNORE_LIST:
                files.append(os.path.join(root, f))

    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # MODIFIED REGEX: More flexible with whitespace and line endings
            match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            
            if not match:
                # If you see this, your "---" markers might have spaces after them!
                print(f"⚠️  Skipping {filename}: No valid YAML frontmatter found.")
                continue

            try:
                doc = yaml.safe_load(match.group(1))
                if not isinstance(doc, dict): continue

                raw_id = doc.get('id') or doc.get('item_id') or doc.get('location_id') or doc.get('weapon_id')
                status = str(doc.get('status', 'unfinished')).lower().strip()

                if raw_id is None:
                    print(f"❓ Skipping {filename}: No ID field found.")
                    continue
                
                if status != 'finished':
                    # This tells you exactly which files are being ignored by the 'finished' filter
                    print(f"🚧 Skipping {filename}: Status is '{status}'.")
                    continue

                entry_id = clean_id(raw_id)
                etype = str(doc.get('type', 'room')).lower()

                if etype in ['room', 'location']:
                    room_name = str(doc.get('name', filename)).strip('"').strip("'")
                    n = clean_id(doc.get('north'))
                    s = clean_id(doc.get('south'))
                    e = clean_id(doc.get('east'))
                    w = clean_id(doc.get('west'))

                    cursor.execute('''INSERT OR REPLACE INTO rooms (id, name, north, south, east, west, is_locked, status) 
                                    VALUES (?,?,?,?,?,?,?,?)''',
                                 (entry_id, room_name, n, s, e, w, doc.get('is_locked', 0), status))
                    print(f"📍 Room {entry_id} ({room_name}) synced.")

                elif etype in ['item', 'weapon', 'consumable']:
                    name = str(doc.get('name', 'Unknown')).strip('"').strip("'")
                    cursor.execute('''INSERT OR REPLACE INTO items (id, name, damage, weight, price, health_modifier, status) 
                                    VALUES (?,?,?,?,?,?,?)''',
                                    (entry_id, name, doc.get('damage', 0), doc.get('weight', 0), 
                                     doc.get('price', 0), doc.get('health_modifier', 0), status))
                    print(f"⚔️ Item {entry_id} ({name}) synced.")

            except Exception as e:
                print(f"❌ Error in {filename}: {e}")

    conn.commit()
    conn.close()
    print("--- Sync Complete! ---")

if __name__ == "__main__":
    sync_data()