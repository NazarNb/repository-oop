from jikanpy import Jikan

jikan = Jikan()

# Отримуємо аніме поточного сезону
current_season = jikan.seasons(extension='now')

print("--- Аніме цього сезону ---")
# Виводимо назви перших 5-10 серіалів
for anime in current_season['data'][:10]:
    title = anime['title']
    score = anime['score'] if anime['score'] else "Немає оцінки"
    print(f"Аніме: {title} | Оцінка: {score}")