# File      :CoordinateTransformation.py
# Author    :WJ
# Function  :
# Time      :2021/07/13
# Version   :
# Amend     :
import pyproj

def proj_trans(lon,lat):
    p1 = pyproj.Proj(init="epsg:4326")  # 定义数据地理坐标系
    # 4214    GCS_Beijing_1954
    # 4326    GCS_WGS_1984
    # 4490    GCS_China_Geodetic_Coordinate_System_2000
    # 4610    GCS_Xian_1980
    x1, y1 = p1(lon, lat)
    return x1,y1



