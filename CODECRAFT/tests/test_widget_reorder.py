from app.widgets.reorder_list import ReorderList

# sprawdzamy czy widget do ukladania kodu dziala
def test_reorder_list_logic(qtbot):
    widget = ReorderList()
    qtbot.addWidget(widget)

    elementy = ["print('B')", "x = 5", "print('A')"]
    for item in elementy:
        widget.addItem(item)

    assert widget.count() == 3

    oczekiwany_kod = "print('B')\nx = 5\nprint('A')"
    assert widget.get_code_string().strip() == oczekiwany_kod

    kod_do_wczytania = "x = 10\nprint(x)"
    widget.load_from_code(kod_do_wczytania)

    assert widget.count() == 2
    assert widget.item(0).text() == "x = 10"
    assert widget.item(1).text() == "print(x)"