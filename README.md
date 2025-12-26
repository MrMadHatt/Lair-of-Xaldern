### Lair of Xaldern

# A work in progress/learning project

**A Modular Text-Based RPG Engine | Developed with Python**

---

## Project Overview
*Lair of Xaldern* is an independent game project and a technical portfolio piece designed to demonstrate advanced logic implementation within a text-based environment. Developed as a foundational project ahead of Computer Science coursework at **Pikes Peak State College**, this engine focuses on modularity, state persistence, and robust user-input handling.

## Quick Start
### Prerequisites
- **Python 3.10+** is required to run the engine.

### Installation
1. **Clone the Repository:**
   git clone [https://github.com/YourUsername/Lair-of-Xaldern.git](https://github.com/YourUsername/Lair-of-Xaldern.git)

2. **Launch the game:**
    `python main.py`

## How To Play
The game uses a **Text-Parser Interface**. To interact with the world, type your command and press `Enter`.

### Movement
Explore the lair by typing `Go` followed by a cardinal direction.
* **Example:** `Go North` or `Go West`
* **Logic:** The engine validates if a path exists and updates your location automatically.

### Inventory & Items
Interact with objects found in various rooms.
* **Pick up items:** `Get [Item Name]` (e.g., `Get Key`)
* **View Status:** Your current location and inventory are displayed at the top of every turn.

### 🛠 System Commands
* **Exit:** Type `Quit` at any time to end your session.

---

## 🏗️ Technical Architecture
This project implements several key software engineering principles:

* **Modular Design:** Logic is decoupled into specific modules (`main.py`, `movement.py`, `interface.py`) to adhere to the **Separation of Concerns** principle.
* **State Management:** Utilizes a centralized data structure to track player inventory, global positioning, and world-state updates across the execution lifecycle.
* **Input Sanitization:** Custom parsing logic handles case-sensitivity and whitespace variations, ensuring a resilient user interface.
* **Navigation Algorithms:** Implements a dictionary-based coordinate system to map complex room interconnections and directional constraints.

---

## 🗺️ Roadmap & Future Development
- [ ] **Data Externalization:** Transition room data to `.json` files for easier content management.
- [ ] **Persistence Layer:** Implement Save/Load functionality using the `json` library.
- [ ] **OOP Refactor:** Transition combat and NPC logic into dedicated classes.
- [ ] **GUI Integration:** Develop a full Graphical User Interface to move beyond the CLI.

---

## 📜 License
Distributed under the **MIT License**.

---

**Author:** [Dominiq Barbero | github.com/mrmadhatt]

---


# Why I Built This

I’ve always been fascinated by how software handles complex, changing data. I chose a text-based RPG because it forced me to solve three specific engineering hurdles:

Navigational Logic: How to map a physical space using dictionaries and keys.

State Tracking: Ensuring the program "remembers" what is in the player's inventory across different functions.

Input Validation: Handling unpredictable user text to prevent the program from crashing.

# Current Features (The "Build" so far)

Dynamic Movement: A 5-room map where the user can move North, South, East, or West.

Inventory System: Logic to check for items, add them to a list, and update the game state.

Clean Interface: Clear text prompts to guide the user through the experience.

# Technical Challenges & Lessons Learned

The Global Variable Hurdle: Initially, I struggled with how functions access data. I learned how to pass variables correctly to maintain a "clean" global state.

Infinite Loops: I had to debug several instances where the game wouldn't exit properly, which taught me a lot about while loop conditions.

# Future Roadmap

[ ] Add a "Battle" class to practice Object-Oriented Programming (OOP).

[ ] Implement a Save/Load feature using JSON.


