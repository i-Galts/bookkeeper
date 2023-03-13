import sys

from PySide6 import QtWidgets
from bookkeeper.view.main_window import BookkeeperMainWindow
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.presenter.presenter import Bookkeeper, RepositoryFactory


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BookkeeperMainWindow()
    repo_factory = RepositoryFactory(SQLiteRepository)
    bookkeeper = Bookkeeper(window, repo_factory)
    window.show()
    sys.exit(app.exec())
