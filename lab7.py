import tkinter as tk
from tkinter import scrolledtext
from itertools import combinations

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

def generate_combinations():
    N = int(input_n.get())
    K = int(input_k.get())

    all_combinations = generate_gift_sets_optimized(N, K)

    # Вывод результатов
    text_area.delete('1.0', tk.END)  # Очистка поля вывода перед вставкой нового текста
    if not all_combinations:
        text_area.insert(tk.END, "К сожалению, комбинаций, удовлетворяющих условиям, не существует.")
    else:
        for i, gift_set in enumerate(all_combinations):
            text_area.insert(tk.END, f"{i + 1}. {' '.join(gift_set)}\n")

    # Расчет и вывод оптимального решения
    optimal_solution = target_function(all_combinations)
    additional_info_area.delete("1.0", tk.END)
    additional_info_area.insert(tk.END,
                                "Оптимальное решение (количество возможных комбинатов): %s" % optimal_solution)

def additional_info():
    additional_info_text = additional_info_area.get('1.0', tk.END).strip()
    if additional_info_text:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, additional_info_text)

# Создание окна приложения
window = tk.Tk()
window.title("Генератор комбинаций покупки открыток")
window.geometry("500x500")

# Создание элементов ввода
label_n = tk.Label(text="Введите количество открыток, которые нужно купить (N):")
label_n.grid(row=0, column=0)
input_n = tk.Entry()
input_n.grid(row=0, column=1, padx=5, pady=5)

label_k = tk.Label(text="Введите общее количество видов открыток (K):")
label_k.grid(row=1, column=0)
input_k = tk.Entry()
input_k.grid(row=1, column=1, padx=5, pady=5)

# Создание кнопки
button_generate = tk.Button(text="Сгенерировать", command=generate_combinations)
button_generate.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


# Создание метки после кнопки
result_label = tk.Label(text=f"Все возможные комбинации покупки")
result_label.grid(row=6, column=0, sticky="nsew")

# Создание поля вывода с вертикальной полосой прокрутки
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
text_area.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Метка с дополнительной информацией
additional_info_label = tk.Label(text="Оптимальное решение (количество возможных комбинаций)")
additional_info_label.grid(row=8, column=0, sticky="nsew")

# Поле ввода для дополнительной информации
additional_info_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=5)
additional_info_area.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Размещение окна в центре экрана
window.geometry(f"+{(window.winfo_screenwidth() - 200) // 2}+{(window.winfo_screenheight() - 200) // 2}")
window.mainloop()

# Запуск основного цикла приложения
window.mainloop()
