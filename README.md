# Lair of Xaldern
**A Data-Driven Text-Adventure Engine**

*Lair of Xaldern* is a technical portfolio project developed to demonstrate proficiency in modular software design, relational data management, and automated ETL (Extract, Transform, Load) pipelines. Originally created as a foundational project ahead of Computer Science coursework at **Pikes Peak State College**, this engine focuses on decoupling narrative content from execution logic.

---
## 📁 Project Architecture

The engine follows a modular architecture to adhere to the **Single Responsibility Principle**:

* **`engine/`**: The core execution layer, containing decoupled modules for movement validation, inventory state, and the user interface.
* **`tools/`**: Contains the **Data-Sync Pipeline**, a custom utility that parses Obsidian Markdown files (YAML frontmatter) and synchronizes them with the production database.
* **`design/`**: The "Source of Truth" for game content. By utilizing Markdown, the world-building process is kept distinct from the codebase.
* **`data/`**: The persistence layer, housing the SQLite database. (Note: `.db` files are git-ignored to maintain local state integrity).

## 🚀 Installation & Usage

### Prerequisites
- **Python 3.10+**
- **SQLite3**
- **PyYAML** (`pip install pyyaml`)

### 1. Synchronize the World Data
This engine uses a "Sync-First" approach. To build the game world from the design files, run:
```bash
python tools/data_sync.py

python engine/Main.py

```markdown
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
- [ ] **Inventory Persistence**: Implementing the "Get" logic to update relational tables.
- [ ] **Object-Oriented Refactor**: Transitioning room and player entities into Class structures.

**Author:** [Dominiq Barbero | [github.com/mrmadhatt](https://github.com/mrmadhatt)]