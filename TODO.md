# Lair of Xaldern - Development Roadmap

## Completed ✅
- [x] Separate engine logic from world data (Moved `data.py` to JSON vault)
- [x] Establish GitHub Community Standards (README, CoC, Contributing, Security)
- [x] Configure .github templates (Issues & Pull Requests)

## Core Engine & Refactoring ⚙️
- [ ] Move format functions from `interface.py` to `format.py`
- [ ] Implement the save/load functionality (Import database module)
- [ ] Allow player to view stats and quest log

## Combat & Survival ⚔️
- [ ] Add player stats and leveling system
- [ ] Implement combat trigger and scenario handling
- [ ] Import combat module and integrate checks in the game loop
- [ ] Implement damage calculation and enemy health tracking
- [ ] Add health management system and death conditions
- [ ] Add enemy encounters in specific rooms

## World & Inventory 🗺️
- [ ] Add more rooms with enemies
- [ ] Allow ability to drop items (sync with room data structure)
- [ ] Add ability to use items in and out of combat
- [ ] Implement puzzle mechanics in randomized rooms

## Narrative & Content 📜
- [ ] Begin narrative elements for story progression
- [ ] Add NPC interactions and dialogues
- [ ] Add player choices and branching storylines (Choices affecting outcomes)
- [ ] Include side/optional quests (1-3)

## Visuals & Sound (Late Stage) 🎨
- [ ] Add GUI elements for visual engagement
- [ ] Import character module for visual representation
- [ ] Add sound effects and background music (GUI dependent)