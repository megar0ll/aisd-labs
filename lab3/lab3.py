import random,copy
def reader(filename):
    with open(filename,'r') as file:
        return [list(map(int,line.split())) for line in file]
k,n=int(input("Введите число k: ")),int(input("Введите число n: "))
KON,UMN,Fk,A,A_B,G,x,count_polozh,count_otric=[],[],[],[],[],0,n,0,0
for i in range(n):
    A.append([0]*n), A_B.append([0]*n), Fk.append([0]*n), UMN.append([0]*n), KON.append([0]*n)
A=reader('matrix.txt')
print("Матрица А: ")
for i in range(n):
    print(f"{A[i]}")
F = copy.deepcopy(A)
AT=[[0 for j in range(len(A))]for i in range(len(A[0]))]
for i in range(len(AT)):
    for j in range(len(AT)):
        AT[j][i]=A[i][j]
print("Транспонированная матрица А: ")
for i in range(n):
    print(f"{AT[i]}")
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
                F[i][j], F[j][i] = F[j][i], F[i][j]
        e-=1
else:
    for i in range(n):
        for j in range(n):
            if i < j and j < e:
                F[i][j], F[x-1-j][i]=F[x-1-j][i], F[i][j]
        e-=1
print("Матрица F: ")
for i in range(n):
    print(f"{F[i]}")
for i in range(len(AT)):
    for j in range(len(AT)):
        A_B[i][j] = (A[i][j] + F[i][j])
        Fk[i][j] = F[i][j] * k
        for m in range(len(AT)):
            UMN[i][j] += A_B[i][m]*AT[m][j]
        KON[i][j]=UMN[i][j]-Fk[i][j]
print("Матрица, равная сумме матриц F и A:")
for i in range(n):
    print(f"{A_B[i]}")
print("Матрица (F+A)*AT:")
for i in range(n):
    print(f"{UMN[i]}")
print(f"Матрица, равная произведению матрицы F и числа {k}:")
for i in range(n):
    print(f"{Fk[i]}")
print("Результат:")
for i in range(n):
    print(f"{KON[i]}")
