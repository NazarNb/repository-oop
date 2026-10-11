import pytest
from app import Figure


# Fixture зі scope="module" (використовується повторно у кількох тестах)
@pytest.fixture(scope="module")
def default_square():
    return Figure("квадрат", 10)


# Звичайна fixture
@pytest.fixture
def figure_len_10():
    return Figure("трикутник", 10)


# 1. Тести з маркером unit
@pytest.mark.unit
def test_triangle_type():
    triangle = Figure("трикутник", 4)
    assert triangle.type == "трикутник"


@pytest.mark.unit
def test_square_angles(default_square):
    assert default_square.get_angles() == 4


# 2. Другий тест, який використовує fixture зі scope="module"
def test_module_fixture_reuse(default_square):
    assert default_square.get_figure_length == 10
    assert default_square.type == "квадрат"


# 3. Перевірка fixture з довжиною 10
def test_figure_fixture_length(figure_len_10):
    assert figure_len_10.get_figure_length == 10
    assert figure_len_10.type == "трикутник"


# 4. Параметризований тест для всіх дозволених фігур
@pytest.mark.parametrize("fig_type", Figure.FIGURES)
def test_allowed_figures(fig_type):
    fig = Figure(fig_type, 5)
    assert fig.type == fig_type


# 5. Тести для неправильних значень довжини (0 та від'ємні)
@pytest.mark.parametrize("bad_length", [0, -1, -10])
def test_invalid_lengths(bad_length):
    with pytest.raises(AssertionError):
        Figure("квадрат", bad_length)


# 6. Тести для неправильних типів фігур
@pytest.mark.parametrize("bad_type", ["коло", "трапеція", "овал", ""])
def test_invalid_figure_types(bad_type):
    with pytest.raises(AssertionError):
        Figure(bad_type, 5)