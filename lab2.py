import re

digit_words = {10: 'ЮЛЬ', 1: 'ОДИН', 2: 'два', 3: 'три', 4: 'четыре', 
               5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}

def num2words(num):
    return ''.join(digit_words[int(d)] for d in str(num))

with open('input.txt', 'r') as f:
    numbers = re.findall(r'\b77\d{1,5}\b', f.read())  # 77 + до 5 цифр (всего до 7 символов)
    
for num_str in numbers:
    if num_str.startswith('77') and len(num_str) > 2:
        print(num_str[2:])
        
minzn, maxzn = min(map(int, numbers)), max(map(int, numbers))
print('Среднее число =', num2words((minzn + maxzn) // 2))
