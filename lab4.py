import numpy, matplotlib, random
count_polozh, count_otric,k,n=0,0,int(input("Введите k:")), int(input("Введите n:"))
A=numpy.eye(n)
for i in range(n):
    for j in range(n):
        A[i][j]=random.randint(-10,10)
print("Матрица А:", A)
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
print("Матрица F:", F)
C=numpy.linalg.inv(A)
if round(numpy.linalg.det(A))>numpy.trace(F):
    VIR = numpy.subtract(numpy.dot(A,A.T),  k * numpy.dot(F, C))
    print(f"Транспонированная матрица A:{A.T}\nМатрица, обратная A:{C}\nМатрица A, умноженная на свою транспонированную версию:{numpy.dot(A, A.T)}\nМатрица F, умноженная на матрицу, обратную A {numpy.dot(F, C)}\nМатрица k*F*invA{k*numpy.dot(F, C)}\n Результат вычислений:{VIR}")
else:
    G=numpy.tril(A)
    VIR = k*(numpy.subtract(numpy.add(k*C, G), F.T))
    print(f"Транспонированная матрица F:{F.T}\nНижняя треугольная матрица G:{G}\nМатрица, обратная A:{C}\nМатрица k*invA:{k*C}\nМатрица k*invA+G:{numpy.add(k*C, G)}\nМатрица k*invA+G-F.T:{numpy.subtract(numpy.add(k*C, G),F.T)}\nРезультат вычислений:{VIR}")





