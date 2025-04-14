import numpy, matplotlib.pyplot as plt, random
count_polozh, count_otric,k,n=0,0,int(input("Введите k:")), int(input("Введите n:"))
def reader(filename):
    with open(filename,'r') as file:
        return [list(map(int,line.split())) for line in file]
A=reader("matrix3.txt")
A=numpy.copy(A)
print("Матрица А:\n", A)
F=numpy.copy(A)
if n%2==0:
    r=n//2
    for i in range(r, n, 1):
        for j in range(r):
            if F[i][j] > 0 and (j + 1) % 2 == 0:
                count_polozh += 1
            if F[i][j] < 0 and (j+1)%2!=0:
                count_otric += 1
else:
    r=((n-1)//2)+1
    for i in range(r, n, 1):
        for j in range(r-1):
            if F[i][j]>0 and (j+1)%2==0:
                count_polozh += 1
            if F[i][j] < 0 and (j+1)%2!=0:
                count_otric += 1
if count_polozh>count_otric:
    for i in range(r,n,1):
        x=n-1
        if n%2==0:
            for j in range(r):
                F[i][j],F[i][x]=F[i][x],F[i][j]
                x-=1
        else:
            for j in range(r-1):
                F[i][j], F[i][x] = F[i][x], F[i][j]
                x -= 1
else:
    for i in range(r,n,1):
        if n%2==0:
            for j in range(r):
                F[i][j],F[i-r][j+r]=F[i-r][j+r],F[i][j]
        else:
            for j in range(r-1):
                F[i][j],F[i - r][j + r] = F[i - r][j + r],F[i][j]
print("Матрица F:\n", F)
C, G=numpy.linalg.inv(A), numpy.tril(A)
if round(numpy.linalg.det(A))>numpy.trace(F):
    VIR = numpy.subtract(numpy.dot(A, A.T),  k * numpy.dot(F, C))
    print(f"Транспонированная матрица A:\n{A.T}\nМатрица, обратная A:\n{C}\nМатрица A, умноженная на свою транспонированную версию:\n{numpy.dot(A, A.T)}\nМатрица F, умноженная на матрицу, обратную A:\n{numpy.dot(F, C)}\nМатрица k*F*invA:\n{k*numpy.dot(F, C)}\n Результат вычислений:\n{VIR}")
else:
    VIR = k*(numpy.subtract(numpy.add(k*C, G), F.T))
    print(f"Транспонированная матрица F:\n{F.T}\nНижняя треугольная матрица G:\n{G}\nМатрица, обратная A:\n{C}\nМатрица k*invA:\n{k*C}\nМатрица k*invA+G:\n{numpy.add(k*C, G)}\nМатрица k*invA+G-F.T:\n{numpy.subtract(numpy.add(k*C, G),F.T)}\nРезультат вычислений:\n{VIR}")
plt.figure(figsize=(15, 5))
# 1. Тепловая карта матрицы F
plt.subplot(131)
plt.imshow(F, cmap='winter', interpolation='nearest')
plt.colorbar()
plt.title("Тепловая карта F")
# 2. График суммы по строкам (линейный)
plt.subplot(132)
plt.plot(F.sum(axis=1), 'o-', color='cyan')
plt.title("Сумма по строкам")
plt.grid(True)
# 3. Столбчатая диаграмма суммы по столбцам (вместо линейного)
plt.subplot(133)
plt.bar(range(F.shape[1]), F.sum(axis=0), color='cyan', alpha=0.6)
plt.title("Сумма по столбцам (bar)")
plt.grid(True)
plt.tight_layout()
plt.show()
