"""
Тесты для диалогового окна редактирования бюджета.
"""
import pytest
from pytestqt.qt_compat import qt_api

from PySide6 import QtCore

from bookkeeper.view.budget_edit_window \
                import EditBudgetWidget


budget_list = ['Fruits, , ', 'Apples, , ']
cat_names = [cat.split(',')[0].capitalize() for cat in budget_list]
    # exp_list = [['March 10, 2023', 'March 11, 2023', '100', 'Молоко', ''], 
    #             ['March 12, 2023', 'March 13, 2023', '50', 'Хлеб', 'цельнозерновой']]
    # bud_list = ['Fruits, 7, 300', 'Apples, 30, 500']
    # return cat_list

def signal_add_bud(category: str, period: str, amount: str):
    budget_list.append(f'{category.capitalize()}, ' 
                       f'{period}, {amount}')

def signal_del_bud(name: str):
    ind = cat_names.index(name.capitalize())
    budget_list.pop(ind)

@pytest.fixture
def dialog(qtbot):
    window = EditBudgetWidget(budget_list, 
                              signal_add_bud, signal_del_bud)
    qtbot.add_widget(window)
    return window

def test_dialog_window_add_bud(qtbot, dialog):
    window = dialog
    qtbot.addWidget(window)
    qtbot.keyClicks(window.add_bud_wdt.cat_names, 'Apples')
    qtbot.keyClicks(window.add_bud_wdt.period, '30')
    qtbot.keyClicks(window.add_bud_wdt.amount, '700')
    qtbot.mouseClick(window.add_button, QtCore.Qt.LeftButton)
    assert budget_list == ['Fruits, , ', 'Apples, , ', 'Apples, 30, 700']
