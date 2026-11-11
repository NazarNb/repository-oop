from app import get_angles

def test_get_angles_triangle():
    assert get_angles("triangle") == [60, 60, 60]

def test_get_angles_square():
    assert get_angles("square") == [90, 90, 90, 90]

def test_get_angles_rectangle():
    assert get_angles("rectangle") == [90, 90, 90, 90]

def test_get_angles_unknown():
    assert get_angles("unknown") == []