#!/ usr/bin/python
# -*- coding:utf-8 -*-

import math


def LonLat2XY(longitude,latitude):
  a = 6378137.0
  # b = 6356752.3142
  # c = 6399593.6258
  # alpha = 1 / 298.257223563
  e2 = 0.0066943799013
  # epep = 0.00673949674227


  #将经纬度转换为弧度
  latitude2Rad = (math.pi / 180.0) * latitude

  beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
  L = beltNo * 3 #计算中央经线
  # print(L)
  l0 = longitude - L #经差
  tsin = math.sin(latitude2Rad)
  tcos = math.cos(latitude2Rad)
  t = math.tan(latitude2Rad)
  m = (math.pi / 180.0) * l0 * tcos
  et2 = e2 * pow(tcos, 2)
  et3 = e2 * pow(tsin, 2)
  X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
    4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
  N = a / math.sqrt(1 - et3)

  x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
  61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
  y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
  5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)

  return x, y, L


def XY2LonLat(X, Y, L0):
  '''高斯坐标的X,Y'''

  iPI = 0.0174532925199433
  a = 6378137.0
  f= 0.00335281006247
  ZoneWide = 3 #按3度带进行投影

  ProjNo = int(Y / 1000000)
  L0 = L0 * iPI
  Y0 = ProjNo * 1000000 + 500000
  X0 = 0
  Yval = Y - Y0
  Xval = X - X0

  e2 = 2 * f - f * f #第一偏心率平方
  e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
  ee = e2 / (1 - e2) #第二偏心率平方

  M = Xval
  u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

  fai = u \
     + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
     + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
     + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u)\
     + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
  C = ee * math.cos(fai) * math.cos(fai)
  T = math.tan(fai) * math.tan(fai)
  NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
  R = a * (1 - e2) / math.sqrt(
    (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)))
  D = Yval / NN

  #计算经纬度（弧度单位的经纬度）
  longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
  5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
  latitude1 = fai - (NN * math.tan(fai) / R) * (
  D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
  61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)

  #换换为deg
  longitude = longitude1 / iPI
  latitude = latitude1 / iPI

  return longitude,latitude

def to_XY(lon,lat):
  x = []
  y = []
  for j in range(len(lon)):
    a, b, L = LonLat2XY(lon[j],lat[j])
    x.append(a)
    y.append(b)

  return x, y, L


def to_LonLat(X, Y, L):
  lon = []
  lat = []
  for j in range(len(X)):
    a, b = XY2LonLat(Y[j], X[j], L)
    lon.append(a)
    lat.append(b)
  return lon, lat
#
if __name__=="__main__":
  x,y,L0=LonLat2XY(111.6184695,16.54999562)
  print(x,y)
  lon,lat=XY2LonLat(x, y,L0)
  print(lon,lat)
