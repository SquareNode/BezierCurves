# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 14:33:22 2020

@author: Nikola
"""


import sys
import matplotlib.pyplot as plt
    
def n_over_k(n,k):
    if k == 0:
        return 1
    if k == n:
        return 1
    return n_over_k(n-1, k-1) + n_over_k(n-1, k)
    

def get_poly(i,n):
    """
    
    takes integer i and n -> degree of curve
    returns polynomial (n i) * t^i * (1-t)^n-i as arr of coef
    1 + 2t + t^3 -> [1,2,0,1]
    
    """
    
    res,deg = [],n-i
    
    #calc (1-t)^n-1
    for j in range(deg+1):
        res.append((-1)**j*n_over_k(deg, j))
    for j in range(deg+1):
        res[j] *= n_over_k(n, i)
    #mul t^i
    for j in range(i):
        res.insert(0,0)

    return res        
    
def mul(point, poly, coord):
    
    res = []
    for i in range(len(poly)):
        res.append(point[coord] * poly[i])
    return res

def calc_curve_fs(points):
    """
    
    takes arr of points
    returns tuple - (x(t), y(t))
    
    """
    
    poly, deg = [], len(points) - 1
    
    for i in range(deg + 1):
        #(n i) * t^i * (1-t)^n-i
        #n over i 
        poly.append(get_poly(i, deg))
        
    
    i = 0
    resx = [0 for i in poly[0]]
    resy = [0 for i in poly[0]]
    for pol in poly:
        curr = 0
        for c in pol:
            
            resx[curr] += points[i][0] * c
            resy[curr] += points[i][1] * c
            curr+=1
       
        i+=1
    
    
    return(resx,resy)
    

def de_castelau(t, points):
    
    points_copy = [point for point in points]
    n = len(points) - 1
    k = 1
    while k <= n:
        i = 0
        while i <= n - k:
            points_copy[i] = ((1-t)*points_copy[i][0] + t * points_copy[i+1][0], 
                         (1-t)*points_copy[i][1] + t * points_copy[i+1][1])
            i+=1
        k+=1
        
    return points_copy[0]
    
    

if __name__ == '__main__':
    
    points = [(1,1), (-2,-5), (1,12), (3, 5)]
    
    dt = 1e-3
    t = 0
    
    res = []
    
    funcs = calc_curve_fs(points)
    
    fx = f'{funcs[0][0]}'
    fy = f'{funcs[1][0]}'
    
    for i in range(1, len(funcs[0])):
        fx += f'+{funcs[0][i]} t^ {i}'
        fy += f'+{funcs[1][i]} t^ {i}'
    
    print(fx,'\n',fy)    
    
    while t <= 1:
        res.append(de_castelau(t,points))
        t+=dt
    
    
    
    start_xes, start_ys = [], []
    
    for point in points:
        start_xes.append(point[0])
        start_ys.append(point[1])
        
    curve_xes, curve_ys = [], []
    
    for r in res:
        curve_xes.append(r[0])
        curve_ys.append(r[1])
        
    plt.figure()
    # plt.scatter(start_xes, start_ys)
    plt.plot(start_xes,start_ys, '-o', label='control points')
    plt.plot(curve_xes, curve_ys, label='curve')
    plt.title('Bezier curve')
    plt.legend(('control points', 'curve'))
    plt.show()