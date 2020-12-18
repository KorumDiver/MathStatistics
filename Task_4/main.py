import numpy as np
import matplotlib.pyplot as plt
import Task_4.read_task as read
import scipy.stats as stats


def main():
    task_1()
    print()
    task_2()


def task_1():
    data = read.read("Data/r4z1.csv")
    n = len(data)

    alf = 0.1
    r = 6  # Интервалов r+1
    s = 4  # интервалов s+1
    v = r*s
    x_1, x_r = 115.05, 123.05
    y_1, y_s = 80.05, 86.05

    # С критическая
    c_critical = stats.chi2.ppf(1 - alf, v)

    # Создание таблицы сопряженности

    # Для компонеты x
    x_partition = [[float("-inf"), x_1]]
    x_p = np.linspace(x_1, x_r, r)
    [x_partition.append([x_p[i], x_p[i + 1]]) for i in range(len(x_p) - 1)]
    x_partition.append([x_r, float("inf")])
    # Для компоненты y
    y_partition = [[float("-inf"), y_1]]
    y_p = np.linspace(y_1, y_s, s)
    [y_partition.append([y_p[i], y_p[i + 1]]) for i in range(len(y_p) - 1)]
    y_partition.append([y_s, float("inf")])

    tab = np.zeros((r + 1, s + 1), int)

    for i in range(len(tab)):
        for j in range(len(tab[i])):
            for d in data:
                if x_partition[i][0] <= d["x"] < x_partition[i][1] and y_partition[j][0] <= d["y"] < y_partition[j][1]:
                    tab[i, j] += 1
    x_sum = sum(tab.transpose())
    y_sum = sum(tab)

    # Вычисление статистики
    T = 0
    for i in range(r + 1):
        for j in range(s + 1):
            T += ((n * tab[i, j] - x_sum[i] * y_sum[j]) ** 2) / (n * x_sum[i] * y_sum[j])
    p_value = 1 - stats.chi2.cdf(T, v)

    print("Критическая константа:", c_critical)
    print("Таблица сопряженности:", tab, sep='\n')
    print("x:", x_sum)
    print("y:", y_sum)
    print("Статистика T =", T)
    print("P значение:", p_value)
    if p_value > alf:
        print("Гипотеза независимости принимается!")
    else:
        print("Гипотеза независимости отвергается!")


def task_2():
    data = read.read("Data/r4z1.csv")
    predict_x = 116

    x = np.array([i["x"] for i in data])
    y = np.array([i["y"] for i in data])

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    x_std = np.std(x)
    y_std = np.std(y)

    cor = np.corrcoef(x, y)[0, 1]
    # y = k*x + b

    k, b, r_value, p_value, std_err = stats.linregress(x, y)
    # plt.plot(x, b + k * x, 'r', label='fitted line')

    print("M(x) =", x_mean)
    print("sigma(x) =", x_std)
    print("M(y) =", y_mean)
    print("sigma(y) =", y_std)
    print("Cor =", cor)
    print("Уравнение регрессий:", "y = %s + %s * (x - %s)" % (y_mean, cor * y_std / x_std, x_mean))
    print("Значение регрессий в точке X = %s" % predict_x,
          " равно Y = %s" % (y_mean + cor * y_std / x_std * (predict_x - x_mean)))

    plt.plot(x, y, 'o', label='original data')
    plt.plot(x, y_mean + cor * y_std / x_std * (x - x_mean), 'r', label='fitted line')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
