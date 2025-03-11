import random,copy
k,n=int(input("Введите число k: ")),int(input("Введите число n: "))
KON,UMN,Fk,A,A_B,G,x,count_polozh,count_otric=[],[],[],[],[],0,n,0,0
for i in range(n):
    A.append([0]*n), A_B.append([0]*n), Fk.append([0]*n), UMN.append([0]*n), KON.append([0]*n)
for i in range(n):
    for j in range(n):
        A[i][j]=random.randint(-10,10)
print("Матрица А: ",A)
F = copy.deepcopy(A)
AT=[[0 for j in range(len(A))]for i in range(len(A[0]))]
for i in range(len(AT)):
    for j in range(len(AT)):
        AT[j][i]=A[i][j]
print("Транспонированная матрица А: ", AT)
e=n-1
for i in range(n):
    for j in range(n):
        if i>j and j>e and (j+1)%2==0 and F[i][j]>0:
            count_polozh+=1
    e-=1
e=n-1
for i in range(n):
    for j in range(n):
        if i<j and j<e and (j+1)%2!=0 and F[i][j]<0:
            count_otric+=1
    e-=1
e=n-1
if count_polozh>count_otric:
    for i in range(n):
        for j in range(n):
            if i>j and j>e:
                G = F[j][i]
                F[j][i] = F[i][j]
                F[i][j] = G
        e-=1
else:
    for i in range(n):
        for j in range(n):
            if i < j and j < e:
                G=F[i][j]
                F[i][j]=F[x-1-j][i]
                F[x-1-j][i]=G
        e-=1
print("Матрица F: ",F)
for i in range(len(AT)):
    for j in range(len(AT)):
        A_B[i][j] = (A[i][j] + F[i][j])
        Fk[i][j] = F[i][j] * k
        for m in range(len(AT)):
            UMN[i][j] += A_B[i][m]*AT[m][j]
        KON[i][j]=UMN[i][j]-Fk[i][j]
print(f"Матрица, равная сумме матриц F и A: {A_B}\nМатрица (F+A)*AT: {UMN}\nМатрица, равная произведению матрицы F и числа {k}: {Fk}\nРезультат: {KON}")