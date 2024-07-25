# -*- coding: utf-8 -*-
"""
Equation for a cambered 4-digit NACA airfoil
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
from scipy.optimize import root

pd.set_option('display.float_format', '{:.3f}'.format)
pd.set_option('display.max_columns', None)

class NACA4turbo:
    def __init__(self, p, t):
        # self.m = m / 100 # максимальный развал
        self.p = p / 10 # место максимального развала
        self.t = t / 100 # максимальная толщина в долях хорды
        
        self.coef = np.array([0.2969, -0.126, -0.3516, 0.2843, -0.1015])
        self.pol = lambda x: (0.2969*x**.5 - 0.126*x - 0.3516*x**2 + 
                              0.2843*x**3 - 0.1015*x**4)
        

    def profile(self, m):
        self.m = m / 100 # максимальный развал
        self.n = 200
        self.f = pd.DataFrame(columns=['x', 'yc', 'dyc', 'teta', 'yt', 'xU', 'yU', 
                    'xL', 'yL'], index=range(self.n), dtype=float)
        
        self.f.x = np.linspace(0, 1, self.n)
        
        # координата линии развала
        self.f.loc[((self.f.x <= self.p)), 'yc'] = (self.m / self.p**2 *
                    (2 * self.p * self.f.loc[((self.f.x < self.p)), 'x'] -
                    self.f.loc[((self.f.x < self.p)), 'x']**2))
        
        self.f.loc[((self.f.x > self.p)), 'yc'] = (self.m / (1 - self.p)**2 *
                    (1 - 2 * self.p + 2 * self.p * self.f.loc[((self.f.x > self.p)), 'x'] -
                     self.f.loc[((self.f.x > self.p)), 'x']**2))
        
        # градиент линии развала 
        self.f.loc[((self.f.x <= self.p)), 'dyc'] = (2 * self.m / self.p**2 *
                    (self.p - self.f.loc[((self.f.x <= self.p)), 'x']))
        
        self.f.loc[((self.f.x > self.p)), 'dyc'] = (2 * self.m / (1 - self.p)**2 *
                    (self.p - self.f.loc[((self.f.x > self.p)), 'x']))
        
        # толщина 
        self.f.yt = self.t / 2 * self.pol(self.f.x) * 10
        
        self.f.teta = np.arctan(self.f.dyc)
        
        # координата верхней поверхности профиля 
        self.f.yU = self.f.yc + self.f.yt * np.cos(self.f.teta)
        self.f.yL = self.f.yc - self.f.yt * np.cos(self.f.teta)
        
        # координата нижней поверхности профиля
        self.f.xU = self.f.x - self.f.yt * np.sin(self.f.teta)
        self.f.xL = self.f.x + self.f.yt * np.sin(self.f.teta)
        
        self.g = pd.Series([np.nan], index=['alpha1'])
        
        # расчет углов
        self.g['alpha1'] = math.degrees(math.atan((self.f.yc[1] - 
                        self.f.yc[0]) / (self.f.x[1] - self.f.x[0])))
        
        self.g['alpha2'] = math.degrees(math.atan((self.f.yc[self.n-1] - 
                        self.f.yc[self.n-2]) / (self.f.x[self.n-1] - self.f.x[self.n-2])))
       
        self.g['d_alpha'] = self.g['alpha1'] - self.g['alpha2']
        
        return self.g['d_alpha']
        
        
    def plot(self, n=100):
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
        # title = ('NACA-' + str(int(self.m*100)) + '-' + str(int(self.p*10)) + 
        #         '-' + str(int(self.t*100)))
        # file_name =  title + '.jpg'
        # plt.title(title, loc='left')
        plt.tight_layout() # оптимизируем поля и расположение объектов
        plt.savefig('NACA4-turbo-alpha.jpg', dpi = 300)
        plt.show()


    def flowAngle(self, dalpha):
        def func_resedual(x, dalpha):
            resedual = self.profile(m=x) - dalpha
            return resedual
        sol = root(func_resedual, 5, args=(dalpha))
        print(sol.x[0])
        
        



