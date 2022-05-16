import random
import math


def gen_raw_noise(length, diff_max=1):
    nt_x = []
    nt_y = []

    for i in range(length - 1):
        nt_x.append(i)
        nt_y.append(random.uniform(-1, 1))

    for i in range(len(nt_y)):
        if i != 0 and abs(nt_y[i] - nt_y[i - 1]) > diff_max:
            nt_y[i] = (nt_y[i] + nt_y[i - 1]) / 2

    nt_x.append(i + 1)
    nt_y.append(nt_y[0])

    return nt_x, nt_y


def gen_smooth_noise(length, pt_btw, diff_max=1):
    return __cos_noise_interpolation(gen_raw_noise(length, diff_max), pt_btw)


def __cos_noise_interpolation(noise, pt_btw):
    tab_x = []
    tab_y = []
    (nt_x, nt_y) = noise
    i = 0
    while i + 1 < len(nt_x):

        x_a = nt_x[i]
        y_a = nt_y[i]

        x_b = nt_x[i + 1]
        y_b = nt_y[i + 1]

        coef = (y_b - y_a) / 2

        for k in range(pt_btw):
            t = k * 1 / pt_btw

            tab_x.append(x_a + t)
            tab_y.append(-coef * (math.cos(t * math.pi) + 1) + y_b)
        i += 1
    return tab_x, tab_y
