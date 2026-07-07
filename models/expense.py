from datetime import datetime

from models.category import Category


class Expense:

    def __init__(self, name: str, category: str, amount: int, date: datetime = None):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self.category = None

        for _category in Category:
            if category.lower() == _category.value.lower():
                self.category = _category

        if self.category is None:
            raise ValueError("Unknown category")

        self.name = name
        self.amount = amount
        self.date = date if date else datetime.now()

    def change_name(self, name: str):
        self.name = name

    def change_category(self, category: str):
        self.category = category

    def change_amount(self, amount: int):
        self.amount = amount

    def change_date(self, date: datetime):
        self.date = date