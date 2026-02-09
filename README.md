****CS 361 Fitness Tracker - Assignment 5 Milestone****
A simple web application fitness tracker that allows users to log workouts, view workout history,
and track progress towards a fitness goal.
Built as part of CS 361 main program

**Features**
- Workout Entry
   - Log workout type, duration, date, and notes.
   - Live status indicator.
   - Validation and confirmation messages.
- Workout History
   - Displays workouts in a labeled table.
   - Delete workouts with confirmation prompt
- Progress Summary
   - Workouts stored in json
   - Goal stored in json
**Tech Used**
- Python
  - matplotlib
- HTML
- CSS
- JavaScript
- JSON file storage

**Project Structure**
- Assignment5_milestone1/
    - app.py
    - requirements.txt
    - README.md
    - data/
        - workouts.json
        - goal.json
    - static/
        - style.css
        - app.js
        - progress_chart.png
    - template/
        - base.html
        - entry.html
        - history.html
        - progress/html
  
**Setup instructions**
1) Clone Repository:
   git clone <repo name>
   cd Assignment5_milestone1
2) Create virtual environemnt (program won't run if not working in a venv)
   python3 -m venv .venv
   source .venv/bin/activate
3) Install dependencies
   pip install -r requirements.txt
4) run application: python app.py (make sure you're in the Assignment5_milestone1 directory

**Data Storage**
Workouts are stored in workouts.json
Goals are stored in goal.json



