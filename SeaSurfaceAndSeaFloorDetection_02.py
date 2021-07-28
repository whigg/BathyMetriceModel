# File      :SeaSurfaceAndSeaFloorDetection_02.py
# Author    :WJ
# Function  :海面海底光子检测
# Time      :2021/07/10
# Version   :2.0
# Amend     :

import math
import pandas as pd
import numpy as np
np.set_printoptions(suppress=False, linewidth=np.nan,precision=3, formatter={'float': '{: 0.3f}'.format})
import GaussianDistributionFitting as GausFit
from icecream import ic

def get_v(D, n):
    return D / (1 + math.log(n, 2))


def hist(array, step=0.1):
    x = np.arange(np.min(array), np.max(array) + step, step)
    hist = np.zeros((len(x), 1))
    for i in range(0, len(array)):
        for j in range(0, len(x) - 1):
            if array[i] >= x[j] and array[i] < x[j + 1]:
                hist[j] = hist[j] + 1
    Hist = np.vstack((x.transpose(), hist.transpose()))
    return Hist.transpose()


def get_u1sigma1(para):
    if para[0] > para[3]:
        u1 = para[1]
        sigma1 = para[2]
    else:
        u1 = para[4]
        sigma1 = para[5]
    return u1, sigma1


def surfaceAndFloorDetection(ph_data,step_01,step_02):
    '''海表光子与海底光子检测，
    输入清洗后的ICESat-2csv,
    输出海表光子, 海面上的光子, 海面下的光子, 第一次滤波的海底光子, 第二次滤波的海底光子, 第三次滤波的海底光子'''
    # 1.导入光子数据
    # ATL03 = pd.read_csv(csvfile)
    ATL03 = ph_data
    ATL03.sort_values('dist_ph_along', inplace=True, ignore_index=True)
    # '数据组织形式：'
    print(ATL03.columns.values)
    beg_01 = np.min(ATL03['dist_ph_along'])
    # 2.设置输出格式
    aboveSurface = pd.DataFrame(columns=ATL03.columns.values)
    seaSurface = pd.DataFrame(columns=ATL03.columns.values)
    underSurface = pd.DataFrame(columns=ATL03.columns.values)

    # 3.进行光子检测
    while beg_01 < np.max(ATL03['dist_ph_along']):
        end_01 = beg_01 + step_01
        print('----------------------------------')
        print('%.3f' % beg_01, '%.3f' % end_01)
        # 3.1 对原数据切片
        data_atl03 = ATL03[(beg_01 <= ATL03['dist_ph_along']) & (ATL03['dist_ph_along'] < end_01)]
        # 3.2 计算总直方图
        n=len(data_atl03)
        ic(len(data_atl03))
        D = 1
        v=get_v(D,n)

        # v = 0.1
        hist_2 = hist(data_atl03['h_ph'].values, v)
        # 3.3 双峰高斯分布拟合
        para = GausFit.Gaussian2_fit(hist_2[:, 0], hist_2[:, 1])
        print(para)
        u1, sigma1 = get_u1sigma1(para)
        # 绘制双峰高斯分布曲线
        # GausFit.Gaussian2_show(hist_2, para, u1, sigma1, beg_01)
        # 3.4 海表探测
        aboveSurface_ = data_atl03[data_atl03['h_ph'] >= u1 + 3 * abs(sigma1)]
        seaSurface_ = data_atl03[
            (u1 - 3 * abs(sigma1) <= data_atl03['h_ph']) & (data_atl03['h_ph'] < u1 + 3 * abs(sigma1))]
        underSurface_ = data_atl03[data_atl03['h_ph'] <= u1 - 3 * abs(sigma1)]

        aboveSurface = pd.concat([aboveSurface, aboveSurface_], ignore_index=False)
        seaSurface = pd.concat([seaSurface, seaSurface_], ignore_index=False)
        underSurface = pd.concat([underSurface, underSurface_], ignore_index=False)
        beg_01 += step_01

    
    # 3.5 海底探测(当海面下的光子数少于给定阈值(如20)时认为不存在海底，舍去)
    seaFloor_01 = pd.DataFrame(columns=ATL03.columns.values)
    seaFloor_02 = pd.DataFrame(columns=ATL03.columns.values)
    seaFloor_03 = pd.DataFrame(columns=ATL03.columns.values)
    beg_02 = np.min(underSurface['X'])
    while beg_02 < np.max(underSurface['X']):
        end_02 = beg_02 + step_02
        print('%.3f' % beg_02, '%.3f' % end_02)
        # 3.1 对原数据切片
        seafloor_ = underSurface[(beg_02 <= underSurface['X']) & (underSurface['X'] < end_02)]
        ic(len(seafloor_))
        i=0
        while   len(seafloor_)>10 and i<3:
            # 中值滤波迭代3次
            # if i == 0:
            #     median = np.median(seafloor_['h_ph'])
            median = np.median(seafloor_['h_ph'])
            hist_1 = hist(seafloor_['h_ph'].values, v)
            para = GausFit.Gaussian1_fit(hist_1[:, 0], hist_1[:, 1])
            sigma2 = para[2]
            print(para)
            seafloor_0 = seafloor_[
                (median - 2 * abs(sigma2) <= seafloor_['h_ph']) & (seafloor_['h_ph'] < median + 2 * abs(sigma2))]
            if len(seafloor_0) > 12:
                seafloor_ = seafloor_0
            # GausFit.Gaussian1_show(hist_1,para, median, sigma2, beg_02, i)
            if i == 0:
                seaFloor_01 = pd.concat([seaFloor_01, seafloor_], ignore_index=False)
            elif i == 1:
                seaFloor_02 = pd.concat([seaFloor_02, seafloor_], ignore_index=False)
            elif i == 2:
                seaFloor_03 = pd.concat([seaFloor_03, seafloor_], ignore_index=False)
            i+=1
        beg_02 += step_02

    return seaSurface, aboveSurface, underSurface, seaFloor_01, seaFloor_02, seaFloor_03

