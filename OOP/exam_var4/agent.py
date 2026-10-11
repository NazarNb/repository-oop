import os
from abc import ABC, abstractmethod
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Завантажуємо API-ключ із файлу .env
load_dotenv()

# =====================================================================
# 1. OOP СТРУКТУРА (Абстракція, Наслідування, Інкапсуляція, Поліморфізм)
# =====================================================================

class Person(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @abstractmethod
    def get_role(self) -> str:
        pass


class Student(Person):
    def __init__(self, name: str, age: int = 18):
        super().__init__(name, age)
        # Інкапсуляція: приватний атрибут __grades
        self.__grades: list[float] = []

    def add_grade(self, grade: float):
        if 0 <= grade <= 100:
            self.__grades.append(grade)
        else:
            raise ValueError("Оцінка повинна бути в межах від 0 до 100")

    def average(self) -> float:
        return sum(self.__grades) / len(self.__grades) if self.__grades else 0.0

    def min_grade(self) -> float:
        return min(self.__grades) if self.__grades else 0.0

    def max_grade(self) -> float:
        return max(self.__grades) if self.__grades else 0.0

    # Поліморфізм
    def get_role(self) -> str:
        return "Студент"


class Teacher(Person):
    def __init__(self, name: str, age: int, subject: str):
        super().__init__(name, age)
        self.subject = subject

    def evaluate(self, student: Student, grade: float):
        student.add_grade(grade)

    # Поліморфізм
    def get_role(self) -> str:
        return f"Викладач предмету {self.subject}"


# =====================================================================
# 2. AI-AGENT TOOL (Функція-інструмент)
# =====================================================================

def calculate_grade(name: str, scores: list[float]) -> dict:
    """
    Розраховує статистику успішності студента за його оцінками.
    """
    student = Student(name=name, age=18)
    for score in scores:
        student.add_grade(float(score))
        
    avg = student.average()
    if avg >= 90:
        letter = "A"
    elif avg >= 75:
        letter = "B"
    elif avg >= 60:
        letter = "C"
    else:
        letter = "F"
        
    return {
        "student": student.name,
        "average": round(avg, 2),
        "min": student.min_grade(),
        "max": student.max_grade(),
        "letter_grade": letter
    }


# =====================================================================
# 3. АВТОМАТИЧНИЙ ЗАПУСК ДІАЛОГІВ (ГЕНЕРАЦІЯ ЛОГУ ДЛЯ ЗВІТУ)
# =====================================================================

# Вимога пункту 6: визначення змістовного промпту та root_agent
system_prompt = (
    "Ти є помічником з аналізу успішності студентів. Коли тебе просять проаналізувати "
    "оцінки, ти ОБОВ'ЯЗКОВО викликаєш інструмент `calculate_grade` з правильними аргументами. "
    "На основі повернених даних напиши розгорнуту відповідь українською мовою з порадами."
)

client = genai.Client()

# Нам потрібен простий прямий запуск, щоб обійти баги локального сервера ADK
def run_direct_agent():
    user_inputs = [
        "Привіт! Проаналізуй, будь ласка, оцінки студента Назар: 95, 92, 88, 100, 91.",
        "Які результати у студента Дмитро, якщо у нього такі бали: 60, 72, 65, 58, 70?",
        "Допоможи розібратися з оцінками Олени: 45, 50, 62, 55."
    ]

    print("🤖 Спроба прямого підключення до Gemini через Tool...\n")

    for idx, query in enumerate(user_inputs, 1):
        print(f"--- ДІАЛОГ №{idx} ---")
        print(f"Користувач: {query}\n")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[calculate_grade],
                temperature=0.3,
            )
        )
        print(f"Агент:\n{response.text}\n")
        print("-" * 60)

# Глобальне визначення для ADK (вимога пункту 6)
root_agent = calculate_grade

if __name__ == "__main__":
    run_direct_agent()