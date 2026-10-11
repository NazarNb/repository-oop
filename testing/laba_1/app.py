class Figure:
    def __init__(self, figure_type: str, length: float):
        if length <= 0:
            raise ValueError("Довжина повинна бути більшою за нуль!")

        valid_types = ["квадрат", "трикутник", "прямокутник"]
        if figure_type.lower() not in valid_types:
            raise ValueError(f"Невідомий тип фігури: {figure_type}")

        self.figure_type = figure_type.lower()
        self.length = length

    @property
    def get_figure_type(self) -> str:
        return self.figure_type

    @property
    def get_figure_length(self) -> float:
        # Помилка була в тому, що властивість не повертала довжину (або повертала None).
        # Виправлено:
        return self.length

    def get_angles(self) -> int:
        """Повертає кількість кутів для фігури."""
        if self.figure_type in ["квадрат", "прямокутник"]:
            return 4
        elif self.figure_type == "трикутник":
            return 3
        raise ValueError("Неможливо визначити кути для даної фігури")


if __name__ == "__main__":
    # Ручна перевірка властивостей об'єктів
    f1 = Figure("квадрат", 10)
    f2 = Figure("трикутник", 6.5)
    print(f"Тип: {f1.get_figure_type}, Довжина: {f1.get_figure_length}, Кути: {f1.get_angles()}")
    print(f"Тип: {f2.get_figure_type}, Довжина: {f2.get_figure_length}, Кути: {f2.get_angles()}")