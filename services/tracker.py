import datetime

from models.category import Category
from models.expense import Expense
from services.storage import Database


class ExpenseTracker:

    def __init__(self, db_path: str = 'data.db'):
        self.__db = Database(db_path)
        self.expenses = self.__get_expenses()

    def __get_expenses(self) -> list[Expense]:
        expenses = []
        tmp_data = self.__db.get_all_expenses()
        for expense in tmp_data:
            expenses.append(Expense(expense[0], expense[1], expense[2], expense[3], expense[4]))
        return expenses

    def get_all_expenses(self) -> list[Expense]:
        return self.expenses

    def get_expense(self, expense_id: int) -> Expense | None:
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def get_total_expenses(self, category: str | Category | None = None) -> int | float:
        category = category if isinstance(category, str) else None if not category else category.value
        return self.__db.get_total_expenses(category)

    def get_30_expenses(self, category: str | Category | None = None) -> int | float:
        category = category if isinstance(category, str) else None if not category else category.value
        return self.__db.get_expenses_for_the_last_month(category)

    def delete_expense(self, expense: Expense) -> bool:
        if self.__db.del_expense(expense.id):
            self.expenses.remove(expense)
            return True
        return False

    def get_expenses_by_category(self, category: Category) -> list[Expense]:
        category = category.value
        expenses_by_category = []
        tmp_data = self.__db.get_expenses_by_category(category)
        for expense in tmp_data:
            expenses_by_category.append(Expense(expense[0], expense[1], expense[2], expense[3], expense[4]))
        return expenses_by_category

    def add_expense(self, name: str, category: Category, amount: int | float, date: datetime.datetime) -> bool:
        result_id = self.__db.add_expense(name, category.value, amount, date)
        if result_id >= 0:
            self.expenses.append(Expense(result_id, name, category.value, amount, date))
            return True
        return False
