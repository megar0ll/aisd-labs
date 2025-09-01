import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import math
import os
class TradeDeal:
    def __init__(self, deal_id, product, seller, amount, price):
        self.deal_id = deal_id
        self.product = product
        self.seller = seller
        self.amount = amount
        self.price = price
    def total_cost(self):
        return self.amount * self.price
    def __str__(self):
        return f"Сделка {self.deal_id}: {self.amount} x {self.product} @ {self.price} (Продавец: {self.seller})"
class TradeDealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление торговыми сделками")
        self.deals = []
        # Создаем вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        # Вкладка для добавления сделок
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Добавить сделку")
        self.setup_add_tab()
        # Вкладка для просмотра сделок
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="Просмотр сделок")
        self.setup_view_tab()
        # Вкладка для текстовой сегментации
        self.segmentation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.segmentation_tab, text="Текстовая сегментация")
        self.setup_segmentation_tab()
        # Вкладка для визуализации
        self.visualization_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.visualization_tab, text="Визуализация")
        self.setup_visualization_tab()
        # Загружаем сделки при запуске
        self.load_deals()
    def setup_add_tab(self):
        # Поля для ввода данных
        ttk.Label(self.add_tab, text="ID сделки:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.deal_id_entry = ttk.Entry(self.add_tab)
        self.deal_id_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.add_tab, text="Товар:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_entry = ttk.Entry(self.add_tab)
        self.product_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.add_tab, text="Продавец:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.seller_entry = ttk.Entry(self.add_tab)
        self.seller_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.add_tab, text="Количество:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(self.add_tab, text="Цена за единицу:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.price_entry = ttk.Entry(self.add_tab)
        self.price_entry.grid(row=4, column=1, padx=5, pady=5)
        # Кнопки
        self.add_button = ttk.Button(self.add_tab, text="Добавить сделку", command=self.add_deal)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.load_button = ttk.Button(self.add_tab, text="Загрузить из файла", command=self.load_from_file)
        self.load_button.grid(row=6, column=0, pady=10, padx=5)
        self.save_button = ttk.Button(self.add_tab, text="Сохранить в файл", command=self.save_to_file)
        self.save_button.grid(row=6, column=1, pady=10, padx=5)
    def setup_view_tab(self):
        # Таблица для отображения сделок
        columns = ("ID", "Товар", "Продавец", "Количество", "Цена", "Сумма")
        self.deals_tree = ttk.Treeview(self.view_tab, columns=columns, show="headings")
        for col in columns:
            self.deals_tree.heading(col, text=col)
            self.deals_tree.column(col, width=100, anchor=tk.CENTER)
        self.deals_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Кнопка обновления
        self.refresh_button = ttk.Button(self.view_tab, text="Обновить", command=self.refresh_deals_view)
        self.refresh_button.pack(pady=5)
    def setup_segmentation_tab(self):
        # Фрейм для выбора типа сегментации
        segmentation_frame = ttk.LabelFrame(self.segmentation_tab, text="Тип сегментации")
        segmentation_frame.pack(fill=tk.X, padx=5, pady=5)
        self.segmentation_type = tk.StringVar(value="products")
        ttk.Radiobutton(segmentation_frame, text="По товарам", variable=self.segmentation_type,
                        value="products").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(segmentation_frame, text="По продавцам", variable=self.segmentation_type,
                        value="sellers").pack(side=tk.LEFT, padx=5)
        # Кнопка выполнения сегментации
        self.segment_button = ttk.Button(segmentation_frame, text="Выполнить сегментацию",
                                         command=self.show_text_segmentation)
        self.segment_button.pack(side=tk.LEFT, padx=5)
        # Текстовое поле для отображения результатов
        self.segmentation_text = tk.Text(self.segmentation_tab, wrap=tk.WORD, height=15)
        self.segmentation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self.segmentation_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.segmentation_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.segmentation_text.yview)
    def setup_visualization_tab(self):
        # Фрейм для выбора типа визуализации
        vis_frame = ttk.LabelFrame(self.visualization_tab, text="Тип визуализации")
        vis_frame.pack(fill=tk.X, padx=5, pady=5)
        self.vis_type = tk.StringVar(value="products")

        ttk.Radiobutton(vis_frame, text="По товарам", variable=self.vis_type,
                        value="products").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(vis_frame, text="По продавцам", variable=self.vis_type,
                        value="sellers").pack(side=tk.LEFT, padx=5)
        # Кнопка выполнения визуализации
        self.visualize_button = ttk.Button(vis_frame, text="Построить диаграмму",
                                           command=self.show_visualization)
        self.visualize_button.pack(side=tk.LEFT, padx=5)
        # Холст для круговой диаграммы
        self.canvas = tk.Canvas(self.visualization_tab, width=500, height=400, bg='white')
        self.canvas.pack(pady=10)
    def show_text_segmentation(self):
        if not self.deals:
            messagebox.showwarning("Предупреждение", "Нет данных для сегментации")
            return
        segmentation_type = self.segmentation_type.get()
        if segmentation_type == "products":
            segments = self.segment_by_products()
            title = "Сегментация по товарам:\n\n"
        else:
            segments = self.segment_by_sellers()
            title = "Сегментация по продавцам:\n\n"
        # Формируем текст для отображения
        result_text = title
        total = sum(item[1] for item in segments)

        for item in segments:
            percent = (item[1] / total) * 100
            result_text += f"{item[0]}: {item[1]} сделок ({percent:.2f}%)\n"
        # Отображаем в текстовом поле
        self.segmentation_text.delete(1.0, tk.END)
        self.segmentation_text.insert(tk.END, result_text)
    def show_visualization(self):
        if not self.deals:
            messagebox.showwarning("Предупреждение", "Нет данных для визуализации")
            return
        vis_type = self.vis_type.get()
        if vis_type == "products":
            segments = self.segment_by_products()
            title = "Распределение по товарам"
        else:
            segments = self.segment_by_sellers()
            title = "Распределение по продавцам"
        self.draw_pie_chart(segments, title)
    def add_deal(self):
        try:
            deal_id = self.deal_id_entry.get()
            product = self.product_entry.get()
            seller = self.seller_entry.get()
            amount = int(self.amount_entry.get())
            price = float(self.price_entry.get())
            if not deal_id or not product or not seller:
                raise ValueError("Все текстовые поля должны быть заполнены")
            if amount <= 0 or price <= 0:
                raise ValueError("Количество и цена должны быть положительными числами")
            new_deal = TradeDeal(deal_id, product, seller, amount, price)
            self.deals.append(new_deal)
            # Очищаем поля ввода
            self.deal_id_entry.delete(0, tk.END)
            self.product_entry.delete(0, tk.END)
            self.seller_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            messagebox.showinfo("Успех", "Сделка успешно добавлена")
            self.refresh_deals_view()
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
    def refresh_deals_view(self):
        # Очищаем текущие данные
        for item in self.deals_tree.get_children():
            self.deals_tree.delete(item)
        # Добавляем новые данные
        for deal in self.deals:
            self.deals_tree.insert("", tk.END, values=(
                deal.deal_id,
                deal.product,
                deal.seller,
                deal.amount,
                f"{deal.price:.2f}",
                f"{deal.total_cost():.2f}"
            ))
    def segment_by_products(self):
        products = {}
        for deal in self.deals:
            if deal.product in products:
                products[deal.product] += 1
            else:
                products[deal.product] = 1
        # Сортируем по убыванию количества
        return sorted(products.items(), key=lambda x: x[1], reverse=True)
    def segment_by_sellers(self):
        sellers = {}
        for deal in self.deals:
            if deal.seller in sellers:
                sellers[deal.seller] += 1
            else:
                sellers[deal.seller] = 1
        # Сортируем по убыванию количества
        return sorted(sellers.items(), key=lambda x: x[1], reverse=True)
    def draw_pie_chart(self, segments, title):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = min(center_x, center_y) - 20
        # Рисуем заголовок
        self.canvas.create_text(center_x, 20, text=title, font=('Arial', 12, 'bold'))
        # Если нет данных
        if not segments:
            self.canvas.create_text(center_x, center_y, text="Нет данных для отображения")
            return
        # Вычисляем общее количество для нормализации
        total = sum(item[1] for item in segments)
        # Генерируем цвета
        colors = self.generate_colors(len(segments))
        # Рисуем сектора
        start_angle = 0
        for i, (label, count) in enumerate(segments):
            angle = 360 * (count / total)
            # Рисуем сектор
            self.canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle,
                fill=colors[i], outline='black'
            )
            # Вычисляем позицию для метки
            mid_angle = start_angle + angle / 2
            label_radius = radius * 0.7
            label_x = center_x + label_radius * math.cos(math.radians(mid_angle))
            label_y = center_y - label_radius * math.sin(math.radians(mid_angle))
            # Рисуем метку с процентом
            percent = (count / total) * 100
            self.canvas.create_text(
                label_x, label_y,
                text=f"{percent:.1f}%",
                font=('Arial', 8, 'bold')
            )
            # Рисуем легенду
            legend_x = 20
            legend_y = 40 + i * 20
            self.canvas.create_rectangle(
                legend_x, legend_y,
                legend_x + 15, legend_y + 15,
                fill=colors[i], outline='black'
            )
            self.canvas.create_text(
                legend_x + 30, legend_y + 8,
                text=f"{label} ({count})",
                anchor=tk.W,
                font=('Arial', 9)
            )
            start_angle += angle
    def generate_colors(self, n):
        # Генерируем n различных цветов
        colors = []
        hue_step = 360 / n
        for i in range(n):
            hue = i * hue_step
            # Преобразуем HSV в HEX (Hue, Saturation=80%, Value=90%)
            rgb = self.hsv_to_rgb(hue, 0.8, 0.9)
            hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
            colors.append(hex_color)
        return colors
    def hsv_to_rgb(self, h, s, v):
        # Конвертация HSV в RGB
        h = h / 360.0
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        if i % 6 == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

        return (int(r * 255), int(g * 255), int(b * 255))
    def load_deals(self):
        # Попытка загрузить сделки из файла по умолчанию
        default_file = "deals.csv"
        if os.path.exists(default_file):
            try:
                with open(default_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.deals = []
                    for row in reader:
                        if len(row) == 5:
                            deal_id, product, seller = row[0], row[1], row[2]
                            try:
                                amount = int(row[3])
                                price = float(row[4])
                                self.deals.append(TradeDeal(deal_id, product, seller, amount, price))
                            except ValueError:
                                continue
                self.refresh_deals_view()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    def save_to_file(self):
        if not self.deals:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")],
            title="Сохранить сделки в файл"
        )
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    for deal in self.deals:
                        writer.writerow([deal.deal_id, deal.product, deal.seller, deal.amount, deal.price])
                messagebox.showinfo("Успех", f"Сделки успешно сохранены в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    def load_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")],
            title="Выберите файл с данными о сделках"
        )
        if file_path:
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.deals = []
                    for row in reader:
                        if len(row) == 5:
                            deal_id, product, seller = row[0], row[1], row[2]
                            try:
                                amount = int(row[3])
                                price = float(row[4])
                                self.deals.append(TradeDeal(deal_id, product, seller, amount, price))
                            except ValueError:
                                continue
                self.refresh_deals_view()
                messagebox.showinfo("Успех", f"Данные успешно загружены из {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
if __name__ == "__main__":
    root = tk.Tk()
    app = TradeDealApp(root)
    root.geometry("800x600")
    root.mainloop()