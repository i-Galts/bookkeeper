from pytestqt.qt_compat import qt_api

from PySide6 import QtWidgets

from bookkeeper.view.budget_widget import BudgetWidget

def test_only_cat_input(qtbot):
    main_window = QtWidgets.QMainWindow()
    exp_list = []
    bud_list = []
    cat_list = ['Fruits, ', 'Apples, Fruits']
    widget = BudgetWidget(cat_list, exp_list, bud_list)
    widget.fill_columns('Fruits')
    qtbot.keyClicks(widget.cat_choice, 'Fruits')
    assert widget.cat_choice.get_category() == 'Fruits'
    for i in range(2):
        for j in range(3):
            assert widget.create_table().item(i, j) == None
