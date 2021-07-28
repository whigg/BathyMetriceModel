# File      :Visualize_01.py
# Author    :WJ
# Function  :
# Time      :2021/06/28
# Version   :
# Amend     :

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import pandas
import pandas as pd


def visulize_csv(csvfile):

    csv_ph=pd.read_csv(csvfile)



    # <editor-fold desc="section">
    plt.figure(figsize=(16,9),dpi=300)
    plt.scatter(x=csv_ph['dist_ph_along'],y=csv_ph['h_ph'],marker='.',label='h_ph')
    plt.rc('font', family='Times New Roman')
    # plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylim(-50, 50)
    plt.xlabel('dist_ph_along')
    plt.ylabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('./pic/section-dist_ph_along.png')
    # plt.pause(10)
    plt.close()

    plt.figure(figsize=(16,9), dpi=300)
    plt.scatter(x=csv_ph['lat_ph'],y=csv_ph['h_ph'],marker='.',label='h_ph')
    plt.rc('font', family='Times New Roman')
    # plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylim(-50, 50)
    plt.xlabel('lat_ph')
    plt.ylabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('./pic/section-lat_ph.png')
    # plt.pause(10)
    plt.close()

    plt.figure(figsize=(16,9), dpi=300)
    plt.scatter(x=csv_ph['dist_ph_across'], y=csv_ph['h_ph'], marker='.', label='h_ph')
    plt.rc('font', family='Times New Roman')
    # plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylim(-50, 50)
    plt.xlabel('dist_ph_across')
    plt.ylabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('./pic/section-dist_ph_across.png')
    # plt.pause(10)
    plt.close()
    # </editor-fold>

    # <editor-fold desc="3d-section">
    fig = plt.figure(figsize=(16,9), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter( csv_ph['dist_ph_along'],csv_ph['dist_ph_across'],csv_ph['h_ph'], marker='.', label='h_ph')
    plt.rc('font', family='Times New Roman')
    # plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    ax.set_xlabel('dist_ph_along')
    ax.set_ylabel('dist_ph_across')
    ax.set_zlabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('./pic/3d-section.png')
    # plt.show()
    plt.close()
    # </editor-fold>

    fig = plt.figure(figsize=(16,9), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(csv_ph['lat_ph'], csv_ph['lon_ph'], csv_ph['h_ph'], marker='.', label='h_ph')
    plt.rc('font', family='Times New Roman')
    # plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    ax.set_xlabel('lat_ph')
    ax.set_ylabel('lon_ph')
    ax.set_zlabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('./pic/3d-section-xyh.png')
    # plt.show()
    plt.close()
    print('Done!')

def visulize_lat_h(csvfile,picname):
    csv_ph=pd.read_csv(csvfile)
    # <editor-fold desc="section">
    plt.figure(figsize=(16,9), dpi=300)
    plt.scatter(x=csv_ph['lat_ph'],y=csv_ph['h_ph'],marker='.',label='h_ph')
    plt.rc('font', family='Times New Roman')
    # plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylim(-40, 40)
    plt.xlabel('lat_ph')
    plt.ylabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('./pic/section/'+picname+'.png')
    # plt.pause(10)
    plt.close()
    # </editor-fold>
    print('Done!')

if __name__=='__main__':
    plt.figure(figsize=(16, 9), dpi=300)
    plt.rc('font', family='Times New Roman')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    csvfile = './data/ATL03_20190222135159_08570207_003_01_gt3l.csv'

    csv_ph = pd.read_csv(csvfile)
    plt.scatter(x=csv_ph['lat_ph'], y=csv_ph['h_ph'], c='black',marker='.', label='ICESat-2 photon')

    csvfile = './output/seaSurface.csv'
    csv_ph = pd.read_csv(csvfile)
    plt.scatter(x=csv_ph['lat_ph'], y=csv_ph['h_ph'], c='b', marker='.', label='seaSurface photon')

    csvfile = './output/seaFloor_01.csv'
    csv_ph = pd.read_csv(csvfile)
    plt.scatter(x=csv_ph['lat_ph'], y=csv_ph['h_ph'], c='orange', marker='.', label='seaFloor_1 photon')

    csvfile = './output/seaFloor_02.csv'
    csv_ph = pd.read_csv(csvfile)
    plt.scatter(x=csv_ph['lat_ph'], y=csv_ph['h_ph'], c='green', marker='.', label='seaFloor_2 photon')

    csvfile = './output/seaFloor_03.csv'
    csv_ph = pd.read_csv(csvfile)
    plt.scatter(x=csv_ph['lat_ph'], y=csv_ph['h_ph'], c='r', marker='.', label='seaFloor_3 photon')

    plt.ylim(-40, 40)
    plt.xlabel('lat_ph/dgree')
    plt.ylabel('h_ph/meter')
    plt.legend(loc='best')
    plt.savefig('./pic/section/DetectionResult_0712-1m+30.png')

    plt.close()
    print('Done!')

'''
    csvfile='./data/ATL03_20190222135159_08570207_003_01_gt3l.csv'
    visulize_csv(csvfile,'all')
    csvfile = './output/seaSurface.csv'
    visulize_csv(csvfile,'seaSurface')
    csvfile = './output/seaSurface.csv'
    visulize_csv(csvfile, 'seaSurface')
    csvfile = './data/ATL03_20190222135159_08570207_003_01_gt3l.csv'
    visulize_csv(csvfile,'all')
'''