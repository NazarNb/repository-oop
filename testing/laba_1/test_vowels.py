import unittest
from vowels import count_vowels


class TestCountVowels(unittest.TestCase):

    def test_regular_words(self):
        """Звичайні слова."""
        self.assertEqual(count_vowels("python"), 2)
        self.assertEqual(count_vowels("hello"), 2)

    def test_empty_string(self):
        """Вимога: перевірка порожнього рядка."""
        self.assertEqual(count_vowels(""), 0)

    def test_digits_and_symbols(self):
        """Вимога: рядок з цифрами та символами."""
        self.assertEqual(count_vowels("12345!@#$"), 0)
        self.assertEqual(count_vowels("test 123"), 1)

    def test_ukrainian_letters(self):
        """Вимога: українські літери різного регістру."""
        self.assertEqual(count_vowels("програмування"), 5)
        self.assertEqual(count_vowels("ЮНІТ ТЕСТ"), 3)

    def test_wrong_type(self):
        """Перевірка винятку при неправильному типі даних."""
        with self.assertRaises(TypeError):
            count_vowels(12345)


if __name__ == "__main__":
    unittest.main()