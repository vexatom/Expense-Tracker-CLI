import sqlite3
from datetime import datetime

from models.expense import Expense


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, path: str = 'data.db'):
        self.path = path
        self.prepare_db()

    def prepare_db(self) -> None:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS `expenses` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                amount INTEGER NOT NULL,
                date TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
            )''')
            conn.commit()

    def save(self, expenses: list[Expense]) -> None:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            for expense in expenses:
                cur.execute('''INSERT OR IGNORE INTO `expenses` (name, category, amount, date)
                    VALUES (?, ?, ?, ?)''',
                            (expense.name, expense.category.value, expense.amount, expense.date))
            conn.commit()

    def add_expense(self, name: str, category: str, amount: float | int, date: datetime) -> int:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute('''INSERT OR IGNORE INTO `expenses` (name, category, amount, date)
                VALUES (?, ?, ?, ?)''',
                        (name, category, amount, date))
            conn.commit()

            return cur.lastrowid if cur.rowcount > 0 else -1

    def del_expense(self, expense_id: int) -> bool:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute('''DELETE FROM `expenses` WHERE id == ?''', (expense_id,))
            conn.commit()

            return True if cur.rowcount > 0 else False

    def get_all_expenses(self) -> list[()]:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            results = cur.execute('''SELECT id, name, category, amount, date FROM `expenses`''').fetchall()

        return results

    def get_expenses_by_category(self, category: str) -> list[()]:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            results = cur.execute('''SELECT id, name, category, amount, date FROM `expenses` 
                                        WHERE category == ?''', (category,)).fetchall()

        return results

    def get_expense(self, expense_id: int) -> ():
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            result = cur.execute('''SELECT id, name, category, amount, date FROM `expenses`
            WHERE id == ?''', (expense_id,)).fetchone()

        return result

    def get_total_expenses(self, category: str | None = None) -> int | float:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            if category is None:
                res = cur.execute('SELECT COALESCE(SUM(amount), 0) FROM `expenses`').fetchone()[0]
            else:
                res = cur.execute('SELECT COALESCE(SUM(amount), 0) FROM `expenses` WHERE category = ?', (category,)).fetchone()[0]

        return res

    def get_expenses_for_the_last_month(self, category: str | None = None) -> int | float:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            if category is None:
                res = cur.execute("""SELECT COALESCE(SUM(amount), 0) FROM `expenses` 
                                    WHERE date >= datetime('now', '-30 days') """).fetchone()[0]
            else:
                res = cur.execute("""SELECT COALESCE(SUM(amount), 0) FROM `expenses` 
                                    WHERE date >= datetime('now', '-30 days') AND category = ?""",
                                  (category,)).fetchone()[0]

        return res
