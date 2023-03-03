from PySide6 import QtWidgets, QtCore

class BudgetWidget(QtWidgets.QtWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._budget_table = QtWidgets.QTableWidget()
        self._budget_table.setColumnCount(2)
        self._budget_table.setRowCount(3)
        self._budget_table.setHorizontalHeaderLabels(
                    "Сумма Бюджет".split())
        
