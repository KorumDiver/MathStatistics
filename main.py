import DataReader as dr
import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Вариант 7
    Коробов А.А. 09-821
    """
    Task_1()
    print()
    Task_2()


def Task_1():
    """
    Критерий знаков (Вариант 3)

    Событие А состоит в уменьшений показателя
    H0: p = 0.5 - нудевая гипотеза. Событие происходит с одинаковой частотой
    H1: p > 0.5 - уменьшился показатель (Событие А происходит чаще противоположного)

    Статистика критерия знака M = sum(Xi) ~ Fbin(n, p)



    1. Выборки одинакового объема. Каждая пара i-х наблюдений у одного и того же i-го объекта
    2. Вид критической области: A = { M: M > 23}
       Критическая константа: 23
    3. Значение статистики критерия зкаков: 32 (Нулевая гипотеза отвергается)
    4. p-значение = 2.0372681319713593e-09
    """

    def search_c_crit(n, alf, p0=0.5):
        """
        Находит критическую константу
        :param n: Чило элементов в выборке
        :param alf: Уровень значисости
        :param p0: Заданный уровень (В даннос члучае это вероятность того что события равновероятны)
        :return: Критическая константа
        """
        sum_f_bin = C(n, 0) * (p0 ** 0) * ((1 - p0) ** (n - 0))
        for c in range(n):
            new_val = C(n, c + 1) * (p0 ** c) * ((1 - p0) ** (n - c))
            sum_f_bin = sum((sum_f_bin, new_val))
            if sum_f_bin >= 1 - alf:
                return c

    def Fbin(M, n, p0=0.5):
        sum_f_bin = C(n, 0) * (p0 ** 0) * ((1 - p0) ** (n - 0))
        for c in range(M):
            new_val = C(n, c + 1) * (p0 ** c) * ((1 - p0) ** (n - c))
            sum_f_bin = sum((sum_f_bin, new_val))

        return sum_f_bin

    def C(n, k):
        """
        Находит число сочитаний из n по k
        """
        if 0 <= k <= n:
            nn = 1
            kk = 1
            for t in range(1, min(k, n - k) + 1):
                nn *= n
                kk *= t
                n -= 1
            return nn // kk
        else:
            return 0

    print('Task_1')

    # Получаем набор единиц и нулей удоволетворяющих тому что x > y. Те показатель уменьшился
    data = dr.rf_task_1('Data/Data1_txt.txt')

    n = len(data)  # Количесто элементов в выборке
    alf = 0.01  # Уровень значисости
    c_crit = search_c_crit(n, alf)  # Критическая константа
    print('Критическая константа:', c_crit)
    print('Вид критической области: ', 'A = { M: M > ', c_crit, '}', sep='')

    M = sum(data)  # Статистика критерия знаков
    print('Значение статистики критерия зкаков: ', M, sep='')
    if M > c_crit:
        print('(Нулевая гипотиза отвергается. Так как M > ', c_crit, ')', sep='')
    else:
        print('(Нулевая гипотеза принимается. Так как M > ', c_crit, ')', sep='')

    p_value = 1 - Fbin(M, len(data))
    print('P-значение:', p_value)
    print('___________________________________________________________________________________________________________')


def Task_2():
    """

    :return:
    """
    print('Task_2')
    value = np.sort(dr.rf_task_2('Data/Data2_txt.txt'))
    print(value)


if __name__ == '__main__':
    main()
