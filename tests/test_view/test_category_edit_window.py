from pytestqt.qt_compat import qt_api

from bookkeeper.view.category_edit_window \
                import AddCategoryInput, DeleteCategoryInput, EditCategoryWidget

def test_add_cat_name(qtbot):
    cat_list = []
    widget = AddCategoryInput(cat_list)
    qtbot.keyClicks(widget.cat_name, 'Milk')
    assert widget.get_cat_name() == 'Milk'

def test_add_cat_parent(qtbot):
    cat_list = ['Milk', 'Bread']
    widget = AddCategoryInput(cat_list)
    qtbot.keyClicks(widget.parent_names, 'Milk')
    assert widget.get_parent() == 'Milk'

def test_add_cat_parent_default(qtbot):
    cat_list = ['Milk', 'Bread']
    widget = AddCategoryInput(cat_list)
    assert widget.get_parent() == ''

def test_delete_cat(qtbot):
    cat_list = ['Milk', 'Bread']
    widget = DeleteCategoryInput(cat_list)
    qtbot.keyClicks(widget.cat_names, 'Bread')
    assert widget.get_cat_name() == 'Bread'

def test_delete_cat_default(qtbot):
    cat_list = ['Milk', 'Bread']
    widget = DeleteCategoryInput(cat_list)
    assert widget.get_cat_name() == ''