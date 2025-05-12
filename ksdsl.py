import tkinter as tk
from tkinter import scrolledtext
from itertools import combinations

def generate_gift_sets_optimized(N, K):
    all_gifts = [
        {"name": "Шарик", "cost" : "25"},
        {"name": "Новый год", "cost" : "35"},
        {"name": "Снегурочка", "cost": "50"},
        {"name": "Санта", "cost": "15"},
        {"name": "Снежинка", "cost": "30"},
        {"name": "Рождество", "cost" : "20"}
    ]
    max_cost=50
    valid_sets = []
    # Генерируем все комбинации длины N
    for combo in combinations(all_gifts, N):
        costs=[gift['cost'] for gift in combo]
        cost_sum=int(gift['cost'])
        if sum(int(set(costs))) >= max_cost:
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
