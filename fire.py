import matplotlib.pylab as plt
import noise
import numpy as np
from numpy import arange, linspace

# from utils import measure_time
# from numba import jit
#
# from math import tan, pi, trunc
# from random import uniform

# def iterp_interval(x1, x2, a1, a2):
#     def __poly(x):
#         b = (a1 + a2) / (x2 - x1) ** 2 - x2 - x1
#         c = -(a1 * x2 + a2 * x1) / (x2 - x1) ** 2 + x1 * x2
#         return (x - x1) * (x - x2) * (x ** 2 + b * x + c)
#
#     return __poly
#
#
# @measure_time
# def gen(start, stop, step, res=None):
#     res = 50 // step if res is None else res
#
#     # generate points
#     xs = linspace(start, stop, (stop - start) // step)
#
#     # generate gradient
#     grads = [tan(uniform(-pi / 2 + 0.5, pi // 2 - 0.5)) for i in range(len(xs))]
#
#     # interpolate intervals
#     polies = [iterp_interval(xs[i], xs[i + 1], grads[i], grads[i + 1]) for i in range(len(xs) - 1)]
#
#     # calculating points
#     points_x = np.concatenate(
#         [
#             linspace(xs[pos], xs[pos + 1], res)
#             for pos in range(len(xs) - 1)
#         ],
#         axis=0
#     )
#
#     points_y = np.concatenate(
#         [
#             poly(points_x[res * i:res * (i + 1)])
#             for i, poly in enumerate(polies)
#         ],
#         axis=0
#     )
#     return points_x, points_y
#
#
# @measure_time
# def gen_good_api(start, stop, step, points=100):
#     ang = pi // 2 - 0.5
#     # generate points
#     num_intervals = trunc((stop - start) / step)
#
#     # generate gradient
#     grads = [tan(uniform(-ang, ang)) for i in range(num_intervals + 1)]
#
#     # interpolate intervals
#     polies = [iterp_interval(start + i * step, start + (i + 1) * step, grads[i], grads[i + 1])
#               for i in range(num_intervals)]
#     # calculating points
#     points_x = linspace(start, stop, points)[:-1]
#     z = [polies[trunc((x - start) / step)](x) for x in points_x[:-1]]
#     z.extend([polies[-1](points_x[-1])])
#     points_y = np.array(z)
#     return points_x, points_y
#
#
# @measure_time
# @jit
# def gen_fast(start, stop, step, res=50):
#     ang = pi // 2 - 0.5
#     # generate endpoints
#     xs = arange(start, stop, step)
#
#     points_x = []
#     points_y = []
#     for pos in range(len(xs) - 1):
#         x1 = xs[pos]
#         x2 = xs[pos + 1]
#         a1 = tan(uniform(-ang, ang))
#         a2 = tan(uniform(-ang, ang))
#
#         b = (a1 + a2) / (x2 - x1) ** 2 - x2 - x1
#         c = -(a1 * x2 + a2 * x1) / (x2 - x1) ** 2 + x1 * x2
#
#         x = linspace(x1, x2, res)
#         y = (x - x1) * (x - x2) * (x ** 2 + b * x + c)
#
#         points_x.extend(x)
#         points_y.extend(y)
#
#     return np.array(points_x), np.array(points_y)




def ns(y, points=100, seed=3, octaves=1):
    xs = linspace(0, 10, points)
    ys = np.array([noise.pnoise3(x, y, seed, octaves) for x in xs])
    return xs, ys


import pygame
from pygame.draw import circle, line

pygame.init()

pygame.init()

sc = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()
offset = 1
speed = 1
zx, zy = 80, 300
offset_y = 400
mu, sigma = 0, 0.9
numpoints = 1000
x = np.linspace(-4.5, 4.5, numpoints)
s = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

x2 = np.linspace(-10, 10, numpoints)
s2 = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (x2 - mu) ** 2 / (2 * sigma ** 2))
plt.plot(x2, s2)
plt.show()
n = 2
a = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    sc.fill((0, 0, 0))
    offset += speed * clock.get_time() / 1000
    xs, ys = ns(offset, points=numpoints, octaves=7)
    zs = - a * (xs - 5) ** (2 * n) + a
    ys *= s
    ys += s2
    ys += 0.1
    ys *= zs

    for pos in range(2 * numpoints // 5, numpoints * 3 // 5):
        # circle(sc, (255, 0, 0), (xs[pos] * zx, -ys[pos] * zy + offset_y), 1)
        line(sc, (255, 0, 0), (xs[pos] * zx, -ys[pos] * zy + offset_y),
             (xs[pos + 1] * zx, -ys[pos + 1] * zy + offset_y))
    pygame.display.update()
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick()
