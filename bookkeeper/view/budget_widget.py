# """
# Виджет таблицы с бюджетом.
# """
# from typing import Callable

# from PySide6 import QtWidgets

# from bookkeeper.view.expenses_edit_panel import CategoryChoice


# class BudgetTable(QtWidgets.QWidget):
#     """
#     Класс таблицы бюджета. Принимает данные о всех трех
#     моделях для отображения.
#     """
#     def __init__(self, cat_list: list[str],
#                  exp_list: list[list[str]],
#                  bud_list: list[str],
#                  *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.bud_list = bud_list
#         self.cat_list = cat_list
#         self.exp_list = exp_list

#         self.cat_choice = CategoryChoice(cat_list)

#         self.budget_table = QtWidgets.QTableWidget()
#         self.budget_table.setColumnCount(3)
#         self.budget_table.setRowCount(2)
#         self.budget_table.setVerticalHeaderLabels(
#                     "Сумма Бюджет".split())
#         self.budget_table.setHorizontalHeaderLabels(
#                     "День Неделя Месяц".split())

#         self.horizontal_header = self.budget_table.horizontalHeader()
#         self.horizontal_header.setSectionResizeMode(
#             0, QtWidgets.QHeaderView.Stretch)
#         self.horizontal_header.setSectionResizeMode(
#             1, QtWidgets.QHeaderView.Stretch)

#         self.vertical_header = self.budget_table.verticalHeader()
#         self.vertical_header.setSectionResizeMode(
#             0, QtWidgets.QHeaderView.Stretch)
#         self.vertical_header.setSectionResizeMode(
#             1, QtWidgets.QHeaderView.Stretch)
#         self.vertical_header.setSectionResizeMode(
#             2, QtWidgets.QHeaderView.Stretch)

#         self.budget_table.setEditTriggers(
#             QtWidgets.QAbstractItemView.NoEditTriggers)

#         self.fill_columns(self.cat_choice.get_category())

    # def fill_columns(self, cat: str) -> None:
    #     """
    #     Заполнение таблицы для выбранной
    #     пользователем категории cat.
    #     """
    #     if not self.cat_list:
    #         return
    #     if not self.exp_list:
    #         exp_per_day = 0
    #     if not self.bud_list:
    #         bud_per_day = 0
    #     else:
    #         sum_amount = 0.0
    #         days_count = 0
    #         for exp in self.exp_list:
    #             if (exp[3].lower() == cat.lower()):
    #                 exp_amount = float(exp[2])
    #                 sum_amount += exp_amount
    #                 days_count += 1
    #         try:
    #             exp_per_day = sum_amount / days_count
    #         except ZeroDivisionError:
    #             exp_per_day = 0

    #         for bud in self.bud_list:
    #             if (bud.split(',')[0].lower() == cat.lower()):
    #                 period = int(bud.split(',')[1])
    #                 bud_amount = float(bud.split(',')[2])
    #         try:
    #             bud_per_day = bud_amount / period
    #         except ZeroDivisionError:
    #             bud_per_day = 0

    #         days = [1, 7, 30]
    #         for i in days:
    #             self.budget_table.setItem(
    #                     0, i,
    #                     QtWidgets.QTableWidgetItem(exp_per_day * i))
    #             self.budget_table.setItem(
    #                     1, i,
    #                     QtWidgets.QTableWidgetItem(bud_per_day * i))

    # def create_show_budget_button(self):
    #     """
    #     Привязка кнопки для отображения бюджета.
    #     """
    #     self.show_budget_button = QtWidgets.QPushButton('Показать бюджет')
    #     self.show_budget_button.clicked.connect(
    #                             self.show_budget_button_clicked)
    #     return self.show_budget_button

    # def register_show_budget_button(self,
    #                                 handler: Callable[[None], None]):
    #     """
    #     Регистрация действий при нажатии на
    #     кнопку для отображения бюджета.
    #     """
    #     def show_budget_button_clicked():
    #         chosen_cat = self.cat_choice.get_category()
    #         self.fill_columns(chosen_cat)
    #         handler()
    #     self.show_budget_button_clicked = show_budget_button_clicked

    # def create_table(self):
    #     return self.budget_table

    # def create_cat_choice(self) -> QtWidgets.QHBoxLayout:
    #     return self.cat_choice.create_choice()

    # def create(self):
    #     return self.main_layout

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = QtWidgets.QMainWindow()
#     window.resize(300, 300)
#     central_widget = QtWidgets.QTabWidget()
#     window.setCentralWidget(central_widget)
#     budget_table = BudgetWidget()
#     data = [
#         ['705.43', '1000'],
#         ['6719.43', '7000'],
#         ['10592.96', '30000']
#     ]
#     budget_table.set_data(data)
#     vertical_layout = QtWidgets.QVBoxLayout()
#     vertical_layout.addWidget(budget_table.create())

#     central_widget.setLayout(vertical_layout)
#     window.show()

#     sys.exit(app.exec())
