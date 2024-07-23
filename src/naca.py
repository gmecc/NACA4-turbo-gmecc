# -*- coding: utf-8 -*-
"""
Equation for a symmetrical 4-digit NACA airfoil
"""

import matplotlib.pyplot as plt
import numpy as np
import math

class NACA4sym:
    def __init__(self, profile):
        self.m = int(profile[0]) / 100
        self.p = int(profile[1]) / 100
        self.t = int(profile[2:4]) / 100 # максимальная толщина в долях хорды
        
    def plot(self):

        n = 100
        x = np.linspace(0, 1, n)
        y = 5 * self.t * (0.2969 * x**.5 - 0.126 * x - 0.3516 * x**2 
                      + 0.2843 * x**3 - 0.1015 * x**4)
        
        plt.figure(figsize=(5, 4))
        
        plt.plot(x, y) # верхняя поверхность
        plt.plot(x, -y) # нижняя поверхность
        plt.xlabel('x') 
        plt.ylabel('y') 
        plt.grid(linestyle='--', linewidth=0.5, color='black') # сетка
        plt.ylim(-0.4, 0.4)
        plt.axis('equal')
        plt.show()

# pr = NACA4sym('0015')
# pr.plot()


