import random
import math

from pygame.math import Vector2

PERMUTATION_TABLE_SIZE = 256

GRADIENT_TABLE_2D = (Vector2(1, 1).normalize(), Vector2(-1, 1).normalize(), Vector2(1, -1).normalize(), Vector2(-1, -1).normalize(), Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1))
GRADIENT_TABLE_1D = (-1, 1)


def interpolation_function(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def scalar(a, b):
    return a[0]*b[0] + a[1]*b[1]


class NoiseHandler:

    def __init__(self, seed):
        self.__seed = seed
        self.__permutation_table = [i for i in range(PERMUTATION_TABLE_SIZE)]
        self.reset()

    def __get_gradient_2D(self, point):
        return GRADIENT_TABLE_2D[self.__permutation_table[(int(point.x) + self.__permutation_table[int(point.y) % PERMUTATION_TABLE_SIZE]) % PERMUTATION_TABLE_SIZE] % len(GRADIENT_TABLE_2D)]

    def __get_gradient_1D(self, x):
        return GRADIENT_TABLE_1D[self.__permutation_table[x % PERMUTATION_TABLE_SIZE] % len(GRADIENT_TABLE_1D)]

    def get_1D_noise(self, x, res, lenght_mod=2048):
        lenght_mod = int(lenght_mod / res)
        x /= res
        p0 = math.floor(x)
        p1 = p0 + 1

        t = x - p0
        fade_t = interpolation_function(t)

        v_g0 = self.__get_gradient_1D(p0 % lenght_mod)
        v_g1 = self.__get_gradient_1D(p1 % lenght_mod)

        return (1 - fade_t) * v_g0 * (x - p0) + fade_t * v_g1 * (x - p1)

    def get_2D_noise(self, point, res):
        x, y = point.xy
        x /= res
        y /= res
        point.update(x, y)
        p0 = Vector2(math.floor(x), math.floor(y))
        p1 = Vector2(p0.x + 1, p0.y)
        p2 = Vector2(p0.x, p0.y + 1)
        p3 = Vector2(p0.x + 1, p0.y + 1)

        v_g0 = self.__get_gradient_2D(p0)
        v_g1 = self.__get_gradient_2D(p1)
        v_g2 = self.__get_gradient_2D(p2)
        v_g3 = self.__get_gradient_2D(p3)

        t0 = x - p0.x
        fade_t0 = interpolation_function(t0)

        t1 = y - p0.y
        fade_t1 = interpolation_function(t1)
        p0p1 = (1 - fade_t0) * v_g0.dot(point - p0) + fade_t0 * v_g1.dot(point - p1)
        p2p3 = (1 - fade_t0) * v_g2.dot(point - p2) + fade_t0 * v_g3.dot(point - p3)

        return (1.0 - fade_t1) * p0p1 + fade_t1 * p2p3

    def reset(self):
        random.seed(self.__seed)
        random.shuffle(self.__permutation_table)
