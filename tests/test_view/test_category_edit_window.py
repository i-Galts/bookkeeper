"""
Тесты для диалогового окна редактирования списка категорий.
"""
import pytest
from pytestqt.qt_compat import qt_api

from PySide6 import QtCore

from bookkeeper.view.category_edit_window \
                import AddCategoryInput, DeleteCategoryInput, EditCategoryWidget


def test_add_cat_name(qtbot):
    cat_list = []
    widget = AddCategoryInput(cat_list)
    qtbot.keyClicks(widget.cat_name, 'Milk')
    assert widget.get_cat_name() == 'Milk'

def test_add_cat_parent(qtbot):
    cat_list = ['Milk, ', 'Bread, Food']
    widget = AddCategoryInput(cat_list)
    qtbot.keyClicks(widget.parent_names, 'Milk')
    assert widget.get_parent() == 'Milk'

def test_add_cat_parent_default(qtbot):
    cat_list = ['Milk, ', 'Bread, Food']
    widget = AddCategoryInput(cat_list)
    assert widget.get_parent() == ''

def test_delete_cat(qtbot):
    cat_list = ['Milk, ', 'Bread, Food']
    widget = DeleteCategoryInput(cat_list)
    qtbot.keyClicks(widget.cat_names, 'Bread')
    assert widget.get_cat_name() == 'Bread'

def test_delete_cat_default(qtbot):
    cat_list = ['Milk, ', 'Bread, Food']
    widget = DeleteCategoryInput(cat_list)
    assert widget.get_cat_name() == ''

category_list = ['Fruits, ', 'Apples, Fruits']
cat_names = [cat.split(',')[0].capitalize() for cat in category_list]
    # exp_list = [['March 10, 2023', 'March 11, 2023', '100', 'Молоко', ''], 
    #             ['March 12, 2023', 'March 13, 2023', '50', 'Хлеб', 'цельнозерновой']]
    # bud_list = ['Fruits, 7, 300', 'Apples, 30, 500']
    # return cat_list


def signal_add_cat(name: str, parent: str):
    category_list.append(f'{name.capitalize()}, {parent.capitalize()}')

def signal_del_cat(name: str):
    ind = cat_names.index(name.capitalize())
    category_list.pop(ind)

@pytest.fixture
def dialog(qtbot):
    window = EditCategoryWidget(category_list, 
                                signal_add_cat, signal_del_cat)
    qtbot.add_widget(window)
    return window

def test_dialog_window_add_cat(qtbot, dialog):
    window = dialog
    qtbot.addWidget(window)
    qtbot.keyClicks(window.add_cat_wdt.cat_name, 'Bananas')
    qtbot.keyClicks(window.add_cat_wdt.parent_names, 'Fruits')
    qtbot.mouseClick(window.add_button, QtCore.Qt.LeftButton)
    assert category_list == ['Fruits, ', 'Apples, Fruits', 'Bananas, Fruits']

def test_dialog_window_del_cat(qtbot, dialog):
    window = dialog
    qtbot.addWidget(window)
    qtbot.keyClicks(window.del_cat_wdt.cat_names, 'Apples')
    qtbot.mouseClick(window.delete_button, QtCore.Qt.LeftButton)
    assert category_list == ['Fruits, ', 'Bananas, Fruits']
