# ЛАБ1-Написать программу, которая читая символы из бесконечной последовательности (эмулируется конечным файлом, читающимся поблочно), распознает, преобразует и выводит на экран лексемы по определенному правилу. Лексемы разделены пробелами. Преобразование делать по возможности через словарь. Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа. Регулярные выражения использовать нельзя. Натуральные нечетные числа, превышающие 3 цифры. Отдельно выводит на экран четные числа, меняя в них местами каждые две соседние цифры пока не встретит число из К подряд идущих нулей. После чего вывод идет без смены и прописью.
# ЛАБ2-Написать программу, решающую задачу из 1 лабораторной работы (в соответствии со своим вариантом) со следующими изменениями:
1.	Входной файл является обыкновенным (т.е. нет требования на «бесконечность» файла);
2.	Распознавание и обработку делать  через регулярные выражения;
3.	В вариантах, где есть параметр (например К), допускается его заменить на любое число(константу);
4.	Все остальные требования соответствуют варианту задания лабораторной работы №1.
#ЛАБ3-С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N) заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное заполнение, а целенаправленное, введенное из файла или полученное генератором. Условно матрица разделена на 4 части:
Для ИСТд-13
  4
3   1
  2
Библиотечными методами (NumPy) пользоваться нельзя.
2.	Формируется матрица F следующим образом: Скопировать в нее матрицу А и если количество положительных элементов в четных столбцах в области 2 больше, чем количество отрицательных  элементов в нечетных столбцах в области 4, то поменять симметрично области 1 и 2 местами, иначе  поменять местами области 3 и 4 местами несимметрично. При этом матрица А не меняется. После чего вычисляется выражение: (F+A)*AT – K * F. На печать выводятся по мере формирования А, F и все матричные операции последовательно.
#ЛАБ4-С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10]. Для отладки использовать не случайное заполнение, а целенаправленное (ввод из файла и генератором). Вид матрицы А: 
Для ИСТд-13
D	Е
С	В
На основе матрицы А формируется матрица F. По матрице F необходимо вывести не менее 3 разных графика. Программа должна использовать функции библиотек numpy  и matplotlib
Формируется матрица F следующим образом: скопировать в нее А и если в С количество положительных элементов в четных столбцах, чем количество отрицательных  элементов в нечетных столбцах, то поменять местами С и В симметрично, иначе С и Е поменять местами несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F, то вычисляется выражение: A*AT – K * F*A-1, иначе вычисляется выражение (К*A-1 +G-FТ)*K, где G-нижняя треугольная матрица, полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно.
