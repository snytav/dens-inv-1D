# -*- coding: utf-8 -*-
"""exp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jwkxNnC31fAsqZ5wW05L6BPYTANIS5T5
"""

import torch         # библиотека для работы с нейронныит сетями. Здесь нужна для вычислений с производными
import numpy as np   # математическая библиотека Python
boxsize = 1.0        # размер расчетной области
Nx = 10              # количество узлов
N = 100              # количество частиц
pos = np.random.rand(N,1)*boxsize #  массив координат частиц
pos = torch.from_numpy(pos)       #  преобразоввание в формат библиотеки PyTorch
pos.requires_grad = True          #  флаг, разрешающий взятие производных по массиву pos

def denst(Pos,Nx,boxsize,n0):                      #  функция, вычисляющая плотность по массиву частиц
    dx = boxsize/Nx
    n= torch.zeros(Nx)
    for pos in Pos:
        j = torch.floor(pos / dx).long()
        #print('pos,j ',pos,j)
        jp1 = j + 1
        weight_j=(jp1 * dx - pos) / dx
        weight_jp1 = (pos - j * dx) / dx
        jp1 = torch.remainder(jp1, Nx)
        j   = torch.remainder(j, Nx)
        n[j] += weight_j
        n[jp1] += weight_jp1
    n *= n0 * boxsize / N / dx
    return n



n = denst(pos,Nx,boxsize,1.0)                     # пробный запуск
#n

xx = torch.linspace(0,boxsize,Nx)

import sys



import matplotlib.pyplot as plt
fig = plt.figure()
plt.legend()
n0 = torch.exp(xx) # профиль плоности, который нужно воспроизвести с помощью частиц. Обязательно в виде массива библиотеки PyTorch
plt.plot(xx.numpy(),n0.detach().numpy(),color='green')
optimizer = torch.optim.Adam([pos],lr=0.001)
lf = 1e6*torch.ones(1)
i = 0
while lf.item() > 1e-2:
    optimizer.zero_grad()
    n = denst(pos,Nx,boxsize,n0)
    n0 = torch.ones_like(n)
    #plt.plot(xx.numpy(),n.detach().numpy(),color='red',label='iteration '+ str(i))
    n0 = torch.exp(xx) # torch.ones_like(n)
    lf = torch.max(torch.abs(torch.subtract(n,n0)))  # функция потерь: разница между текущим и желаемым профилем плотности: max|n-n_0|
    print(i,lf.item())
    lf.backward()          # вычисление производных функции потерь по всему, от чего она зависит, в данном случае только производная по массиву pos
    optimizer.step()       # изменение независимых переменных (массива pos)
    i = i+1

plt.scatter(xx.numpy(),n.detach().numpy(),color='blue',marker='o')

def F(tau):
    if(torch.abs(tau) < 1.0):
      t = torch.exp(1-tau**2)
    else:
      t = 0
    return t
xx = torch.linspace(0,boxsize,Nx)

yy = [F(x) for x in xx]
n0 = torch.tensor(yy)
print(n0)

import matplotlib.pyplot as plt
plt.plot(xx.numpy(),n0.numpy())