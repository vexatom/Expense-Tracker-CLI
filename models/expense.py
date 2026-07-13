from datetime import datetime

from models.category import Category


class Expense:

    def __init__(self, expense_id: int, name: str, category: str, amount: int, date: datetime = None):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self.category = None

        for _category in Category:
            if category.lower() == _category.value.lower():
                self.category = _category

        if self.category is None:
            raise ValueError("Unknown category")

        self.id = expense_id
        self.name = name
        self.amount = amount
        try:
            if isinstance(date, datetime):
                self.date = date
            else:
                formats = [
                    '%Y-%m-%d %H:%M:%S.%f',
                    '%Y-%m-%d %H:%M:%S'
                ]

                for fmt in formats:
                    try:
                        self.date = datetime.strptime(date, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError("Unsupported date format")

        except (ValueError, TypeError) as _e:
            self.date = datetime.now()

    def __str__(self):
        return str(self.id)

    def change_name(self, name: str):
        self.name = name

    def change_category(self, category: str):
        self.category = category

    def change_amount(self, amount: int):
        self.amount = amount

    def change_date(self, date: datetime):
        self.date = date
