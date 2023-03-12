import pytest
from pytestqt.qt_compat import qt_api

from PySide6 import QtGui

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.main_window import BookkeeperMainWindow
from bookkeeper.presenter.presenter import Bookkeeper, RepositoryFactory


@pytest.fixture
def app(qtbot):
    window = BookkeeperMainWindow()
    qtbot.add_widget(window)
    repo_fact = RepositoryFactory(MemoryRepository)
    presenter = Bookkeeper(window, repo_fact)

    return window

def test_click_menu_bar(app):
    # cat_edit_win_action = app.findChild(QtGui.QAction, 'edit_cats_action')
    # cat_edit_win_action.trigger()
    pass



# def test_menubar_click(qtbot):
#     window = BookkeeperMainWindow()
#     repo_fact = RepositoryFactory(MemoryRepository)
#     presenter = Bookkeeper(window, repo_fact)
