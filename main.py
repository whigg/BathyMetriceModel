# File      :main_02.py
# Author    :WJ
# Function  :
# Time      :2021/07/13
# Version   :
# Amend     :
import os, h5py
import time
import numpy as np
import pandas as pd
import SeaSurfaceAndSeaFloorDetection_02 as detect
np.set_printoptions(suppress=True)
import Section as sction
import ReadH5 as readh5
from icecream import ic

if __name__ == '__main__':
    bound = [111.59, 16.530, 111.62, 16.55]
    step1 = 1
    step2 = 30
    print("********************************************")
    ##
    # 运行目录
    os.chdir(r'D:\Program Files\JetBrains\PycharmProjects\BathyMetriceModel\data0')
    seasurface_all=[]
    seafloor_all=[]
    for hdf_file in os.listdir():
        for beam in ['gt1l','gt2l','gt3l']:  #循环处理3个激光波束
            if hdf_file[-4:] == ".hdf" or hdf_file[-3:] == ".h5":
                h5File = hdf_file
                prefix = h5File + beam
                print('------------------------------')
                ic(prefix)

                csv_ph= readh5.h5TOcsv(h5File,beam,bound=bound)
                print(len(csv_ph))
                if len(csv_ph)>1000:
                    ic(csv_ph)
                    # csv_ph.to_csv('../output/' + prefix + '_all.csv')
                    ic()
                    seaSurface, aboveSurface, underSurface, seaFloor1, seaFloor2, seaFloor3 = detect.surfaceAndFloorDetection(
                    csv_ph, step1, step2)
                    ic()
                    seasurface_all.extend(seaSurface.to_numpy())
                    seafloor_all.extend(seaFloor3.to_numpy())
                    ic()
                    # seaSurface.to_csv('../output/' + prefix + '_seaSurface.csv')
                    # seaFloor3.to_csv('../output/' + prefix + '_seaFloor_03.csv')
                    sction.Section_one(seaSurface, prefix + '_surface_' + str(step1) + '+' + str(step2))
                    sction.Section_one(seaFloor3, prefix + '_seafloor_' + str(step1) + '+' + str(step2))


    print(len(seasurface_all))
    seasurface_all=np.array(seasurface_all)
    np.savetxt('../output/seasurface_all_0723.txt',seasurface_all,delimiter=',',fmt='%.03f')

    print(len( seafloor_all))
    seafloor_all = np.array(seafloor_all)
    np.savetxt('../output/seafloor_all_0723.txt', seafloor_all, delimiter=',',fmt='%.03f')#,




