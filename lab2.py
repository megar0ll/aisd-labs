import re
K = 3
F = 0
digit_words = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}
A=[]
B=[]
def num2words(num):
    return ' '.join(digit_words[int(d)] for d in str(num)) if num != 0 else 'ноль'

def transform_even_number(word):
    return ''.join([word[i + 1] + word[i] for i in range(0, len(word) - 1, 2)]) + (word[-1] if len(word) % 2 else '')
def process_numbers(text, F):
    number_pattern = re.compile(r'\b\d+\b')
    zero_pattern = re.compile(r'0' * K)
    for match in number_pattern.finditer(text):
        word = match.group()
        if word.isdigit():
            if int(word) % 2 != 0 and len(word) > 3:
                A.append(int(word))
            if int(word) % 2 == 0:
                transformed = transform_even_number(word)
                if F>0 or zero_pattern.search(transformed):
                    F += 1
                    B.append(num2words(int(word)))
                if F==0:
                    B.append(transformed)
    print(f"Первый список: {A}\nВторой список: {B}")
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    process_numbers(text, F)


