## Lair of Xaldern
# This project is still in development

**A Data-Driven Text-Adventure Engine**

*Lair of Xaldern* is a technical portfolio project developed to demonstrate proficiency in modular software design, relational data management, and automated ETL (Extract, Transform, Load) pipelines. Originally created as a foundational project ahead of Computer Science coursework at **Pikes Peak State College**, this engine focuses on decoupling narrative content from execution logic.

---
## 📁 Project Architecture

The engine follows a modular architecture to adhere to the **Single Responsibility Principle**:

* **`engine/`**: The core execution layer, containing decoupled modules for movement validation, inventory state, and the user interface.
* **`tools/`**: Contains the **Data-Sync Pipeline**, a custom utility that parses Obsidian Markdown files (YAML frontmatter) and synchronizes them with the production database.
* **`design/`**: The "Source of Truth" for game content. By utilizing Markdown, the world-building process is kept distinct from the codebase.
* **`data/`**: The persistence layer, housing the SQLite database. (Note: `.db` files are git-ignored to maintain local state integrity).

## 🛠 Prerequisites

This game requires **Python 3.10+** and **SQLite3** to manage world data and item persistence.

### 1. Python 3.10+
The engine utilizes features found in modern Python versions. 
* **Windows:** Download from [python.org](https://www.python.org/). **Check "Add Python to PATH" during installation.**
* **macOS:** Use Homebrew (`brew install python@3.10`) or the official installer.
* **Linux:** `sudo apt update && sudo apt install python3.10`

### 2. SQLite3
SQLite acts as the game's database. To check if you have it, run `sqlite3 --version` in your terminal.
* **Windows:** Usually bundled with Python. If not, download binaries from [sqlite.org](https://www.sqlite.org/).
* **macOS/Linux:** Almost always pre-installed. If missing on Linux, use `sudo apt install sqlite3`.

---

## 🚀 Installation & Setup

### macOS Environment Setup (Required)
To avoid "Externally Managed Environment" errors when installing dependencies on Mac, you **must** use a virtual environment:

1. **Create venv:** `python3 -m venv .venv`
2. **Activate venv:** `source .venv/bin/activate`
3. **Install PyYAML:** `pip install pyyaml`

*Note: Windows users can simply run `pip install pyyaml`, though a venv is still recommended.*

---

## 🕹️ How to Play

1. **Sync Data:** Every time you change a Markdown file in the `design/` folder, you must sync the database:
   ```
   python3 tools/data_sync.py
   ```
2. **Start Game: Launch the engine:**
    ```
    python3 engine/main.py
    ```

---

## 🛠️ Engineering Highlights & Technical Principles

### **Relational Data Persistence**
The engine utilizes a **relational SQLite database**. This allows for complex queries, such as Join Tables for room-item relationships, ensuring that game state changes (like picking up an item) are persistent and memory-efficient.

### **Automated Data Pipeline**
Implemented a custom parser in `data_sync.py` that automates the transition from narrative design to structured data. This pipeline handles:
* **Sanitization**: Cleaning YAML frontmatter for database entry.
* **Mapping**: Converting Markdown internal links to relational Foreign Keys.
* **Filtering**: Excluding draft content to ensure a stable production environment.

### **Input Sanitization & UI**
The engine features a robust text-parser that handles case-sensitivity, whitespace, and "fuzzy" matching. The HUD is dynamically rendered to provide real-time feedback on player vitals and spatial positioning.

---

## 📈 Development Roadmap
- [x] **Relational Migration**: Transitioned from flat-file JSON to SQLite.
- [x] **Design-to-Data Pipeline**: Created Obsidian-to-SQL synchronization tools.
- [x] **Inventory Persistence**: Implementing the "Get" logic to update relational tables.
- [ ] **Object-Oriented Refactor**: Transitioning room and player entities into Class structures.

**Author:** [Dominiq Barbero | [github.com/mrmadhatt](https://github.com/mrmadhatt)]