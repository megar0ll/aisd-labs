import re
d = {0:'ноль',1:'один',2:'два',3:'три',4:'четыре',5:'пять',6:'шесть',7:'семь',8:'восемь',9:'девять'}
k = 3
text = open('input.txt').read()
A = [int(w) for w in re.findall(r'\d{4,}', text) if int(w)%2]
nums = re.findall(r'\d+', text)
B, f = [], False
for w in nums:
    if int(w)%2 == 0:
        t = re.sub(r'(\d)(\d)', r'\2\1', w[:-1]) + w[-1]*(len(w)%2)
        if f or re.search(f'0{{{k}}}', t): B.append(' '.join(d[int(c)] for c in w)); f = True
        else: B.append(t)
print(f"1:{A}\n2:{B}")
