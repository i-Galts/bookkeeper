import sys
from PySide6 import QtWidgets

class BudgetWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.budget_table = QtWidgets.QTableWidget(3, 2)
        self.budget_table.setColumnCount(2)
        self.budget_table.setRowCount(3)
        self.budget_table.setHorizontalHeaderLabels(
                    "Сумма Бюджет".split())
        self.budget_table.setVerticalHeaderLabels(
                    "День Неделя Месяц".split())
        
        self.vertical_header = self.budget_table.horizontalHeader()
        self.vertical_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.vertical_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        
        self.horizontal_header = self.budget_table.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.horizontal_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.horizontal_header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        
        self.budget_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        
    def set_data(self, data: list[list[str]]) -> None:
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.budget_table.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
            )

    def create(self) -> QtWidgets.QTableWidget:
        return self.budget_table
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.resize(300, 300)
    central_widget = QtWidgets.QTabWidget()
    window.setCentralWidget(central_widget)
    budget_table = BudgetWidget()
    data = [
        ['705.43', '1000'],
        ['6719.43', '7000'],
        ['10592.96', '30000']
    ]
    budget_table.set_data(data)
    vertical_layout = QtWidgets.QVBoxLayout()
    vertical_layout.addWidget(budget_table.create())

    central_widget.setLayout(vertical_layout)
    window.show()

    sys.exit(app.exec())