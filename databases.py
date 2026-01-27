import sqlite3
import csv
import os
from datetime import datetime
from typing import List, Tuple


class GameDatabase:
    def __init__(self):
        self.db_path = "game_data.db"
        self.csv_path = "game_progress.csv"
        self.init_database()
        self.init_csv()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_mode TEXT NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER,
                date TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_mode_score 
            ON records(game_mode, score DESC)
        ''')

        conn.commit()
        conn.close()

    def init_csv(self):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'timestamp', 'game_mode', 'score',
                    'level', 'moves_left', 'lines_cleared'
                ])

    def save_record(self, game_mode: str, score: int, level: int = None) -> bool:
        date_str = datetime.now().strftime("%d.%m.%Y")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if level:
            cursor.execute('''
                SELECT score FROM records 
                WHERE game_mode = ? AND level = ?
                ORDER BY score DESC LIMIT 1
            ''', (game_mode, level))
        else:
            cursor.execute('''
                SELECT score FROM records 
                WHERE game_mode = ?
                ORDER BY score DESC LIMIT 1
            ''', (game_mode,))

        existing_record = cursor.fetchone()

        if existing_record is None or score > existing_record[0]:
            cursor.execute('''
                INSERT INTO records (game_mode, score, level, date)
                VALUES (?, ?, ?, ?)
            ''', (game_mode, score, level, date_str))

            conn.commit()
            conn.close()

            self.save_to_csv(game_mode, score, level)
            return True

        conn.close()

        self.save_to_csv(game_mode, score, level)
        return False

    def save_to_csv(self, game_mode: str, score: int, level: int = None,
                    moves_left: int = 0, lines_cleared: int = 0):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.csv_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, game_mode, score,
                level if level else '',
                moves_left, lines_cleared
            ])

    def get_best_records(self, limit: int = 10) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT game_mode, score, level, date 
            FROM records 
            ORDER BY score DESC 
            LIMIT ?
        ''', (limit,))

        records = cursor.fetchall()
        conn.close()

        return records

    def get_records_by_mode(self, game_mode: str, limit: int = 10) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT game_mode, score, level, date 
            FROM records 
            WHERE game_mode = ?
            ORDER BY score DESC 
            LIMIT ?
        ''', (game_mode, limit))

        records = cursor.fetchall()
        conn.close()

        return records

    def get_today_records(self) -> List[Tuple]:
        today = datetime.now().strftime("%d.%m.%Y")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT game_mode, score, level, date 
            FROM records 
            WHERE date = ?
            ORDER BY score DESC
        ''', (today,))

        records = cursor.fetchall()
        conn.close()

        return records

    def get_all_records(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT game_mode, score, level, date 
            FROM records 
            ORDER BY date DESC, score DESC
        ''')

        records = cursor.fetchall()
        conn.close()

        return records

    def get_classic_record(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT score FROM records 
            WHERE game_mode = 'classic'
            ORDER BY score DESC 
            LIMIT 1
        ''')

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else 0

    def get_level_record(self, level_number):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT score FROM records 
            WHERE game_mode = 'adventure' AND level = ?
            ORDER BY score DESC 
            LIMIT 1
        ''', (level_number,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else 0


db = GameDatabase()
