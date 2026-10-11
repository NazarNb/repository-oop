# Звіт до роботи
## Тема: Тестування з бібліотекою pytest
### Мета роботи: _Навчитись писати тести за допомогою pytest, використовувати fixtures, маркери та параметризацію_;

---
### Виконання роботи

#### Встановлення pytest
```bash
poetry add --group dev pytest
```

#### Запуск існуючих тестів
```bash
poetry run pytest -v
```
![](photo/src1.1.png)

#### 1. Fixture з довжиною 10
Додав fixture яка повертає фігуру з довжиною 10 та два тести для перевірки її властивостей:
```python
@pytest.fixture
def figure_length_10():
    return Figure("квадрат", 10)

def test_figure_length_10(figure_length_10):
    assert figure_length_10.get_figure_length == 10

def test_figure_type_length_10(figure_length_10):
    assert figure_length_10.type == "квадрат"
```
![](photo/src1.2.png)

#### 2. Маркер `unit`
Додав маркер `unit` до двох тестів (`test_triangle_type` та `test_square_angles`) та зареєстрував його у файлі `pytest.ini`:
```ini
[pytest]
markers =
    unit: швидкі юніт-тести
```
Запуск тільки тестів з маркером:
```bash
poetry run pytest -m unit -v
```
Результат: `2 passed, 12 deselected` — виконались лише два тести з маркером, решту 12 тестів було пропущено.

![](photo/src1.3.png)

#### 3. Fixture зі `scope="module"`
```python
@pytest.fixture(scope="module")
def allowed_figures():
    return Figure.FIGURES

def test_figures_count(allowed_figures):
    assert len(allowed_figures) == 3

def test_figures_contains_square(allowed_figures):
    assert "квадрат" in allowed_figures
```
Fixture з `scope="module"` створюється один раз на весь файл з тестами, а не перед кожним тестом.

#### Повний запуск усіх тестів
Після всіх змін запустив усі тести:
```bash
pytest -x --tb=short
```
Результат: зібрано 14 тестів, усі 14 пройшли успішно (`14 passed in 0.05s`).

#### Різниця між `unittest.TestCase` та функцією `pytest`
- `unittest` вимагає клас який наслідує `TestCase` та методи що починаються з `test_`
- `pytest` дозволяє писати прості функції без класу, використовує звичайний `assert` замість `assertEqual`, `assertTrue` тощо

#### Параметризація
Дозволяє виконати один тест для кількох наборів даних:
```python
@pytest.mark.parametrize("figure_type", ["квадрат", "трикутник"])
def test_allowed_figure(figure_type):
    assert Figure(figure_type, 1).type == figure_type
```

### Висновки
У ході роботи я навчився писати тести за допомогою pytest: створювати fixtures (у тому числі з `scope="module"`), позначати тести маркерами та запускати вибірково через `-m`, а також використовувати параметризацію. Порівняно з `unittest`, pytest дозволяє писати простіший код без класів і спеціальних методів перевірки.