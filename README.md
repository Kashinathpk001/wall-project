<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# CAN YOU LEAN ON? 🎯

> *"We all need some wall to lean on."*

## Basic Details
### Team Name: Solo Project

### Team Members
- Team Lead: Kashinath P K - [Your College Name]

### Project Description
A satirical, Apple-grade architectural telemetry platform that answers humanity's most pressing unanswered question: **"Can you lean on this wall without it collapsing or ruining your shirt with chalk powder?"** Features a proprietary 0–100 Trust Score algorithm, psychiatric wall profiling, red flag audits, and a 6-level visual scale ranging from pristine museum concrete to ancient weeping moss bogs.

### The Problem (that doesn't exist)
Millions of tired college students, waiting tea-drinkers, and weary homeowners lean against walls every single day with blind, reckless faith. They have no idea if that wall is secretly plotting structural mutiny, weeping emotional moisture, or coated in decades of chalk dust and peeling paint. The tragic result? Ruined black hoodies, chalk dust embarrassments, and profound architectural trust issues.

### The Solution (that nobody asked for)
**CAN YOU LEAN ON?** provides comprehensive fictional integrity forensics. Users input wall height, millimeter girth, visible existential cracks, and weeping moisture levels. Our algorithm cross-examines the wall's loyalty, classifies it into psychological archetypes (e.g., *Nap Polish Certified*, *The Emotional Sponge*, *The Walking Disaster*), highlights tactical red flags, records the audit to a MySQL database with automatic SQLite fallback, and ranks it on the public Wall Hall of Fame & Shame.

---

## Technical Details
### Technologies/Components Used
For Software:
- **Languages used:** Python 3.11, JavaScript (ES6+), HTML5, Vanilla CSS3
- **Frameworks used:** Flask (Python Web Framework)
- **Libraries used:** `mysql-connector-python` (MySQL Database Driver), `sqlite3` (Zero-Config Automatic Failover)
- **Tools used:** Git & GitHub, VS Code, Antigravity IDE, MySQL Server 8.0, Playwright / Browser Testing

For Hardware:
- *Software Only Project (No hardware components required)*

---

### Implementation
For Software:

# Installation
```bash
# 1. Clone the repository
git clone https://github.com/Kashinathpk001/wall-project.git
cd wall-project

# 2. Set up virtual environment
python -m venv venv
.\venv\Scripts\activate      # Windows (pwsh / cmd)
# source venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

# Run
```bash
# Start the Flask development server
python app.py

# Open your browser and navigate to:
# http://127.0.0.1:5000/
```
*(Note: If MySQL is not installed or unreachable, the application automatically activates an embedded SQLite fallback database `wall_trust.db` with zero configuration required!)*

---

### Project Documentation
For Software:

# Screenshots

### 1. Homepage & Apple-Style Starting Reveal
![Homepage](static/images/walls/level_7.jpg)
*Cinematic dark-to-light reveal featuring the motto "We all need some wall to lean on", campus hotspots, live ticker telemetry, and fast presets.*

### 2. The 6 Levels of Wall Health (Visual Tier List)
![6 Levels of Wall Health](static/images/walls/level_1.jpg)
*Ranked visual reference guide from Level 6 (The Dream Wall - 100/100) down to Level 1 (Ancient Wet Moss Wall - 02/100 Biohazard).*

### 3. Interactive Wall Audit & Holographic Radar Scanner
![Audit Scanner](static/images/walls/level_5.jpg)
*Specimen inspection form featuring Kerala campus presets (Lecture Hall 101, Cricket Corridor, Fee Counter) with animated radar telemetry.*

### 4. Certified Wall Dossier & Psychological Archetype
![Wall Dossier](static/images/walls/level_6.jpg)
*Audited report with circular score count-up, pass/caution/fail verdict, psychiatric diagnosis, and red flag warnings.*

---

# Diagrams

### Architecture & Telemetry Workflow
```mermaid
flowchart TD
    A[User Enters Wall Specs or Clicks Campus Preset] --> B[Holographic Scanner Modal Animates]
    B --> C[POST /inspect to Flask Engine]
    C --> D[Calculate Trust Score & Penalties]
    D --> E[Assign Psychological Archetype & Red Flags]
    E --> F{MySQL Database Available?}
    F -- Yes --> G[Save to MySQL 'wall_trust.walls']
    F -- No --> H[Fallback: Save to SQLite 'wall_trust.db']
    G --> I[Render Dynamic Dossier Page]
    H --> I
    I --> J[Public Hall of Fame & Shame Leaderboard]
```
*End-to-end data flow: From user wall parameter inputs, penalty math calculation, dual-database fault-tolerant storage, to live leaderboard ranking.*

---

### Project Demo
# Video
[Add your demo video link here]
*Demonstrates the pitch-black Apple opening animation, testing the Lecture Hall 101 wall, holographic scanning, and inspecting the 6 Levels of Wall Health.*

# Additional Demos
- **Live Local URL:** `http://127.0.0.1:5000/`
- **GitHub Repository:** `https://github.com/Kashinathpk001/wall-project`
- **Interactive Preset Specimens:**
  - 😴 *Lecture Hall 101 Backrow* (70/100 — Nap Polish Certified)
  - 🏏 *Boys Hostel Cricket Corridor* (45/100 — Survived 14 Matches)
  - 🗄️ *College Fee Counter* (100/100 — Impenetrable Bureaucracy)

---

## Team Contributions
- **Kashinath P K**: End-to-end development — backend architecture with Flask, dual MySQL/SQLite fault-tolerant database integration, mathematical scoring algorithm, Apple Keynote-grade CSS & JS animations, holographic scanner UI, 6-level photorealistic visual tier scale, and satirical comedic writing.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
