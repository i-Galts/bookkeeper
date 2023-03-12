from pytestqt.qt_compat import qt_api

from bookkeeper.view.main_window import BookkeeperMainWindow

def test_add_new_expense(qtbot):
    window = BookkeeperMainWindow()