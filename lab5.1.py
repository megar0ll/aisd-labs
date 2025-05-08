#Вариант 2. Книжный магазин подает рождественские открытки К видов. Покупателю нужно N открыток. Сформировать все возможные комплекты покупки.
from itertools import combinations
import timeit
#Алгоритмический вариант
def generate_gift_sets_algorithmic(N, K):
    all_gifts = list(range(1, K + 1))
    gift_sets = []
    def backtrack(start, path):
        if len(path) == N:
            gift_sets.append(tuple(path))
            return
        for i in range(start, K):
            path.append(all_gifts[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return gift_sets
#Вариант с использованием itertools
def generate_gift_sets_itertools(N, K):
    all_gifts = list(range(1, K + 1))
    return list(combinations(all_gifts, N))
N = int(input("Введите количество открыток, которое нужно купить (N): "))
K = int(input("Введите общее количество видов открыток(K): "))
# Измерение времени выполнения
algorithmic_time = timeit.timeit(lambda: generate_gift_sets_algorithmic(N, K), number=1)
itertools_time = timeit.timeit(lambda: generate_gift_sets_itertools(N, K), number=1)
print("\n1 часть - Результаты:")
print("Алгоритмический вариант:", generate_gift_sets_algorithmic(N, K))
print("Вариант с itertools:", generate_gift_sets_itertools(N, K))
print("\nВремя выполнения:")
print(f"Алгоритмический вариант: {algorithmic_time:.6f} сек")
print(f"Вариант с itertools: {itertools_time:.6f} сек")
