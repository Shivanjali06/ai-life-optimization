import sqlite3
from datetime import datetime

DB_NAME = "life_optimization.db"

def init_db():
    """Initializes the SQLite database and creates the daily_logs table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            sleep_hours REAL,
            step_count INTEGER,
            study_hours REAL,
            screen_time_hours REAL,
            expenses REAL,
            predicted_score REAL,
            bottleneck TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_daily_data(sleep, steps, study, screen_time, expenses, score, bottleneck):
    """Inserts or updates today's entries in SQLite."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
        INSERT INTO daily_logs (date, sleep_hours, step_count, study_hours, screen_time_hours, expenses, predicted_score, bottleneck)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            sleep_hours=excluded.sleep_hours,
            step_count=excluded.step_count,
            study_hours=excluded.study_hours,
            screen_time_hours=excluded.screen_time_hours,
            expenses=excluded.expenses,
            predicted_score=excluded.predicted_score,
            bottleneck=excluded.bottleneck
    ''', (today_date, sleep, steps, study, screen_time, expenses, score, bottleneck))
    
    conn.commit()
    conn.close()

def fetch_history_data():
    """Retrieves all logged historical entries ordered chronologically."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT date, sleep_hours, step_count, study_hours, screen_time_hours, expenses, predicted_score, bottleneck FROM daily_logs ORDER BY date ASC')
    rows = cursor.fetchall()
    conn.close()
    return rows
def clear_all_entries():
    """Clears all historical entries from the sqlite database."""
    conn = sqlite3.connect("life_optimization.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_logs")
    conn.commit()
    conn.close()