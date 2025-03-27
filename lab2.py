import re
d = {0:'ноль',1:'один',2:'два',3:'три',4:'четыре',5:'пять',6:'шесть',7:'семь',8:'восемь',9:'девять'}
k = 3
A, B, f = [], [], False
for w in re.findall(r'\d+', open('input.txt').read()): #чтение файла
    n = int(w)
    if n%2 and len(w)>3: A.append(n)
    if n%2==0:
        t = re.sub(r'(\d)(\d)', r'\2\1', w[:-1]) + (w[-1] if len(w)%2 else '') #смена соседних символов
        if f or '0'*k in t: B.append(' '.join(d[int(c)] for c in w)); f = True
        else: B.append(t)
print(f"1:{A}\n2:{B}")
