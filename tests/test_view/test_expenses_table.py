from pytestqt.qt_compat import qt_api

from bookkeeper.view.expenses_table import ExpensesTable

def test_empty_table(qtbot):
    exp_list = []
    widget = ExpensesTable([]).create()
    for i in range(100):
        for j in range(5):
            assert widget.item(i, j) == None

def test_table_with_records(qtbot):
    exp_list = [['March 10, 2023', 'March 11, 2023', '100', 'Молоко', ''], 
                ['March 12, 2023', 'March 13, 2023', '50', 'Хлеб', 'цельнозерновой']]
    widget = ExpensesTable(exp_list).create()
    assert widget.item(0, 2).text() == '100'
    assert widget.item(0, 4).text() == ''
    assert widget.item(1, 4).text() == 'Цельнозерновой'