import math

import DataReader as dr
import numpy as np
import scipy.stats.distributions as sps
import scipy.special as spec


def main():
    """
    Вариант 7
    Коробов А.А. 09-821
    """
    Task_1()
    print('__________________________________________________________________________________________________________')
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
        print('(Нулевая гипотеза принимается. Так как M <= ', c_crit, ')', sep='')

    p_value = 1 - Fbin(M, len(data))
    print('P-значение:', p_value)


def Task_2():
    """

    :return:
    """
    print('Task_2')
    data = np.sort(dr.rf_task_2('Data/Data3_txt.txt'))

    r = 8
    intervals = np.linspace(data[0], data[-1], r + 1)
    intervals[0] = float('-inf')
    intervals[-1] = float('inf')

    v = []
    for i in range(r):
        num = 0
        for j in data:
            if intervals[i] <= j < intervals[i + 1]:
                num += 1
        v.append(num)
    x_mean = np.mean(data)
    x_var = np.var(data) ** 0.5

    def F(x):
        return (1 + spec.erf(x / (2 ** 0.5))) / 2

    p = [F((intervals[1] - x_mean) / x_var)]
    for i in range(2, len(intervals) - 1):
        p.append(F((intervals[i] - x_mean) / x_var) - F((intervals[i - 1] - x_mean) / x_var))
    p.append(1 - F((intervals[-2] - x_mean) / x_var))

    T = sum([(v[k] - len(data) * p[k]) ** 2 / (len(data) * p[k]) for k in range(r)])

    alf = 0.01
    c_crit = sps.chi2.ppf(1 - alf, r - 1)
    print('Критическая константа:', c_crit)
    print('Вид критической области: ', 'A = { T: T > ', c_crit, '}', sep='')

    print('Статистика критерия хи-квадрат:', T)
    if alf < 1 - sps.chi2.cdf(T, r - 3):
        p_value = 1 - sps.chi2.cdf(T, r - 3)
        print('(Нулевая гипотиза принимается. Так как p_r-3 > alf:', p_value, '>', alf)
    elif alf > 1 - sps.chi2.cdf(T, r - 1):
        p_value = 1 - sps.chi2.cdf(T, r - 1)
        print('(Нулевая гипотиза отвергается. Так как p_r-1 < alf:', p_value, '<', alf)

    print('P-значение:', p_value)


if __name__ == '__main__':
    main()
