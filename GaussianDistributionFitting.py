# File      :GaussianDistributionFitting.py
# Author    :WJ
# Function  :
# Time      :2021/07/04
# Version   :
# Amend     :

import numpy as np
np.set_printoptions(suppress=True, linewidth=np.nan,precision=3, formatter={'float': '{: 0.3f}'.format})
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



def Gaussian1(x, a, u, sigma):
    return a * np.exp(-((x - u) / sigma) ** 2)


def Gaussian2(x, a1, u1, sigma1, a2, u2, sigma2):
    return a1 * np.exp(-((x - u1) / sigma1) ** 2) + a2 * np.exp(-((x - u2) / sigma2) ** 2)


def Gaussian1_fit(x, y):
    '''input:x,y
    output:[a1,u1,sigma1]'''
    x = np.array(x)
    y = np.array(y)
    y_max = np.max(y)
    x_min = np.min(x)
    x_max = np.max(x)
    x_u1 = x[np.argmax(y)]
    p0 = [y_max, x_u1, (x_max - x_u1) / 3]
    # 拟合时需要设定参数边界，参数边界会对拟合效果产生关键影响
    try:
        popt, _ = curve_fit(Gaussian1, x, y, bounds=([0, x_min, 0.05], [y_max, x_max, (x_max - x_min) / 6]))
        # popt, _ = curve_fit(Gaussian1, x, y)
    # 若拟合失败，返回一个确定能包括原数据的参数，即不进行滤波
    except:
        try:
            popt, _ = curve_fit(Gaussian1, x, y, p0=p0)
        except:
            popt = p0
    if popt[0]<1:
        popt = p0
    return popt


def Gaussian2_fit(x, y):
    '''input:x,y
      output:[a1,u1,sigma1,a2,u2,sigma2]'''
    x = np.array(x)
    y = np.array(y)
    y_max = np.max(y)
    x_max = np.max(x)
    x_u1 = x[np.argmax(y)]

    sigma_01 = (x_max - x_u1) / 3
    x2 = x[x < x_u1 - 0.2]
    y2 = y[x < x_u1 - 0.2]

    x_u2 = x2[np.argmax(y2)]
    sigma_02 = (np.max(x) - x_u2) / 3
    p0 = [y_max, x_u1, sigma_01, np.max(y2), x_u2, sigma_02]
    # 拟合时的参数边界会对拟合效果产生关键影响，不设置则默认为无穷小至无穷大
    try:
        popt, _ = curve_fit(Gaussian2, x, y)
    except:
        try:
            popt, _ = curve_fit(Gaussian2, x, y,p0=p0)
        except:
            popt=p0
    return popt


def Gaussian1_show(data, para,med, sigma2, num, times):
    plt.figure(figsize=(8, 4.5))
    # plt.scatter(data[:,0],data[:,1],marker='.',c='r',label='true')
    x = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)
    y=Gaussian1(x,para[0],para[1],para[2])
    plt.plot(x,y,c='y',label='fit')
    plt.bar(data[:, 0], data[:, 1], label='hist_h', width=0.1)
    plt.axvline(x=med, ls='-', c='r', label='median=' + str(format(med, '.3f')))  # 添加垂直线
    plt.axvline(x=med - 2 * abs(sigma2), ls='--', c='gray')  # 添加垂直线
    plt.axvline(x=med + 2 * abs(sigma2), ls='--', c='gray', )  # 添加垂直线
    plt.xlabel('h')
    plt.ylabel('count')
    plt.legend(loc='best')
    plt.savefig('./pic/seaFloor/Gaussian1&Hist_' + str(format(times, '1d')) + '_' + str(format(num, '1.3f')) + '.png')
    # plt.pause(10)
    plt.close()


def Gaussian2_show(data, para, u1, sigma1, num):
    plt.figure(figsize=(8, 4.5))
    x = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)
    y = Gaussian2(x, para[0], para[1], para[2], para[3], para[4], para[5])
    plt.plot(x, y, c='r', label='fit')
    plt.bar(data[:, 0], data[:, 1], label='hist_h', width=0.1)
    plt.axvline(x=u1, ls='-', c='deeppink', label='u1=' + str(format(u1, '.3f')))  # 添加垂直线
    plt.axvline(x=u1 - 3 * abs(sigma1), ls='--', c='gray')  # 添加垂直线
    plt.axvline(x=u1 + 3 * abs(sigma1), ls='--', c='gray')  # 添加垂直线
    plt.xlabel('h')
    plt.ylabel('count')
    plt.legend(loc='best')
    plt.savefig('./pic/seaSurface/Gaussian2&Hist_' + str(format(num, '1.3f')) + '.png')
    # plt.pause(10)
    plt.close()



