import sqlite3

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
                expense_id INTEGER NOT NULL UNIQUE,
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
                cur.execute('''INSERT OR IGNORE INTO `expenses` (expense_id, name, category, amount, date)
                    VALUES (?, ?, ?, ?, ?)''',
                            (expense.expense_id, expense.name, expense.category.value, expense.amount, expense.date))
            conn.commit()

    def add_expense(self, expense: Expense) -> bool:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute('''INSERT OR IGNORE INTO `expenses` (expense_id, name, category, amount, date)
                VALUES (?, ?, ?, ?, ?)''',
                        (expense.expense_id, expense.name, expense.category.value, expense.amount, expense.date))
            conn.commit()

            return True if cur.rowcount > 0 else False

    def del_expense(self, expense_id: int) -> None:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute('''DELETE FROM `expenses` WHERE expense_id == ?''', (expense_id,))
            conn.commit()

            return True if cur.rowcount > 0 else False

    def load_data(self) -> list[()]:
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            results = cur.execute('''SELECT (expense_id, name, category, amount, date) FROM `expenses`''').fetchall()

        return results
