from core import board

def test_cell() -> None:

    # Testing object creation (instance crash)
    a = board.Cell(walkable=True, seethrough=True)
    b = board.Cell(walkable=True, seethrough=False)
    c = board.Cell(walkable=False, seethrough=True)
    d = board.Cell(walkable=False, seethrough=False)
    e = board.Cell()

    # Testing representations
    assert (a.repr() == '(.)')
    assert (b.repr() == '{.}')
    assert (c.repr() == '[.]')
    assert (d.repr() == '<.>')

    # Testing default values
    assert (not e.walkable and e.seethrough)

def test_board():
    # Testing board accessor + type
    # Testing out-of-bounds position
    # Testing board length (shape)
    # Testing board dimensions
    assert True
