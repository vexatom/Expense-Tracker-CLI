import os

from models.category import Category
from models.expense import Expense


class UI:

    def __init__(self, w: int):
        self.w = w

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def header(self, head: str, sym: str = '=') -> None:
        print(head.center(self.w, sym))

    def line(self, sym: str = '=') -> None:
        print(sym * self.w)

    def pause(self, message: str) -> None:
        input(f'{message}\n\n(Press Enter to continue)')

    def display_categories(self, categories: Category) -> dict:
        result = {}
        for i, category in enumerate(categories, start=1):
            print(f'[{i}] {category.value}')
            result[i] = category
        return result

    def display_expenses(self, expenses: list[Expense], total_expenses: int | float,
                         expenses_for_the_last_month: int | float,
                         h: int = 4, page: int = 1) -> [bool, bool]:
        text = ''

        if page < 1:
            raise ValueError('Page must be greater than zero')

        start = (page - 1) * h
        expenses = sorted(expenses, key=lambda exp: exp.date)
        pages_exist = [False, False]

        if not expenses:
            print('You don\'t have any expenses yet.\nAdd one to get started\n')
            return pages_exist

        text += f'Total expenses: ${total_expenses:.2f}\nExpenses for the last month: ${expenses_for_the_last_month:.2f}\n\n'

        for i in range(h):
            indx = start + i
            if indx >= len(expenses):
                break
            expense = expenses[indx]
            text += (f'[{expense.id}] {expense.date.strftime("%d.%m.%Y %H:%M:%S")} | '
                     f'{expense.name} | {expense.category.value} | ${expense.amount:.2f}\n')

        if page > 1:
            text += '[pp] Previous page\n'
            pages_exist[0] = True
        try:
            if expenses[page * h + 1]:
                text += '[np] Next page\n'
                pages_exist[1] = True
        except IndexError:
            pass

        print(text)
        return pages_exist

    def display_expense(self, expense: Expense) -> None:
        print(f'''Name: {expense.name}
Category: {expense.category.value}
Amount: {expense.amount:.2f}
Date: {expense.date.strftime("%d.%m.%Y %H:%M:%S")}''')
