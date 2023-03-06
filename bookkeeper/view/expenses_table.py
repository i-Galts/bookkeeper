import sys
from PySide6 import QtWidgets, QtGui

from bookkeeper.view.edit_panel import CategoryChoice

class ExpensesTable(QtWidgets.QTabWidget):
    def __init__(self, cat_list: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.category_list = cat_list

        self.expenses_table = QtWidgets.QTableWidget()
        self.expenses_table.setColumnCount(4)
        self.expenses_table.setRowCount(100)
        self.expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        
        self.header = self.expenses_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        
        self.expenses_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()

        self.set_category_list()

    # def set_data(self, data: list[list[str]]) -> None:
    #     for i, row in enumerate(data):
    #      for j, x in enumerate(row):
    #         self.expenses_table.setItem(
    #             i, j,
    #             QtWidgets.QTableWidgetItem(x.capitalize())
    #         )

    def set_category_list(self) -> None:
        for i, row in enumerate(self.category_list):
            for j, x in enumerate(row):
                self.expenses_table.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
            )

    def create(self) -> QtWidgets.QTableWidget:
       return self.expenses_table
    
class ExpenseInput(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.vl = QtWidgets.QVBoxLayout()
        self.hl = QtWidgets.QHBoxLayout()
        self.setLayout(self.hl)

        self.hl.addLayout(CategoryChoice().create())

        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText('сумма расхода')
        self.amount.setValidator(QtGui.QDoubleValidator(0.0, 1.0E8, 2, self))

        self.date = QtWidgets.QLineEdit()
        self.date.setPlaceholderText('дата расхода дд:мм:гггг')
        self.comment = QtWidgets.QLineEdit()
        self.comment.setPlaceholderText('комментарий')

        self.hl.addWidget(self.amount)
        self.hl.addWidget(self.date)
        self.hl.addWidget(self.comment)

    def is_filled(self):
        return bool(self.amount.text() and self.date.text() and self.comment.text())

        # self.vl.addLayout(hl)
        # должна быть возм-ть добавить еще запись (типо значок "+")

        # save_button = QtWidgets.QPushButton("Сохранить")
        # save_button.clicked.connect(self.save_editted)
        # self.vl.addWidget(save_button)

    # def save_editted(self):
    #         print("Saved!")

class ExpensesListWidget(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Редактировать записи о расходах")
        self.resize(700, 300)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.lines = []
        self.add_line()
        self.add_line()

        print(self.lines)

        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_editted)
        self.main_layout.addWidget(self.save_button)

        self.exec()

    def add_line(self):
        ln = ExpenseInput()
        self.lines.append(ln)
        self.main_layout.addWidget(ln)

    def save_editted(self):
        print("Saved!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.resize(300, 300)
    central_widget = QtWidgets.QTabWidget()
    window.setCentralWidget(central_widget)
    expenses_table = ExpensesTable()
    data = [
        ['2023-01-09 15:09:00', '7.49', 'Хозтовары', 'Пакет на кассе'],
        ['2023-01-09 15:09:00', '104.99', 'Кефир']
    ]
    expenses_table.set_data(data)
    vertical_layout = QtWidgets.QVBoxLayout()
    vertical_layout.addWidget(expenses_table.create())

    central_widget.setLayout(vertical_layout)
    window.show()

    sys.exit(app.exec())