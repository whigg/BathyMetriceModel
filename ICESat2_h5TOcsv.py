# File      :ICESat2_h5TOcsv.py
# Author    :WJ
# Function  :
# Time      :2021/06/27
# Version   :
# Amend     :
import XY2LONLAT
import os, h5py  # 导入工具包
import numpy as np
import pandas as pd


def h5TOcsv(h5file, csvfile, beam, bound=[111.55, 16.5, 111.64, 16.6]):
    '''beam为激光波束，在ICESat-2中分别有gt1l,gt1r,gt2l,gt2r,gt3l,gt3r六种激光波束'''
    # HDF5的读取：
    print("Running:Open h5file")
    f = h5py.File(h5file, 'r')  # 打开h5文件
    # 读取经纬度、高程等信息
    print("Running:Reading data")
    lon_ph = f[beam + '/heights/lon_ph'][:]
    lat_ph = f[beam + '/heights/lat_ph'][:]
    h_ph = f[beam + '/heights/h_ph'][:]
    delta_time = f[beam + '/heights/delta_time'][:]
    dist_ph_across = f[beam + '/heights/dist_ph_across'][:]
    dist_ph_along = f[beam + '/heights/dist_ph_along'][:]
    f.close()
    # 组织坐标文件，每行一个点位，[经度，维度,高程...]
    coorSet = np.vstack((lon_ph, lat_ph, h_ph, dist_ph_along, dist_ph_across, delta_time,))
    del lon_ph, lat_ph, h_ph, dist_ph_along, dist_ph_across, delta_time
    coorSet_T = coorSet.T
    # 清洗Nodata，清洗范围外的数据
    # <editor-fold desc="数据清洗">
    print("Running:deleting invalid values:", len(coorSet_T))
    invalidDataSet = []
    for i in range(0, len(coorSet_T)):
        # 按经度清洗
        if (coorSet_T[i, 0] > bound[2]) or (coorSet_T[i, 0] < bound[0]):
            invalidDataSet.append(i)
            continue
        # 按纬度清洗
        if (coorSet_T[i, 1] > bound[3]) or (coorSet_T[i, 1] < bound[1]):
            invalidDataSet.append(i)
            continue
        # 按高度清洗
        if (coorSet_T[i, 2] > 1000):
            invalidDataSet.append(i)
            continue
    coorSet_T = np.delete(coorSet_T, invalidDataSet, axis=0)
    # </editor-fold>
    print("Running:coorSet_T:", len(coorSet_T))
    print("Running:OUT csvfile")
    csv_ph = pd.DataFrame()
    csv_ph['lon_ph'] = coorSet_T[:, 0]
    csv_ph['lat_ph'] = coorSet_T[:, 1]
    csv_ph['X'],csv_ph['Y'],_=XY2LONLAT.to_XY(coorSet_T[:, 0],coorSet_T[:, 1])
    csv_ph['h_ph'] = coorSet_T[:, 2]
    csv_ph['dist_ph_along'] = coorSet_T[:, 3]
    csv_ph['dist_ph_across'] = coorSet_T[:, 4]
    csv_ph['delta_time'] = coorSet_T[:, 5]
    csv_ph.to_csv(csvfile, index=False)


if __name__ == '__main__':
    print("********************************************")
    print("Transform h5File TO shpFile")
    print("********************************************")
    ##
    # 运行目录
    os.chdir(r'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\data')
    for hdf_file in os.listdir():
        # for beam in ['gt1l','gt1r','gt2l','gt2r','gt3l','gt3r']:  #循环处理六个激光波束
        for beam in ['gt3l']:  # 选择了其中一个激光波束
            if hdf_file[-4:] == ".hdf" or hdf_file[-3:] == ".h5":
                h5File = hdf_file
                csvFile = h5File.replace(".h5", '_' + beam + ".csv")
                csvFile = csvFile.replace(".hdf", '_' + beam + ".csv")
                # csvFile = os.path.join("csvFile", csvName)
                print(csvFile)
                print("")
                print("Transforming", h5File, csvFile)
                try:
                    h5TOcsv(h5File, csvFile, beam)
                    print("Transformed", h5File, "TO", csvFile)
                except:
                    print("***Error:Transforming", h5File, "TO", csvFile)
