def check_positive_number(num):
    """Функція перевіряє, чи число більше за нуль."""
    if not isinstance(num, (int, float)):
        raise ValueError("Введене значення має бути числом!")
    if num <= 0:
        raise ValueError("Число має бути більшим за нуль!")
    return num


if __name__ == "__main__":
    # 1. Перевірка правильного введення
    correct_number = 15
    result = check_positive_number(correct_number)
    assert result > 0, "Число має бути більшим за нуль!"
    print(f"[OK] Правильне число: {result}")

    # 2. Перевірка неправильного введення (викине помилку)
    bad_number = -7
    print(f"Спроба перевірки числа: {bad_number}")
    assert bad_number > 0, "Число має бути більшим за нуль!"