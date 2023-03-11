from pytestqt.qt_compat import qt_api

from bookkeeper.view.expenses_edit_panel \
                import AmountEdit, CommentEdit, CategoryChoice

def test_amount_edit_normal_input(qtbot):
    widget = AmountEdit()
    qtbot.keyClicks(widget.amount, '1234567890')
    assert widget.get_amount() == '1234567890'

def test_amount_edit_empty_input(qtbot):
    widget = AmountEdit()
    assert widget.get_amount() == ''

def test_amount_edit_negative_input(qtbot):
    widget = AmountEdit()
    qtbot.keyClicks(widget.amount, '-1')
    assert widget.get_amount() == '1'

def test_amount_edit_nonumber_input(qtbot):
    widget = AmountEdit()
    qtbot.keyClicks(widget.amount, 'abc')
    assert widget.get_amount() == ''

def test_comment_edit_normal_input(qtbot):
    widget = CommentEdit()
    qtbot.keyClicks(widget.comment_edit, 'test_0')
    assert widget.get_comment() == 'test_0'

def test_comment_edit_empty_input(qtbot):
    widget = CommentEdit()
    assert widget.get_comment() == ''

def test_cat_choice_default(qtbot):
    cat_list = ['Milk', 'Bread']
    widget = CategoryChoice(cat_list)
    assert widget.get_category() == 'Milk'

def test_cat_choice(qtbot):
    cat_list = ['Milk', 'Bread']
    widget = CategoryChoice(cat_list)
    qtbot.keyClicks(widget.combobox, 'Bread')
    assert widget.get_category() == 'Bread'