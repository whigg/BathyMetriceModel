# File      :Section.py
# Author    :WJ
# Function  :
# Time      :2021/06/28
# Version   :
# Amend     :

import matplotlib.pyplot as plt


def Section_one(csv_ph, picname):
    plt.figure(figsize=(16, 9), dpi=300)
    plt.scatter(x=csv_ph['lat_ph'], y=csv_ph['h_ph'], marker='.', label='h_ph')
    plt.rc('font', family='Times New Roman')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylim(-40, 40)
    plt.xlabel('lat_ph')
    plt.ylabel('h_ph')
    plt.legend(loc='best')
    plt.savefig('../pic/section/' + picname + '.png')
    plt.close()


def Section_all(All, seaSurface, floor01, floor02, floor03, picname):
    plt.figure(figsize=(16, 9), dpi=300)
    plt.rc('font', family='Times New Roman')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.scatter(x=All['lat_ph'], y=All['h_ph'], c='black', marker='.', label='ICESat-2 photon')
    plt.scatter(x=seaSurface['lat_ph'], y=seaSurface['h_ph'], c='blue', marker='.', label='seaSurface photon')
    plt.scatter(x=floor01['lat_ph'], y=floor01['h_ph'], c='orange', marker='.', label='seaFloor_1 photon')
    plt.scatter(x=floor02['lat_ph'], y=floor02['h_ph'], c='green', marker='.', label='seaFloor_2 photon')
    plt.scatter(x=floor03['lat_ph'], y=floor03['h_ph'], c='red', marker='.', label='seaFloor_3 photon')
    plt.ylim(-40, 40)
    plt.xlabel('lat_ph/dgree')
    plt.ylabel('h_ph/meter')
    plt.legend(loc='best')
    plt.savefig('../pic/section/' + picname + '.png')
    plt.close()
