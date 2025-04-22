import timeit
import matplotlib.pyplot as plt
def recurs(n):
    def F(n):
        if n==1:
            return 1
        elif n>=2:
            return (-1)**n*(F(n-1)+G(n-1))
        else:
            return 0
    def G(n):
        if n==1:
            return 1
        elif n>=2:
            return F(n-1) + 2*G(n-1)
        else:
            return 0
    return F(n), G(n)
def iterat(n):
    if n==1:
        return 1
    Fi,Gi=[1]*2,[1]*2
    for i in range(2, n + 1):
        f=(-1)**i*(Fi[i-1]+Gi[i-1])
        g=Fi[i-1] + 2*Gi[i-1]
        Fi.append(f),Gi.append(g)
    return Fi[i],Gi[i]
for n in range(2, 11):
    Fi, Gi = [0] * (n + 1), [0] * (n + 1)
    print(f"n = {n}")
    result_rec = recurs(n)
    result_iter = iterat(n)
    print(f"Рекурсивное значение: {result_rec}")
    print(f"Итеративное значение: {result_iter}")
n_values = list(range(2, 25))
rec_times = []
iter_times = []
for n in n_values:
    time_rec = timeit.timeit(lambda: recurs(n), number=1)
    rec_times.append(time_rec)
    time_iter = timeit.timeit(lambda: iterat(n), number=1)
    iter_times.append(time_iter)
print("n\t| Рекурсивное время (сек)\t| Итеративное время (сек)")
print("-" * 50)
for i in range(len(n_values)):
    print(f"{n_values[i]}\t| {rec_times[i]:.6f}\t\t\t| {iter_times[i]:.6f}")
plt.figure(figsize=(12, 6))
plt.plot(n_values, rec_times, label='Рекурсивное время (сек)', marker='o')
plt.plot(n_values, iter_times, label='Итеративное время (сек)', marker='x')
plt.xlabel('n')
plt.ylabel('Время (сек)')
plt.title('Сравнение времени выполнения рекурсивной и итеративной функций')
plt.legend()
plt.grid(True)
plt.show()
