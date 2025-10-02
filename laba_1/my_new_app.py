import random

def guess_game():
    secret_number = random.randint(1, 10)
    print("Привіт! Я загадав число від 1 до 10. Спробуй вгадати!")
    while True:
        try:
            user_input = input("Введи число (або 'q' для виходу): ").strip()
            if user_input.lower() in ('q', 'quit', 'exit'):
                print("Вихід. Побачимось!")
                return
            guess = int(user_input)
        except ValueError:
            print("Невірне введення — введи ціле число від 1 до 10 або 'q' для виходу.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nВихід.")
            return

        if guess < secret_number:
            print("Загадане число більше!")
        elif guess > secret_number:
            print("Загадане число менше!")
        else:
            print("Вітаю! Ти вгадав число 🎉")
            return

if __name__ == "__main__":
    guess_game()
