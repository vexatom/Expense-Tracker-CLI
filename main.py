import datetime

from models.category import Category
from models.expense import Expense
from services.tracker import ExpenseTracker
from utils.ui import UI


def deleting_expense(expense: Expense, ui: UI, tracker: ExpenseTracker) -> bool:
    ui.clear()
    ui.header('Deleting expense')
    act = input('Are you sure? (y/n): ').lower()
    ui.line()
    if act == 'y':
        if tracker.delete_expense(expense):
            ui.pause('Your expense has been deleted')
            return True
        else:
            ui.pause('Unable to delete the expense')
            return False
    return False


def show_expense(expense: Expense, ui: UI, tracker: ExpenseTracker) -> None:
    while True:
        ui.clear()
        ui.header('Expense info')
        ui.display_expense(expense)
        print('\n[del] Delete this expense')
        print('[back] Back to list')
        ui.line()
        act = input('Choose an option: ')
        ui.line()
        if act == 'del':
            if deleting_expense(expense, ui, tracker):
                return True
        elif act == 'back':
            break


def show_expenses(expenses: list[Expense], total_expenses: int | float, expenses_for_the_last_month: int | float,
                  ui: UI, tracker: ExpenseTracker):
    page = 1
    while True:
        ui.clear()
        ui.header('Expenses')
        pages = ui.display_expenses(expenses, total_expenses, expenses_for_the_last_month, page=page)
        print('[back] Return to back')
        ui.line()
        act = input('Choose an option: ')
        ui.line()
        if act == 'back':
            break
        elif act == 'np' and pages[1]:
            page += 1
            continue
        elif act == 'pp' and pages[0]:
            page -= 1
            continue
        try:
            act = int(act)
            expense = tracker.get_expense(act)  # The user can select any expense by its ID. This is not a bug.
            if expense:
                if show_expense(expense, ui=ui, tracker=tracker):
                    break
        except ValueError:
            continue


def choice_category(ui: UI) -> Category | None:
    while True:
        ui.clear()
        ui.header('Choose category')
        act_list = ui.display_categories(Category)
        print('[back] Return to back')
        ui.line()
        act = input('Choose an option: ')
        ui.line()
        if act == 'back':
            return None
        try:
            act = int(act)
            if act in act_list.keys():
                return act_list[act]
        except ValueError:
            continue


def add_expense(ui: UI, tracker: ExpenseTracker):
    ui.clear()
    ui.header('Add expense')
    name = input('Enter an expense name: ').strip()
    if not name:
        ui.pause('Operation cancelled. The name cannot be empty')
        return
    category = choice_category(ui=ui)
    if category is None:
        ui.pause('Operation cancelled. No category selected')
        return
    ui.clear()
    ui.header('Add expense')
    try:
        amount = float(input('Amount: '))
        if amount <= 0:
            raise ValueError('Amount must be positive')
    except ValueError:
        ui.pause('Adding cancelled. Amount must be a positive number')
        return
    date = input('Expense date (DD.MM.YYYY HH:MM:SS)(press Enter to use the current date): ')
    if not date:
        date = datetime.datetime.now()
    else:
        try:
            date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        except ValueError:
            ui.pause('Adding was interrupted. Invalid date format')
            return

    ui.line()
    if tracker.add_expense(name, category, amount, date):
        ui.pause('Expense successfully added')
    else:
        ui.pause('Unable to add the expense')


def main():
    ui = UI(50)
    tracker = ExpenseTracker()

    while True:
        ui.clear()
        ui.header('Expense Tracker CLI')
        print('''[all] All expenses
[filter] Filter expenses
[add] Add expense
[exit] Exit program''')
        ui.line()
        act = input('Choose an option: ')
        ui.line()
        if act == 'all':
            expenses = tracker.get_all_expenses()
            total_expenses = tracker.get_total_expenses()
            expenses_for_the_last_month = tracker.get_30_expenses()
            show_expenses(expenses, total_expenses, expenses_for_the_last_month, ui=ui, tracker=tracker)
        elif act == 'filter':
            category = choice_category(ui=ui)
            expenses = tracker.get_expenses_by_category(category)
            total_expenses = tracker.get_total_expenses(category)
            expenses_for_the_last_month = tracker.get_30_expenses(category)
            show_expenses(expenses, total_expenses, expenses_for_the_last_month, ui=ui, tracker=tracker)
        elif act == 'add':
            add_expense(ui=ui, tracker=tracker)
        elif act == 'exit':
            break


if __name__ == '__main__':
    main()
    print('Program finished!')
