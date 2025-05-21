import itertools
import timeit
# Список кандидатов с их уровнем знаний (от 1 до 10)
candidates = {1: 8, 2: 10, 3: 7, 4: 6, 5: 9, 6: 4}
# Ограничения:
MIN_MID_AVG = 7
MIN_JUN_AVG = 5
# Целевая функция: максимизировать общий уровень команды
def team_score(team):
    mids, juns = team
    return sum(candidates[m] for m in mids) + sum(candidates[j] for j in juns)
#Оптимизация: сначала отфильтруем кандидатов, чтобы сократить перебор
def get_possible_roles(candidates):
    # Кандидаты, которые могут быть мидлами (уровень ≥ 6, т.к. даже в паре с 10 дадут среднее ≥7)
    possible_mids = [cid for cid, lvl in candidates.items() if lvl >= 6]
    # Кандидаты, которые могут быть джунами (уровень ≥4, т.к. даже в паре с 6 дадут среднее ≥5)
    possible_juns = [cid for cid, lvl in candidates.items() if lvl >= 4]
    return possible_mids, possible_juns
#Оптимизированный перебор с предварительной фильтрацией
def optimized_search(candidates):
    possible_mids, possible_juns = get_possible_roles(candidates)
    results = []
    # Перебираем только возможных мидлов
    for mids in itertools.combinations(possible_mids, 2):
        mid_avg = sum(candidates[m] for m in mids) / 2
        if mid_avg < MIN_MID_AVG:
            continue  # Отсеиваем неподходящие пары мидлов
        # Оставшиеся кандидаты (кроме выбранных мидлов)
        remaining = [cid for cid in possible_juns if cid not in mids]
        # Перебираем только возможных джунов
        for juns in itertools.combinations(remaining, 2):
            jun_avg = sum(candidates[j] for j in juns) / 2
            if jun_avg >= MIN_JUN_AVG:
                results.append((mids, juns))
    return results
# Замер времени
start_time = timeit.default_timer()
opt_result = optimized_search(candidates)
opt_time = timeit.default_timer() - start_time
# Находим оптимальную команду
if opt_result:
    optimal_team = max(opt_result, key=team_score)
    optimal_score = team_score(optimal_team)
# Вывод результатов
print(" Оптимизированный подход (с предварительной фильтрацией кандидатов)")
print(f"Найдено вариантов: {len(opt_result)}")
print(f"Время выполнения: {opt_time:.6f} сек\n")
print(" Оптимальная команда:")
print(
    f"Мидлы: {optimal_team[0]} (уровни: {[candidates[m] for m in optimal_team[0]]}, средний: {sum(candidates[m] for m in optimal_team[0]) / 2:.1f})")
print(
    f"Джуны: {optimal_team[1]} (уровни: {[candidates[j] for j in optimal_team[1]]}, средний: {sum(candidates[j] for j in optimal_team[1]) / 2:.1f})")
print(f"Общий уровень команды: {optimal_score}")
print(f"Средний уровень: {optimal_score / 4:.2f}\n")
print(" Все подходящие варианты:")
for idx, (mids, juns) in enumerate(opt_result, 1):
    score = team_score((mids, juns))
    print(
        f"{idx}. Мидлы: {mids} (ср. {sum(candidates[m] for m in mids) / 2:.1f}), Джуны: {juns} (ср. {sum(candidates[j] for j in juns) / 2:.1f}), Общий: {score}")
