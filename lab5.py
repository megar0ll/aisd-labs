from itertools import combinations
import timeit
# 1 часть-Алгоритмический вариант
def generate_gift_sets_algorithmic(N, K):
    all_gifts = list(range(1, K+1))
    gift_sets = []  # Список для хранения всех комбинаций открыток
    # Алгоритмический подход к генерации всех возможных комбинаций открыток
    def generate_combinations(offset, remaining, combination):
        if remaining == 0:  # базовый случай: если осталось выбрать 0 открыток
            gift_sets.append(tuple(combination))
            return
        for i in range(offset, K):
            new_combination = combination + [all_gifts[i]]  # добавляем открытку в текущую комбинацию
            generate_combinations(i + 1, remaining - 1, new_combination)  # рекурсивно генерируем комбинации для оставшихся открыток
    generate_combinations(0, N, [])
    return gift_sets
# 1 часть - Вариант с использованием функций Python
def generate_gift_sets_pythonic(N, K):
    all_gifts = list(range(1, K+1))
    gift_sets = []  # Список для хранения всех комбинаций открыток
    # Алгоритмический подход к генерации всех возможных комбинаций открыток
    for i in range(1 << K):  # генерируем все подмножества множества открыток
        combination = [all_gifts[j] for j in range(K) if (i & (1 << j))]  # формируем комбинацию на основе битовой маски
        if len(combination) == N:
            gift_sets.append(combination)
    return gift_sets
N = 5  # количество открыток, которые нужно купить
K = 10  # общее количество видов открыток
# Измерение времени выполнения алгоритмического варианта
algorithmic_time = timeit.timeit(lambda: generate_gift_sets_algorithmic(N, K), number=1)
# Измерение времени выполнения варианта с использованием функций Python
pythonic_time = timeit.timeit(lambda: generate_gift_sets_pythonic(N, K), number=1)
print("1 часть - Результат работы алгоритмической функции:", generate_gift_sets_algorithmic(N, K))
print("Результат работы с помощью использования Python функции:", generate_gift_sets_pythonic(N, K))
print("\nВремя выполнения алгоритмического варианта:", algorithmic_time)
print("Время выполнения варианта с использованием функций Python:", pythonic_time)
# 2 часть - Усложненная программа
def generate_gift_sets_optimized(N, K):
    all_gifts = [
        {"name": "Рождество", "color": "красный"},
        {"name": "Новый год", "color": "синий"},
        {"name": "Зима", "color": "белый"},
        {"name": "Санта", "color": "красный"},
        {"name": "Снежинка", "color": "серебряный"}
    ]
    similar_theme = {"Рождество": ["Новый год"], "Санта": ["Зима"]}
    gift_sets = []
    for r in range(1, K + 1):
        comb = combinations(all_gifts, r)
        for c in comb:
            if len(set([gift["color"] for gift in c])) == N:  # Ограничение на цвета
                add_set = True
                # Проверка ограничений на характеристики объектов
                for theme, similar_themes in similar_theme.items():
                    if theme in [gift["name"] for gift in c]:
                        for sim_theme in similar_themes:
                            if sim_theme in [gift["name"] for gift in c]:
                                add_set = False
                                break
                        if not add_set:
                            break
                if add_set:
                    gift_sets.append([gift["name"] for gift in c])
    return gift_sets
def target_function(gift_sets):
    max_unique_themes = 0
    optimal_solution = None
    for gift_set in gift_sets:
        unique_themes = len(set(gift_set))
        if unique_themes > max_unique_themes:
            max_unique_themes = unique_themes
            optimal_solution = gift_set
    return len(optimal_solution) if optimal_solution else 0
N = 3  # Количество открыток, которые нужно купить
K = 5  # Общее количество видов открыток
# Генерация всех возможных комбинаций покупки
all_gift_sets = generate_gift_sets_optimized(N, K)
# Вычисление целевой функции
optimal_solution = target_function(all_gift_sets)
# Вывод результатов
print("\n2 часть - Все возможные комбинации покупки:")
for gift_set in all_gift_sets:
    print(gift_set)
print("\nОптимальное решение (количество возможных комбинатов):", optimal_solution)
