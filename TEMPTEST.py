import os
import sys

sys.path.insert(1, os.path.abspath('.'))

from PIL import Image
import random
import math
import matplotlib.pyplot as plt
import world.noise.noise_handler as noise_handler
from pygame.math import Vector2

dtest = {}


# def get_gradient(p, gt, pt):
#     return gt[pt[(p[0] + pt[p[1] % len(pt)]) % len(pt)] % len(gt)]
#
#
# def get_fade(t):
#     return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
#
#
# def scalar(a, b):
#     return a[0]*b[0] + a[1]*b[1]
#
#
# def noise_1D(x, gt, pt, res):
#     x /= res
#     p0 = math.floor(x)
#     p1 = p0 + 1
#
#     t = x - p0
#     fade_t = get_fade(t)
#
#     g0 = gt[pt[p0 % len(pt)] % len(gt)]
#     g1 = gt[pt[(p0 + 1) % len(pt)] % len(gt)]
#
#     return (1 - fade_t) * g0 * (x - p0) + fade_t * g1 * (x - p1)
#
#
# def get_color_code(x, y, gt, pt, res=50):
#     x /= res
#     y /= res
#
#     p0 = (math.floor(x), math.floor(y))
#     p1 = (p0[0] + 1, p0[1])
#     p2 = (p0[0], p0[1] + 1)
#     p3 = (p0[0] + 1, p0[1] + 1)
#
#     v_g0 = get_gradient(p0, gt, pt)
#     v_g1 = get_gradient(p1, gt, pt)
#     v_g2 = get_gradient(p2, gt, pt)
#     v_g3 = get_gradient(p3, gt, pt)
#
#     t0 = x - p0[0]
#     fade_t0 = get_fade(t0)
#
#     t1 = y - p0[1]
#     fade_t1 = get_fade(t1)
#
#     p0p1 = (1.0 - fade_t0) * scalar(v_g0, (x - p0[0], y - p0[1])) + fade_t0 * scalar(v_g1, (x - p1[0], y - p1[1]))
#     p2p3 = (1.0 - fade_t0) * scalar(v_g2, (x - p2[0], y - p2[1])) + fade_t0 * scalar(v_g3, (x - p3[0], y - p3[1]))
#
#     return (1.0 - fade_t1) * p0p1 + fade_t1 * p2p3
#
#
# random.seed("Negro")
# permut_table = [i for i in range(256)]
# random.shuffle(permut_table)
# print(permut_table)
#
# unit = 1 / math.sqrt(2)
# gradient_table_2D = ((unit, unit), (-unit, unit), (unit, -unit), (-unit, -unit), (1, 0), (-1, 0), (0, 1), (0, -1))
# gradient_table_1D = (-1, 1)
n_handler = noise_handler.NoiseHandler("Niggaria")
# ----------------------------------------
axis_x = []
axis_y = []
size = 4096
for i in range(size):
    axis_x.append(i)
    value = n_handler.get_1D_noise(i, res=1024, lenght_mod=size)
    value += n_handler.get_1D_noise(i, res=512, lenght_mod=size) * 0.5
    value += n_handler.get_1D_noise(i, res=256, lenght_mod=size) * 0.25
    value += n_handler.get_1D_noise(i, res=128, lenght_mod=size) * 0.125
    value += n_handler.get_1D_noise(i, res=64, lenght_mod=size) * 0.125
    value += n_handler.get_1D_noise(i, res=32, lenght_mod=size) * 0.025
    axis_y.append(value)

    if i == 0 or i == 2048:
        print(value)

plt.plot(axis_x, axis_y)
plt.show()
# ----------------------------------------

# min = 128
# max = 128
# size = (2048, 256)
# img = Image.new('RGB', size)
# for i in range(size[0]):
#     for j in range(size[1]):
#         value = n_handler.get_2D_noise(Vector2(i, j), res=256)
#         value += n_handler.get_2D_noise(Vector2(i, j), res=128) * 0.7
#         value += n_handler.get_2D_noise(Vector2(i, j), res=64) * 0.6
#         value += n_handler.get_2D_noise(Vector2(i, j), res=32) * 0.5
#
#         gray_level = int(((value + 0.3) * 0.5 * 255))
#
#         if gray_level < min:
#             min = gray_level
#         if gray_level > max:
#             max = gray_level
#
#         img.putpixel((i, j), (gray_level, gray_level, gray_level))
#
# print(min, max)
# img.show()

