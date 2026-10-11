def count_vowels(text: str) -> int:
    """Рахує кількість голосних літер (українські та англійські)."""
    if not isinstance(text, str):
        raise TypeError("Вхідне значення має бути рядком!")
    
    vowels = "аеєиіїоуюяaeiouyАЕЄИІЇОУЮЯAEIOUY"
    return sum(1 for char in text if char in vowels)