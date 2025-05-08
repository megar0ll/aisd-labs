#Вариант 2. Книжный магазин подает рождественские открытки К видов. Покупателю нужно N открыток. Сформировать все возможные комплекты покупки.
from itertools import combinations
#Усложненная программа
def generate_gift_sets_optimized(N, K):
    all_gifts = [
        {"name": "Шарик", "color": "красный"},
        {"name": "Новый год", "color": "синий"},
        {"name": "Снегурочка", "color": "голубой"},
        {"name": "Санта", "color": "красный"},
        {"name": "Снежинка", "color": "серебряный"},
        {"name": "Рождество", "color": "белый"}
    ]
    # Ограничения: какие открытки нельзя комбинировать
    restrictions = {
        "Шарик": ["Снежинка"],
        "Санта": ["Снегурочка"]
    }
    valid_sets = []
    # Генерируем все комбинации длины N
    for combo in combinations(all_gifts, N):
        # Проверяем ограничение по цветам (все цвета должны быть разными)
        colors = [gift["color"] for gift in combo]
        if len(set(colors)) != N:
            continue
        # Проверяем ограничения по темам
        valid = True
        names = [gift["name"] for gift in combo]
        for name in names:
            if name in restrictions:
                for forbidden in restrictions[name]:
                    if forbidden in names:
                        valid = False
                        break
                if not valid:
                    break
        if valid:
            valid_sets.append([gift["name"] for gift in combo])
    return valid_sets
def target_function(gift_sets):
    if not gift_sets:
        return 0
    # Находим набор с максимальным количеством уникальных тем
    max_unique = max(len(set(gift_set)) for gift_set in gift_sets)
    optimal_solutions = [gift_set for gift_set in gift_sets if len(set(gift_set)) == max_unique]
    # Возвращаем количество оптимальных решений
    return len(optimal_solutions)
# Для второй части фиксируем параметры
N = 2
K = 6
print("\n2 часть - Усложненная программа:")
all_gift_sets = generate_gift_sets_optimized(N, K)
print("Все возможные валидные комбинации:")
for i, gift_set in enumerate(all_gift_sets, 1):
    print(f"{i}. {gift_set}")
optimal_count = target_function(all_gift_sets)
print(f"\nКоличество оптимальных решений: {optimal_count}")
