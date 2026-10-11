class Figure:
    FIGURES = ["квадрат", "прямокутник", "трикутник"]

    def __init__(self, figure_type: str, length: float):
        assert length > 0, "Довжина має бути більшою за нуль!"
        assert figure_type in self.FIGURES, f"Недозволений тип фігури: {figure_type}"

        self.type = figure_type
        self.length = length

    @property
    def get_figure_type(self) -> str:
        return self.type

    @property
    def get_figure_length(self) -> float:
        return self.length

    def get_angles(self) -> int:
        angles = {
            "трикутник": 3,
            "квадрат": 4,
            "прямокутник": 4,
        }
        return angles[self.type]