# -*- coding: utf-8 -*-
"""
Equation for a cambered 4-digit NACA airfoil
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

pd.set_option('display.float_format', '{:.4f}'.format)
pd.set_option('display.max_columns', None)

class NACA4camb:
    def __init__(self, profile):
        self.profile = profile
        self.m = int(profile[0]) / 100 # максимальный развал
        self.p = int(profile[1]) / 10 # место максимального развала
        self.t = int(profile[2:4]) / 100 # максимальная толщина в долях хорды
        
        self.coef = np.array([0.2969, -0.126, -0.3516, 0.2843, -0.1015])
        self.pol = lambda x: (0.2969*x**.5 - 0.126*x - 0.3516*x**2 + 
                              0.2843*x**3 - 0.1015*x**4)
        
    def plot(self, n=200):

        self.f = pd.DataFrame(columns=['x', 'yc', 'dyc', 'teta', 'yt', 'xU', 'yU',
                    'xL', 'yL'], index=range(n), dtype=float)
        
        self.f.x = np.linspace(0, 1, n)
        
        # координата линии развала
        self.f.loc[((self.f.x <= self.p)), 'yc'] = (self.m / self.p**2 *
                    (2 * self.p * self.f.x.loc[((self.f.x < self.p))] - 
                    self.f.x.loc[((self.f.x < self.p))]**2))
        
        self.f.loc[((self.f.x > self.p)), 'yc'] = (self.m / (1 - self.p)**2 *
                    (1 - 2 * self.p + 2 * self.p * self.f.x.loc[((self.f.x > self.p))] - 
                     self.f.x.loc[((self.f.x > self.p))]**2))
        
        # градиент линии развала 
        self.f.loc[((self.f.x <= self.p)), 'dyc'] = (2 * self.m / self.p**2 *
                    (self.p - self.f.x.loc[((self.f.x <= self.p))]))
        
        self.f.loc[((self.f.x > self.p)), 'dyc'] = (2 * self.m / (1 - self.p)**2 *
                    (self.p - self.f.x.loc[((self.f.x > self.p))]))
        
        # толщина 
        self.f.yt = self.t / 2 * self.pol(self.f.x) * 10
        
        self.f.teta = np.arctan(self.f.dyc)
        
        # координата верхней поверхности профиля 
        self.f.yU = self.f.yc + self.f.yt * np.cos(self.f.teta)
        self.f.yL = self.f.yc - self.f.yt * np.cos(self.f.teta)
        
        # координата нижней поверхности профиля
        self.f.xU = self.f.x - self.f.yt * np.sin(self.f.teta)
        self.f.xL = self.f.x + self.f.yt * np.sin(self.f.teta)
        
        plt.figure(figsize=(5, 4))
        
        plt.plot(self.f.xU,self.f.yU,color='red',lw=1) # верхняя поверхность
        plt.plot(self.f.xL,self.f.yL,color='red',lw=1) # нижняя поверхность
        plt.plot(self.f.x,self.f.yc,color='green',label='mean',linestyle='--',lw=1) # верхняя поверхность
        plt.plot([0,1],[0,0],color='blue',label='chord',linestyle='--',lw=1) # верхняя поверхность
        
        plt.xlabel('x') 
        plt.ylabel('y') 
        plt.grid(linestyle='--', linewidth=0.5, color='black') # сетка
        plt.axis('equal')
        plt.legend()
        file_name = 'NACA' + self.profile + '.jpg'
        plt.title('NACA' + self.profile, loc='left')
        plt.tight_layout() # оптимизируем поля и расположение объектов
        plt.savefig('NACA4camb.jpg', dpi = 300)
        plt.show()




