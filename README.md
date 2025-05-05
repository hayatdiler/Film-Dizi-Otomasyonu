# 🎬 Film & Series Watchlist Manager

A personal desktop app to manage your movies and TV shows. Add new titles, rate them, keep track of your watch status, and take personal notes — all with a beautiful and user-friendly interface.

---

## 🎯 Goal

To automate manual tracking and provide an efficient, fast, and intuitive system for organizing what you've watched or plan to watch.

---

## ✨ Features

- 📝 Add / Edit / Delete entries  
- 🔍 Filter & Search  
- ⭐ Rate from 0 to 5 stars  
- 📊 Track watch status (Watched / Watching / Not Watched)  
- 🗒️ Add personal notes  
- 🎨 Dark-themed and modern UI  
- 💾 Data stored locally in `veriler.json`  

---

## 🏗️ System Architecture

The project is designed with a **layered architecture** for better organization and scalability:

1. **UI Layer** – Developed with `tkinter`, manages all user interaction  
2. **Business Logic Layer** – Handles the application's core logic (CRUD)  
3. **Data Access Layer** – Manages reading and writing to the JSON file  
4. **Database** – A simple JSON file that stores all user data  

---

## 🛠️ Requirements

- Python 3.7 or higher  
- `tkinter` (usually comes pre-installed)  
- `Pillow` → Install with `pip install Pillow`  
- `pathlib` (comes with Python 3.4+)  

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. Install dependencies:
   ```bash
   pip install Pillow
3. Run the app:
   ```bash
   python InitialApp.py

## 🎯 Usage

- Start → Add a new film or series
- List → View your collection
- Edit → Modify existing entries
- Delete → Remove any entry
- Filter → Search by type, rating, or status

All data is stored locally in films.json. No internet or external database is required.    

## 📫 Contact
For suggestions or bug reports, feel free to open an issue.
Made with ❤️ at Marmara University.
