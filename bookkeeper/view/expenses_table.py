from PySide6 import QtWidgets, QtCore

class ExpensesTable(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._expenses_table = QtWidgets.QTableWidget()
        self._expenses_table.setColumnCount(4)
        self._expenses_table.setRowCount(100)
        self._expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        
        self.header = self._expenses_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeToContents)
        
        self._expenses_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()

    def set_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
         for j, x in enumerate(row):
            self._expenses_table.setItem(
                i, j,
                QtWidgets.QTableWidgetItem(x.capitalize())
            )