digit_words = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}

def num2words(num):
    return ' '.join(digit_words[int(d)] for d in str(num)) if num != 0 else 'ноль'

def transform_even_number(word):
    return ''.join([word[i+1] + word[i] for i in range(0, len(word)-1, 2)]) + (word[-1] if len(word) % 2 else '')
k = int(input('Введите количество нулей:'))
fl = 0
A,B=[],[]
with open('input.txt', 'r') as f:
    words = f.read().split()
    for word in words:
        if word.isdigit():
            num = int(word)
            if num % 2 != 0 and len(word) > 3:
                A.append(num)
            if int(word)%2==0:
                transformed = transform_even_number(word)
                if fl>0 or '0'*k in transformed:
                    B.append(num2words(int(word)))
                    fl+=1
                if fl==0:
                    B.append(transformed)
    print(f"1-ый список: {A}\n2-ой список: {B}")
