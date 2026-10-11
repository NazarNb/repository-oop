import unittest
from unittest.mock import patch
from app import Figure


def get_user_figure_length() -> float:
    """Функція з input(), яку перевіряємо через patch."""
    user_input = input("Введіть довжину сторони фігури: ")
    return float(user_input)


class TestFigure(unittest.TestCase):

    def setUp(self):
        """Виконується перед кожним тестом."""
        self.square = Figure("квадрат", 10)
        self.triangle = Figure("трикутник", 5)
        self.rectangle = Figure("прямокутник", 8)

    # 1. Тест довжини (виправлений)
    def test_figure_length(self):
        self.assertEqual(self.square.get_figure_length, 10)

    # 2. Тести методу get_angles для різних фігур
    def test_get_angles(self):
        self.assertEqual(self.square.get_angles(), 4)
        self.assertEqual(self.rectangle.get_angles(), 4)
        self.assertEqual(self.triangle.get_angles(), 3)

    # 3. Граничні значення та винятки: нульова і від'ємна довжина, невідомий тип
    def test_zero_length_raises_error(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)

    def test_negative_length_raises_error(self):
        with self.assertRaises(ValueError):
            Figure("трикутник", -5)

    def test_unknown_figure_type_raises_error(self):
        with self.assertRaises(ValueError):
            Figure("коло", 10)

    # 4. subTest для перевірки всіх типів Figure
    def test_all_figure_types_subtest(self):
        cases = [
            ("квадрат", 4),
            ("прямокутник", 4),
            ("трикутник", 3)
        ]
        for fig_type, expected_angles in cases:
            with self.subTest(figure_type=fig_type):
                fig = Figure(fig_type, 7)
                self.assertEqual(fig.get_angles(), expected_angles)

    # 5. Тестування input() за допомогою unittest.mock.patch
    @patch("builtins.input", return_value="14.5")
    def test_input_with_patch(self, mock_input):
        result = get_user_figure_length()
        self.assertEqual(result, 14.5)
        mock_input.assert_called_once()


if __name__ == "__main__":
    unittest.main()